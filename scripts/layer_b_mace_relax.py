"""Layer B: regenerate MACE-MP-0 predictions on the smoke subset.

Follows the upstream MACE discovery protocol at the pinned commit:
MACE-MP-0 checkpoint, ASE FIRE, steps=500, fmax=0.05, FrechetCellFilter,
float64, final relaxed total energy as the prediction.

Output is one JSON record per structure and is resumable by appending to a
gzip JSONL file. The companion scorer is `layer_b_score.py --model mace-mp-0`.
"""

from __future__ import annotations

import argparse
import gzip
import json
import statistics
import time
from importlib.metadata import version
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
INIT_STRUCTS = "data/wbm/2022-10-19-wbm-init-structs.jsonl.gz"
MACE_MP_0_CHECKPOINT = (
    "https://github.com/ACEsuit/mace-foundations/releases/download/"
    "mace_mp_0/2023-12-03-mace-128-L1_epoch-199.model"
)
MAX_STEPS = 500
FMAX = 0.05


def stream_structures(path: Path, wanted: set[str]) -> dict[str, dict]:
    """Single pass over the jsonl.gz keeping only wanted material_ids."""
    found: dict[str, dict] = {}
    with gzip.open(path, "rt", encoding="utf-8") as fh:
        for line in fh:
            if len(found) == len(wanted):
                break
            rec = json.loads(line)
            mat_id = rec.get("material_id")
            if mat_id in wanted:
                struct = rec.get("initial_structure") or rec.get("structure")
                if struct is None:
                    raise KeyError(f"{mat_id}: no initial_structure key in {list(rec)}")
                found[mat_id] = struct
    missing = wanted - set(found)
    if missing:
        raise KeyError(
            f"{len(missing)} subset ids not in {path.name}: {sorted(missing)[:5]}"
        )
    return found


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", default="vendor/matbench-discovery")
    parser.add_argument("--subset", default="papers/matbench-discovery/layer_b_subset.csv")
    parser.add_argument("--limit", type=int, default=0, help="first N subset rows (0 = all)")
    parser.add_argument("--device", default="cuda", choices=["cuda", "cpu"])
    parser.add_argument("--out", required=True)
    parser.add_argument("--checkpoint", default=MACE_MP_0_CHECKPOINT)
    parser.add_argument(
        "--enable-cueq",
        action="store_true",
        help="enable cuequivariance acceleration if installed",
    )
    args = parser.parse_args()

    import torch
    from ase.filters import FrechetCellFilter
    from ase.optimize import FIRE
    from mace.calculators import mace_mp
    from pymatgen.core import Structure
    from pymatgen.io.ase import AseAtomsAdaptor

    if args.device == "cuda" and not torch.cuda.is_available():
        raise SystemExit(
            "--device cuda requested but torch.cuda.is_available() is False "
            "(documented CPU fallback: --device cpu)"
        )

    ids = pd.read_csv(ROOT / args.subset)["material_id"].tolist()
    if args.limit:
        ids = ids[: args.limit]

    out = ROOT / args.out
    done: set[str] = set()
    if out.is_file():
        with gzip.open(out, "rt", encoding="utf-8") as fh:
            done = {json.loads(line)["material_id"] for line in fh}
        print(f"resuming: {len(done)} of {len(ids)} ids already in {out.name}")
    todo = [mat_id for mat_id in ids if mat_id not in done]
    if not todo:
        print("nothing to do; all subset ids already relaxed")

    t0 = time.time()
    structures = stream_structures(ROOT / args.repo / INIT_STRUCTS, set(todo))
    print(f"loaded {len(structures)} initial structures in {time.time() - t0:.1f}s")

    calc = mace_mp(
        model=args.checkpoint,
        device=args.device,
        default_dtype="float64",
        enable_cueq=args.enable_cueq,
    )

    out.parent.mkdir(parents=True, exist_ok=True)
    failures: list[str] = []
    n_new = 0
    with gzip.open(out, "at", encoding="utf-8") as fh:
        for mat_id in todo:
            struct = Structure.from_dict(structures[mat_id])
            atoms = struct.to_ase_atoms()
            atoms.calc = calc
            start = time.time()
            try:
                filtered_atoms = FrechetCellFilter(atoms)
                optimizer = FIRE(filtered_atoms, logfile=None)
                converged = optimizer.run(fmax=FMAX, steps=MAX_STEPS)
                energy = atoms.get_potential_energy()
                final_fmax = float(np.linalg.norm(atoms.get_forces(), axis=1).max())
                relaxed_struct = AseAtomsAdaptor.get_structure(atoms)
                rec = dict(
                    material_id=mat_id,
                    mace_energy=float(energy),
                    mace_structure=relaxed_struct.as_dict(),
                    n_sites=len(atoms),
                    n_steps=int(optimizer.nsteps),
                    fmax_final=round(final_fmax, 5),
                    converged=bool(converged),
                    seconds=round(time.time() - start, 2),
                )
                fh.write(json.dumps(rec) + "\n")
                fh.flush()
                n_new += 1
            except (ValueError, RuntimeError, OSError, KeyError) as exc:
                failures.append(mat_id)
                print(f"FAILED {mat_id}: {exc!r}")

    with gzip.open(out, "rt", encoding="utf-8") as fh:
        records = [json.loads(line) for line in fh]
    secs = [record["seconds"] for record in records]
    print(f"this run: {n_new} new, {len(done)} resumed, {len(failures)} failed")
    print(
        f"versions: mace-torch {version('mace-torch')} | torch {version('torch')} | "
        f"numpy {version('numpy')} | device {args.device}"
        + (f" ({torch.cuda.get_device_name(0)})" if args.device == "cuda" else "")
    )
    print(
        f"protocol: MACE-MP-0 FIRE steps<={MAX_STEPS} fmax={FMAX} "
        f"FrechetCellFilter float64 enable_cueq={args.enable_cueq}"
    )
    print(f"relaxed {len(records)}/{len(ids)} | failures {len(failures)}")
    if secs:
        print(
            f"s/structure: mean {statistics.mean(secs):.2f} | "
            f"median {statistics.median(secs):.2f} | max {max(secs):.2f}"
        )
        print(f"converged: {sum(record['converged'] for record in records)}/{len(records)}")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
