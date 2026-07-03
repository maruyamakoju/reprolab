"""Fold-level bootstrap screen for close Matbench v0.1 leaderboard pairs."""

from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Any

import numpy as np

from matbench_leaderboard_resolution import (
    BENCHMARKS_DIR,
    METADATA_PATH,
    REPORT as RESOLUTION_REPORT,
    format_float,
    read_json,
    score_rows,
)


ROOT = Path(__file__).resolve().parent.parent
REPORT = ROOT / "papers" / "matbench" / "layer_c_fold_bootstrap.md"


def adjacent_pairs_with_diffs(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_task: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_task[row["task"]].append(row)

    pairs: list[dict[str, Any]] = []
    for task, task_rows in sorted(by_task.items()):
        task_type = task_rows[0]["task_type"]
        reverse = task_type == "classification"
        ranked = sorted(task_rows, key=lambda row: row["mean"], reverse=reverse)
        for rank, (better, worse) in enumerate(zip(ranked, ranked[1:]), start=1):
            better_scores = np.asarray(better["fold_scores"], dtype=float)
            worse_scores = np.asarray(worse["fold_scores"], dtype=float)
            fold_diffs = better_scores - worse_scores if task_type == "classification" else worse_scores - better_scores
            mean_gap = float(np.mean(fold_diffs))
            fold_se = float(np.std(fold_diffs, ddof=1) / math.sqrt(len(fold_diffs)))
            if mean_gap == 0 and fold_se == 0:
                gap_to_se = 0.0
            elif fold_se == 0:
                gap_to_se = float("inf")
            else:
                gap_to_se = float(mean_gap / fold_se)
            pairs.append(
                {
                    "task": task,
                    "task_type": task_type,
                    "metric": better["metric"],
                    "rank": rank,
                    "better": better["submission"],
                    "worse": worse["submission"],
                    "better_mean": better["mean"],
                    "worse_mean": worse["mean"],
                    "mean_gap": mean_gap,
                    "fold_se": fold_se,
                    "gap_to_se": gap_to_se,
                    "fold_diffs": fold_diffs,
                }
            )
    return pairs


def bootstrap_pair(pair: dict[str, Any], *, draws: int, rng: np.random.Generator) -> dict[str, Any]:
    fold_diffs = np.asarray(pair["fold_diffs"], dtype=float)
    sample_idx = rng.integers(0, len(fold_diffs), size=(draws, len(fold_diffs)))
    means = fold_diffs[sample_idx].mean(axis=1)
    ci_low, ci_high = np.quantile(means, [0.025, 0.975])
    p_gap_lte_zero = float(np.mean(means <= 0))
    return {
        **{key: value for key, value in pair.items() if key != "fold_diffs"},
        "ci_low": float(ci_low),
        "ci_high": float(ci_high),
        "p_gap_lte_zero": p_gap_lte_zero,
        "ci_includes_zero": bool(ci_low <= 0 <= ci_high),
    }


def write_report(path: Path, results: list[dict[str, Any]], *, draws: int, seed: int) -> None:
    ci_includes_zero = sum(1 for row in results if row["ci_includes_zero"])
    p_ge_05 = sum(1 for row in results if row["p_gap_lte_zero"] >= 0.05)
    exact_ties = sum(1 for row in results if row["mean_gap"] == 0)
    lines = [
        "# Matbench v0.1 fold-bootstrap adjacent-pair screen",
        "",
        "This is a follow-up to `layer_c_leaderboard_resolution.md`. It takes the closest adjacent leaderboard pairs by gap/fold-SE proxy, then bootstraps the five paired fold-score differences. Positive differences mean the higher-ranked submission remains better under the task's primary metric.",
        "",
        "This is a lightweight fold-level uncertainty screen, not a formal statistical test. It has only five folds per pair, and classification uses stored `rocauc`, which behaves as thresholded-label AUC / balanced accuracy for the checked records.",
        "",
        f"- Adjacent pairs checked: {len(results)}",
        f"- Bootstrap draws per pair: {draws}",
        f"- RNG seed: {seed}",
        f"- 95% bootstrap CIs including zero: {ci_includes_zero}",
        f"- P(bootstrapped gap <= 0) >= 0.05: {p_ge_05}",
        f"- Exact adjacent ties in checked set: {exact_ties}",
        "",
        "## Pair results",
        "",
        "| Task | Rank | Better | Worse | Metric | Gap | Gap / SE | CI low | CI high | P(gap <= 0) | CI includes 0 |",
        "|---|---:|---|---|---|---:|---:|---:|---:|---:|---|",
    ]
    for row in results:
        lines.append(
            "| {task} | {rank} | {better} | {worse} | {metric} | {gap} | {ratio} | {ci_low} | {ci_high} | {p} | {includes} |".format(
                task=row["task"],
                rank=row["rank"],
                better=row["better"],
                worse=row["worse"],
                metric=row["metric"],
                gap=format_float(row["mean_gap"]),
                ratio=format_float(row["gap_to_se"]),
                ci_low=format_float(row["ci_low"]),
                ci_high=format_float(row["ci_high"]),
                p=format_float(row["p_gap_lte_zero"]),
                includes="yes" if row["ci_includes_zero"] else "no",
            )
        )
    lines.extend([
        "",
        "## Interpretation",
        "",
        "For these closest adjacent pairs, a CI crossing zero means the five-fold score pattern does not stably separate the two neighboring submissions under this coarse fold-bootstrap screen. Exact ties are deterministic ties in the stored fold scores.",
    ])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--benchmarks-dir", type=Path, default=BENCHMARKS_DIR)
    parser.add_argument("--report", type=Path, default=REPORT)
    parser.add_argument("--pairs", type=int, default=25)
    parser.add_argument("--draws", type=int, default=20000)
    parser.add_argument("--seed", type=int, default=0)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    metadata = read_json(METADATA_PATH)
    rows = score_rows(args.benchmarks_dir, metadata)
    pairs = adjacent_pairs_with_diffs(rows)
    closest = sorted(pairs, key=lambda pair: (pair["gap_to_se"], pair["mean_gap"]))[: args.pairs]
    rng = np.random.default_rng(args.seed)
    results = [bootstrap_pair(pair, draws=args.draws, rng=rng) for pair in closest]
    write_report(args.report, results, draws=args.draws, seed=args.seed)
    summary = {
        "pairs_checked": len(results),
        "draws": args.draws,
        "ci_includes_zero": sum(1 for row in results if row["ci_includes_zero"]),
        "p_gap_lte_zero_gte_0_05": sum(1 for row in results if row["p_gap_lte_zero"] >= 0.05),
        "exact_adjacent_ties": sum(1 for row in results if row["mean_gap"] == 0),
        "report": str(args.report),
        "resolution_report": str(RESOLUTION_REPORT),
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
