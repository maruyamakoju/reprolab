"""Map Matbench v0.1 leaderboard adjacent gaps against fold-score variation."""

from __future__ import annotations

import argparse
import gzip
import json
import math
from collections import defaultdict
from pathlib import Path
from statistics import median
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parent.parent
MATBENCH_ROOT = ROOT / "vendor" / "matbench"
BENCHMARKS_DIR = MATBENCH_ROOT / "benchmarks"
METADATA_PATH = MATBENCH_ROOT / "matbench" / "matbench_v0.1_dataset_metadata.json"
REPORT = ROOT / "papers" / "matbench" / "layer_c_leaderboard_resolution.md"
PRIMARY_METRIC = {"regression": "mae", "classification": "rocauc"}


def read_json(path: Path) -> dict[str, Any]:
    if path.suffix == ".gz":
        with gzip.open(path, "rt", encoding="utf-8") as fh:
            return json.load(fh)
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def format_float(value: float) -> str:
    if math.isinf(value):
        return "inf"
    return f"{value:.6g}"


def score_rows(benchmarks_dir: Path, metadata: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for results_path in sorted(benchmarks_dir.glob("matbench_v0.1_*/results.json.gz")):
        submission = results_path.parent.name
        results = read_json(results_path)
        for task, task_result in sorted(results.get("tasks", {}).items()):
            task_type = metadata[task]["task_type"]
            metric = PRIMARY_METRIC[task_type]
            fold_scores = [
                float(fold_result["scores"][metric])
                for _, fold_result in sorted(task_result["results"].items())
            ]
            if len(fold_scores) != 5:
                raise ValueError(f"{submission} {task}: expected 5 folds, got {len(fold_scores)}")
            mean_score = float(np.mean(fold_scores))
            fold_std = float(np.std(fold_scores, ddof=1))
            rows.append(
                {
                    "submission": submission,
                    "task": task,
                    "task_type": task_type,
                    "metric": metric,
                    "fold_scores": fold_scores,
                    "mean": mean_score,
                    "fold_std": fold_std,
                }
            )
    return rows


def adjacent_pairs(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
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
            if task_type == "classification":
                fold_diffs = better_scores - worse_scores
                mean_gap = better["mean"] - worse["mean"]
            else:
                fold_diffs = worse_scores - better_scores
                mean_gap = worse["mean"] - better["mean"]
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
                    "mean_gap": float(mean_gap),
                    "fold_se": fold_se,
                    "gap_to_se": gap_to_se,
                    "better_fold_std": better["fold_std"],
                    "worse_fold_std": worse["fold_std"],
                }
            )
    return pairs


