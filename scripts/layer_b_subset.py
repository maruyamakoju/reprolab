"""Generate the deterministic Layer B smoke subset (see layer_b_plan.md §2).

Universe: WBM unique_prototypes rows from the bundled ground truth.
Selection: sort by material_id (lexicographic), then sample(n=500, random_state=42).
Pre-smoke = the first 20 rows of the written CSV, in sampled order.

Writes papers/matbench-discovery/layer_b_subset.csv (committed artifact) and prints
summary stats for run_log.md.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
EACH_TRUE = "e_above_hull_mp2020_corrected_ppd_mp"
UNIQ_PROTO = "unique_prototype"
ID_COL = "material_id"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default="vendor/matbench-discovery")
    ap.add_argument("--n", type=int, default=500)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out", default="papers/matbench-discovery/layer_b_subset.csv")
    args = ap.parse_args()

    gt_path = ROOT / args.repo / "data" / "wbm" / "2023-12-13-wbm-summary.csv.gz"
    df = pd.read_csv(gt_path)
    uniq = df[df[UNIQ_PROTO]].sort_values(ID_COL)
    sample = uniq.sample(n=args.n, random_state=args.seed)

    out = ROOT / args.out
    cols = [ID_COL, "formula", EACH_TRUE]
    sample[cols].to_csv(out, index=False)

    stable = (sample[EACH_TRUE] <= 0).mean()
    stable_base = (uniq[EACH_TRUE] <= 0).mean()
    pre = sample[ID_COL].head(20).tolist()
    print(f"universe: {len(uniq):,} unique_prototypes rows (of {len(df):,} total)")
    print(f"sampled: n={len(sample)} seed={args.seed} -> {out.relative_to(ROOT)}")
    print(f"stable fraction: subset {stable:.3f} vs universe {stable_base:.3f}")
    print(f"pre-smoke (first 20 ids): {pre}")


if __name__ == "__main__":
    main()
