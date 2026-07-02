"""Layer B: regenerate CHGNet predictions on the smoke subset (layer_b_plan.md §4).

Replicates the upstream generation protocol from
`models/chgnet/test_chgnet_discovery.py` at the pinned commit:
ASE FIRE relaxation via `chgnet.model.StructOptimizer`, `steps=500`, `fmax=0.05`,
`relax_cell=True`, FrechetCellFilter; the final trajectory energy is the prediction.

Reads initial structures by *streaming* the jsonl.gz (no full-frame load), writes one
JSON record per structure (energy, steps, convergence, wall time) to a git-ignored
experiments/ output. Per-structure try/except mirrors upstream.

Resumable: records are appended to --out as each structure completes (multi-member
gzip; readable by gzip.open transparently), and ids already present in --out are
skipped on restart. The end-of-run summary covers the whole file.

Usage (pre-smoke):
    python scripts/layer_b_relax.py --limit 20 --out experiments/layer-b/chgnet/presmoke-run1.jsonl.gz
"""

from __future__ import annotations

import argparse
import gzip
import inspect
import json
import statistics
import time
from importlib.metadata import version
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
INIT_STRUCTS = "data/wbm/2022-10-19-wbm-init-structs.jsonl.gz"
MAX_STEPS = 500  # upstream test_chgnet_discovery.py
FMAX = 0.05  # eV/Å, upstream


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
        raise KeyError(f"{len(missing)} subset ids not in {path.name}: {sorted(missing)[:5]}")
    return found


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default="vendor/matbench-discovery")
    ap.add_argument("--subset", default="papers/matbench-discovery/layer_b_subset.csv")
    ap.add_argument("--limit", type=int, default=0, help="first N subset rows (0 = all)")
    ap.add_argument("--device", default="cuda", choices=["cuda", "cpu"])
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    import torch
    from chgnet.model import StructOptimizer
    from pymatgen.core import Structure

    if args.device == "cuda" and not torch.cuda.is_available():
        raise SystemExit("--device cuda requested but torch.cuda.is_available() is False "
                         "(documented CPU fallback: --device cpu)")

    ids = pd.read_csv(ROOT / args.subset)["material_id"].tolist()
    if args.limit:
        ids = ids[: args.limit]

    out = ROOT / args.out
    done: set[str] = set()
    if out.is_file():  # resume: skip structures already relaxed into this file
        with gzip.open(out, "rt", encoding="utf-8") as fh:
            done = {json.loads(line)["material_id"] for line in fh}
        print(f"resuming: {len(done)} of {len(ids)} ids already in {out.name}")
    todo = [i for i in ids if i not in done]
    if not todo:
        print("nothing to do; all subset ids already relaxed")

    t0 = time.time()
    structures = stream_structures(ROOT / args.repo / INIT_STRUCTS, set(todo))
    print(f"loaded {len(structures)} initial structures in {time.time() - t0:.1f}s")

    relaxer = StructOptimizer(use_device=args.device)
    # chgnet's kwarg for the ASE cell filter differs across versions
    filter_kwarg = "ase_filter" if "ase_filter" in inspect.signature(
        relaxer.relax).parameters else "cell_filter"

    out.parent.mkdir(parents=True, exist_ok=True)
    failures: list[str] = []
    n_new = 0
    with gzip.open(out, "at", encoding="utf-8") as fh:
        for mat_id in todo:  # keep subset order
            struct = Structure.from_dict(structures[mat_id])
            t1 = time.time()
            try:
                result = relaxer.relax(
                    struct, verbose=False, steps=MAX_STEPS, fmax=FMAX, relax_cell=True,
                    **{filter_kwarg: "FrechetCellFilter"},
                )
                traj = result["trajectory"]
                final_fmax = float(np.linalg.norm(traj.forces[-1], axis=1).max())
                rec = dict(
                    material_id=mat_id,
                    chgnet_energy=float(traj.energies[-1]),
                    n_sites=len(struct),
                    n_steps=len(traj.energies),
                    fmax_final=round(final_fmax, 5),
                    converged=bool(final_fmax <= FMAX),
                    seconds=round(time.time() - t1, 2),
                )
                fh.write(json.dumps(rec) + "\n")
                fh.flush()
                n_new += 1
            except (ValueError, RuntimeError, OSError, KeyError) as exc:
                failures.append(mat_id)
                print(f"FAILED {mat_id}: {exc!r}")

    # summary over the whole file (resumed + new)
    with gzip.open(out, "rt", encoding="utf-8") as fh:
        records = [json.loads(line) for line in fh]
    print(f"this run: {n_new} new, {len(done)} resumed, {len(failures)} failed")
    secs = [r["seconds"] for r in records]
    print(f"versions: chgnet {version('chgnet')} | torch {version('torch')} | "
          f"numpy {version('numpy')} | device {args.device}"
          + (f" ({torch.cuda.get_device_name(0)})" if args.device == "cuda" else ""))
    print(f"protocol: FIRE steps<={MAX_STEPS} fmax={FMAX} relax_cell=True "
          f"FrechetCellFilter ({filter_kwarg})")
    print(f"relaxed {len(records)}/{len(ids)} | failures {len(failures)} "
          f"({len(failures) / len(ids):.0%})")
    if secs:
        print(f"s/structure: mean {statistics.mean(secs):.2f} | "
              f"median {statistics.median(secs):.2f} | max {max(secs):.2f}")
        print(f"converged: {sum(r['converged'] for r in records)}/{len(records)}")
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
