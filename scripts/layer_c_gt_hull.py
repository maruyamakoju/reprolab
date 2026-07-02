"""Layer C (ground truth): recompute e_above_hull from the MP phase diagram.

Layers A-C all *trusted* the WBM summary column
`e_above_hull_mp2020_corrected_ppd_mp`. This script audits that ground truth on the
committed 500-structure Layer B subset:

  WBM computed structure entry (published)
    -> MP2020 compatibility corrections (applied if the shipped entries lack them)
    -> e_above_hull vs the published PatchedPhaseDiagram (2023-02-07-ppd-mp.pkl.gz)
    -> compare against the WBM summary column.

A known risk is itself a finding: the phase diagram ships as a *pickle* created with
2023-era pymatgen; whether it even unpickles under pymatgen 2026 is part of the audit.

Usage:
    python scripts/layer_c_gt_hull.py --out papers/matbench-discovery/layer_c_gt_hull_check.md
"""

from __future__ import annotations

import argparse
import gzip
import json
import pickle
import sys
import time
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import compare_metrics as cm  # noqa: E402

CSE_FILE = "data/wbm/2022-10-19-wbm-computed-structure-entries.jsonl.gz"
PPD_FILE = "data/mp/2023-02-07-ppd-mp.pkl.gz"
GT_COL = "e_above_hull_mp2020_corrected_ppd_mp"


def stream_cses(path: Path, wanted: set[str]) -> dict[str, dict]:
    found: dict[str, dict] = {}
    with gzip.open(path, "rt", encoding="utf-8") as fh:
        for line in fh:
            if len(found) == len(wanted):
                break
            rec = json.loads(line)
            mat_id = rec.get("material_id")
            if mat_id in wanted:
                cse = rec.get("computed_structure_entry") or rec.get("entry") or rec
                found[mat_id] = cse
    missing = wanted - set(found)
    if missing:
        raise KeyError(f"{len(missing)} ids missing from CSE file: {sorted(missing)[:5]}")
    return found


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default="vendor/matbench-discovery")
    ap.add_argument("--subset", default="papers/matbench-discovery/layer_b_subset.csv")
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--out", default="papers/matbench-discovery/layer_c_gt_hull_check.md")
    args = ap.parse_args()

    from pymatgen.entries.compatibility import MaterialsProject2020Compatibility
    from pymatgen.entries.computed_entries import ComputedStructureEntry

    repo = (ROOT / args.repo).resolve()
    ids = pd.read_csv(ROOT / args.subset)["material_id"].tolist()
    if args.limit:
        ids = ids[: args.limit]

    t0 = time.time()
    raw = stream_cses(repo / CSE_FILE, set(ids))
    print(f"streamed {len(raw)} CSEs in {time.time() - t0:.1f}s")

    entries = {mid: ComputedStructureEntry.from_dict(d) for mid, d in raw.items()}
    n_pre_corrected = sum(bool(e.energy_adjustments) for e in entries.values())
    print(f"entries shipping WITH energy adjustments already applied: "
          f"{n_pre_corrected}/{len(entries)}")

    if n_pre_corrected < len(entries):
        compat = MaterialsProject2020Compatibility()
        processed = compat.process_entries(list(entries.values()), verbose=False,
                                           clean=True)
        proc_ids = {e.entry_id for e in processed}
        dropped = [mid for mid, e in entries.items() if e.entry_id not in proc_ids]
        print(f"MP2020 processed: {len(processed)}/{len(entries)} "
              f"(dropped: {len(dropped)})")
        entries = {e.entry_id: e for e in processed}
    else:
        dropped = []

    t0 = time.time()
    with gzip.open(repo / PPD_FILE, "rb") as fh:
        ppd = pickle.load(fh)
    print(f"unpickled PatchedPhaseDiagram under pymatgen "
          f"{__import__('pymatgen.core', fromlist=['__version__']).__version__} "
          f"in {time.time() - t0:.1f}s: {type(ppd).__name__} "
          f"({len(getattr(ppd, 'all_entries', []))} entries)")

    gt = cm.load_ground_truth(repo)
    rows, failed = [], []
    t0 = time.time()
    for mid in ids:
        if mid not in entries:
            continue
        try:
            e_hull = ppd.get_e_above_hull(entries[mid], allow_negative=True)
        except Exception as exc:  # noqa: BLE001 — per-entry audit, record and go on
            failed.append((mid, repr(exc)))
            continue
        rows.append((mid, e_hull, gt.loc[mid, GT_COL]))
    print(f"hull energies for {len(rows)} entries in {time.time() - t0:.1f}s "
          f"({len(failed)} failed)")

    df = pd.DataFrame(rows, columns=["material_id", "recomputed", "published"])
    df["delta_meV"] = (df.recomputed - df.published) * 1e3
    abs_d = df.delta_meV.abs()

    L = [
        "# Layer C (ground truth) — e_above_hull recomputed from the MP phase diagram\n",
        f"Subset: the committed Layer B ids (n={len(ids)}); CSE source `{CSE_FILE}`; "
        f"hull source `{PPD_FILE}` (2023 pickle) unpickled under pymatgen "
        f"{__import__('pymatgen.core', fromlist=['__version__']).__version__}. "
        f"Corrections: entries shipped with adjustments for {n_pre_corrected}/{len(ids)}; "
        + ("MP2020 applied by us to the rest; " if n_pre_corrected < len(ids) else "")
        + f"{len(dropped)} dropped by compatibility processing; "
          f"{len(failed)} hull lookups failed.\n",
        "## Result\n",
        f"- compared: **{len(df)}/{len(ids)}** subset structures",
        f"- median |Δ| = **{abs_d.median():.4f} meV/atom** | p95 = {abs_d.quantile(0.95):.4f} "
        f"| max = {abs_d.max():.4f} meV/atom",
        f"- within 0.1 meV/atom: {(abs_d <= 0.1).mean():.1%} | within 1 meV/atom: "
        f"{(abs_d <= 1).mean():.1%}",
        f"- stable/unstable label (<=0) agreement with published column: "
        f"{((df.recomputed <= 0) == (df.published <= 0)).mean():.1%}",
    ]
    worst = df.reindex(abs_d.sort_values(ascending=False).index).head(10)
    L.append("\n| material_id | published | recomputed | Δ meV/atom |")
    L.append("|---|---|---|---|")
    for _, r in worst.iterrows():
        L.append(f"| {r.material_id} | {r.published:.6f} | {r.recomputed:.6f} "
                 f"| {r.delta_meV:+.4f} |")
    if dropped:
        L.append(f"\nDropped by MP2020 processing: {dropped}")
    if failed:
        L.append(f"\nFailed hull lookups: {failed}")

    out = ROOT / args.out
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L[2:]))
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