def summarize_by_task(rows: list[dict[str, Any]], pairs: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows_by_task: dict[str, list[dict[str, Any]]] = defaultdict(list)
    pairs_by_task: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        rows_by_task[row["task"]].append(row)
    for pair in pairs:
        pairs_by_task[pair["task"]].append(pair)

    summary: list[dict[str, Any]] = []
    for task, task_pairs in sorted(pairs_by_task.items()):
        finite_ratios = [pair["gap_to_se"] for pair in task_pairs if math.isfinite(pair["gap_to_se"])]
        gaps = [pair["mean_gap"] for pair in task_pairs]
        task_rows = rows_by_task[task]
        summary.append(
            {
                "task": task,
                "task_type": task_rows[0]["task_type"],
                "metric": task_rows[0]["metric"],
                "entries": len(task_rows),
                "adjacent_pairs": len(task_pairs),
                "exact_ties": sum(1 for pair in task_pairs if pair["mean_gap"] == 0),
                "within_1se": sum(1 for pair in task_pairs if pair["gap_to_se"] <= 1),
                "within_2se": sum(1 for pair in task_pairs if pair["gap_to_se"] <= 2),
                "min_gap": min(gaps),
                "median_gap": float(median(gaps)),
                "min_gap_to_se": min(finite_ratios) if finite_ratios else float("inf"),
            }
        )
    return summary


def write_report(path: Path, rows: list[dict[str, Any]], pairs: list[dict[str, Any]]) -> None:
    task_summary = summarize_by_task(rows, pairs)
    total_pairs = len(pairs)
    exact_ties = sum(1 for pair in pairs if pair["mean_gap"] == 0)
    within_1se = sum(1 for pair in pairs if pair["gap_to_se"] <= 1)
    within_2se = sum(1 for pair in pairs if pair["gap_to_se"] <= 2)
    classification_pairs = [pair for pair in pairs if pair["task_type"] == "classification"]
    regression_pairs = [pair for pair in pairs if pair["task_type"] == "regression"]
    close_pairs = sorted(pairs, key=lambda pair: (pair["gap_to_se"], pair["mean_gap"]))[:25]
    raw_close_pairs = sorted(pairs, key=lambda pair: pair["mean_gap"])[:25]

    lines = [
        "# Matbench v0.1 leaderboard resolution map",
        "",
        "This uses stored fold scores from public `results.json.gz` artifacts. For each task, submissions are ranked by the primary leaderboard metric (`mae` for regression, stored `rocauc` for classification), then adjacent mean gaps are compared with a fold-level standard-error proxy from the five paired fold-score differences.",
        "",
        "Classification caveat: the stored `rocauc` values in these artifacts behave as thresholded-label AUC / balanced accuracy for the checked records, as documented in the classification probe.",
        "",
        f"- Submission-task rows ranked: {len(rows)}",
        f"- Tasks ranked: {len(task_summary)}",
        f"- Adjacent pairs: {total_pairs}",
        f"- Exact adjacent ties: {exact_ties}",
        f"- Adjacent gaps <= 1 fold-SE proxy: {within_1se}",
        f"- Adjacent gaps <= 2 fold-SE proxy: {within_2se}",
        f"- Regression adjacent pairs: {len(regression_pairs)}",
        f"- Classification adjacent pairs: {len(classification_pairs)}",
        "",
        "## Per-task resolution",
        "",
        "| Task | Type | Metric | Entries | Adjacent pairs | Exact ties | <=1 SE | <=2 SE | Min gap | Median gap | Min gap / SE |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for item in task_summary:
        lines.append(
            "| {task} | {task_type} | {metric} | {entries} | {pairs} | {ties} | {one} | {two} | {min_gap} | {median_gap} | {min_ratio} |".format(
                task=item["task"],
                task_type=item["task_type"],
                metric=item["metric"],
                entries=item["entries"],
                pairs=item["adjacent_pairs"],
                ties=item["exact_ties"],
                one=item["within_1se"],
                two=item["within_2se"],
                min_gap=format_float(item["min_gap"]),
                median_gap=format_float(item["median_gap"]),
                min_ratio=format_float(item["min_gap_to_se"]),
            )
        )

    lines.extend([
        "",
        "## Closest adjacent pairs by fold-SE proxy",
        "",
        "| Task | Rank | Better | Worse | Metric | Better mean | Worse mean | Gap | Fold-SE proxy | Gap / SE |",
        "|---|---:|---|---|---|---:|---:|---:|---:|---:|",
    ])
    for pair in close_pairs:
        lines.append(
            "| {task} | {rank} | {better} | {worse} | {metric} | {better_mean} | {worse_mean} | {gap} | {se} | {ratio} |".format(
                task=pair["task"],
                rank=pair["rank"],
                better=pair["better"],
                worse=pair["worse"],
                metric=pair["metric"],
                better_mean=format_float(pair["better_mean"]),
                worse_mean=format_float(pair["worse_mean"]),
                gap=format_float(pair["mean_gap"]),
                se=format_float(pair["fold_se"]),
                ratio=format_float(pair["gap_to_se"]),
            )
        )

    lines.extend([
        "",
        "## Smallest raw adjacent gaps",
        "",
        "| Task | Rank | Better | Worse | Metric | Gap | Gap / SE |",
        "|---|---:|---|---|---|---:|---:|",
    ])
    for pair in raw_close_pairs:
        lines.append(
            "| {task} | {rank} | {better} | {worse} | {metric} | {gap} | {ratio} |".format(
                task=pair["task"],
                rank=pair["rank"],
                better=pair["better"],
                worse=pair["worse"],
                metric=pair["metric"],
                gap=format_float(pair["mean_gap"]),
                ratio=format_float(pair["gap_to_se"]),
            )
        )

    lines.extend([
        "",
        "## Interpretation",
        "",
        "This is a leaderboard-resolution screen, not a formal significance test. It shows where adjacent point estimates are narrow relative to fold-to-fold metric variation. Exact ties and gaps below one fold-SE proxy should be treated as unresolved without a stronger paired uncertainty analysis.",
    ])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--benchmarks-dir", type=Path, default=BENCHMARKS_DIR)
    parser.add_argument("--report", type=Path, default=REPORT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    metadata = read_json(METADATA_PATH)
    rows = score_rows(args.benchmarks_dir, metadata)
    pairs = adjacent_pairs(rows)
    write_report(args.report, rows, pairs)
    summary = {
        "submission_task_rows": len(rows),
        "tasks": len({row["task"] for row in rows}),
        "adjacent_pairs": len(pairs),
        "exact_adjacent_ties": sum(1 for pair in pairs if pair["mean_gap"] == 0),
        "adjacent_gaps_lte_1se": sum(1 for pair in pairs if pair["gap_to_se"] <= 1),
        "adjacent_gaps_lte_2se": sum(1 for pair in pairs if pair["gap_to_se"] <= 2),
        "report": str(args.report),
    }
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
