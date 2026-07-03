"""Recompute stored Matbench scores across all local v0.1 submissions."""

from __future__ import annotations

import argparse
import gc
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from matbench_score import (
    MATBENCH_ROOT,
    METADATA_PATH,
    ROOT,
    VALIDATION_PATH,
    load_truth,
    probability_auc,
    read_json,
    score_arrays,
)


BENCHMARKS_DIR = MATBENCH_ROOT / "benchmarks"
REPORT = ROOT / "papers" / "matbench" / "layer_a_all_submission_score_scan.md"
TOL = 1e-12


def prediction_type(values: list[Any]) -> str:
    types = {type(value).__name__ for value in values}
    return next(iter(types)) if len(types) == 1 else ",".join(sorted(types))


def format_float(value: float | None) -> str:
    if value is None:
        return ""
    return f"{value:.12g}"


def score_submission(
    path: Path,
    *,
    metadata: dict[str, Any],
    validation: dict[str, Any],
    truth_cache: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    results = read_json(path)
    rows: list[dict[str, Any]] = []

    for task, task_result in sorted(results.get("tasks", {}).items()):
        if task not in truth_cache:
            truth_cache[task] = load_truth(task, metadata)
            gc.collect()
        task_meta = metadata[task]
        truth_by_id = truth_cache[task]

        for fold_key, fold_result in sorted(task_result["results"].items()):
            expected_ids = validation[task][fold_key]["test"]
            predictions_by_id = fold_result["data"]
            expected_set = set(expected_ids)
            predicted_set = set(predictions_by_id)
            id_match = expected_set == predicted_set
            if id_match:
                y_true = [truth_by_id[mbid] for mbid in expected_ids]
                y_pred = [predictions_by_id[mbid] for mbid in expected_ids]
                recomputed = score_arrays(y_true, y_pred, task_meta["task_type"])
                stored = {k: float(v) for k, v in fold_result["scores"].items()}
                deltas = {
                    metric: abs(stored[metric] - recomputed[metric])
                    for metric in recomputed
                }
                fold_max_delta = max(deltas.values())
                proba_auc = (
                    probability_auc(y_true, y_pred)
                    if task_meta["task_type"] == "classification"
                    else None
                )
                pred_type = prediction_type(y_pred)
                stored_rocauc = stored.get("rocauc")
                stored_balacc = stored.get("balanced_accuracy")
            else:
                missing = sorted(expected_set - predicted_set)[:5]
                extra = sorted(predicted_set - expected_set)[:5]
                fold_max_delta = float("nan")
                proba_auc = None
                pred_type = "id_mismatch"
                stored_rocauc = None
                stored_balacc = None
                deltas = {}
                rows.append(
                    {
                        "submission": path.parent.name,
                        "task": task,
                        "fold": fold_key,
                        "task_type": task_meta["task_type"],
                        "n": len(expected_ids),
                        "prediction_type": pred_type,
                        "id_match": False,
                        "max_delta": fold_max_delta,
                        "worst_metric": "",
                        "stored_rocauc": stored_rocauc,
                        "stored_balacc": stored_balacc,
                        "probability_rocauc": proba_auc,
                        "missing": missing,
                        "extra": extra,
                    }
                )
                continue

            worst_metric = max(deltas, key=deltas.get)
            rows.append(
                {
                    "submission": path.parent.name,
                    "task": task,
                    "fold": fold_key,
                    "task_type": task_meta["task_type"],
                    "n": len(expected_ids),
                    "prediction_type": pred_type,
                    "id_match": True,
                    "max_delta": fold_max_delta,
                    "worst_metric": worst_metric,
                    "stored_rocauc": stored_rocauc,
                    "stored_balacc": stored_balacc,
                    "probability_rocauc": proba_auc,
                    "missing": [],
                    "extra": [],
                }
            )

    return rows


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    submission_tasks = {
        (row["submission"], row["task"])
        for row in rows
    }
    submissions = {row["submission"] for row in rows}
    task_counter = Counter(row["task"] for row in rows if row["fold"] == "fold_0")
    failures = [
        row for row in rows
        if not row["id_match"] or row["max_delta"] > TOL
    ]
    classification = [row for row in rows if row["task_type"] == "classification"]
    rocauc_balacc_equal = sum(
        1
        for row in classification
        if row["stored_rocauc"] is not None
        and row["stored_balacc"] is not None
        and abs(row["stored_rocauc"] - row["stored_balacc"]) <= TOL
    )
    max_delta = max((row["max_delta"] for row in rows if row["id_match"]), default=0.0)
    return {
        "submissions": len(submissions),
        "submission_task_records": len(submission_tasks),
        "folds_checked": len(rows),
        "tasks_seen": dict(sorted(task_counter.items())),
        "max_abs_delta": max_delta,
        "failures": len(failures),
        "classification_folds": len(classification),
        "classification_folds_rocauc_equal_balacc": rocauc_balacc_equal,
    }


def write_report(path: Path, rows: list[dict[str, Any]], summary: dict[str, Any]) -> None:
    by_submission: dict[str, dict[str, Any]] = defaultdict(
        lambda: {"tasks": set(), "folds": 0, "max_delta": 0.0, "failures": 0}
    )
    for row in rows:
        item = by_submission[row["submission"]]
        item["tasks"].add(row["task"])
        item["folds"] += 1
        if row["id_match"]:
            item["max_delta"] = max(item["max_delta"], row["max_delta"])
        if not row["id_match"] or row["max_delta"] > TOL:
            item["failures"] += 1

    worst_rows = sorted(
        [row for row in rows if row["id_match"]],
        key=lambda row: row["max_delta"],
        reverse=True,
    )[:20]
    failures = [
        row for row in rows
        if not row["id_match"] or row["max_delta"] > TOL
    ]

    lines = [
        "# Matbench v0.1 all-submission score scan",
        "",
        f"- Submissions checked: {summary['submissions']}",
        f"- Submission/task records checked: {summary['submission_task_records']}",
        f"- Folds checked: {summary['folds_checked']}",
        f"- Max absolute stored-vs-recomputed score delta: {summary['max_abs_delta']:.3e}",
        f"- Failing folds at tolerance {TOL:.0e}: {summary['failures']}",
        f"- Classification folds checked: {summary['classification_folds']}",
        f"- Classification folds with stored `rocauc == balanced_accuracy`: {summary['classification_folds_rocauc_equal_balacc']}",
        "",
        "## Per-submission summary",
        "",
        "| Submission | Tasks | Folds | Max score delta | Failing folds |",
        "|---|---:|---:|---:|---:|",
    ]
    for submission, item in sorted(by_submission.items()):
        lines.append(
            "| {submission} | {tasks} | {folds} | {max_delta:.3e} | {failures} |".format(
                submission=submission,
                tasks=len(item["tasks"]),
                folds=item["folds"],
                max_delta=item["max_delta"],
                failures=item["failures"],
            )
        )

    lines.extend([
        "",
        "## Task coverage",
        "",
        "| Task | Submission records |",
        "|---|---:|",
    ])
    for task, count in summary["tasks_seen"].items():
        lines.append(f"| {task} | {count} |")

    lines.extend([
        "",
        "## Largest score deltas",
        "",
        "| Submission | Task | Fold | n | Prediction type | Worst metric | Max delta | Stored rocauc | Stored bal. acc. | Probability rocauc |",
        "|---|---|---|---:|---|---|---:|---:|---:|---:|",
    ])
    for row in worst_rows:
        lines.append(
            "| {submission} | {task} | {fold} | {n} | {ptype} | {metric} | {delta:.3e} | {rocauc} | {balacc} | {proba} |".format(
                submission=row["submission"],
                task=row["task"],
                fold=row["fold"].replace("fold_", ""),
                n=row["n"],
                ptype=row["prediction_type"],
                metric=row["worst_metric"],
                delta=row["max_delta"],
                rocauc=format_float(row["stored_rocauc"]),
                balacc=format_float(row["stored_balacc"]),
                proba=format_float(row["probability_rocauc"]),
            )
        )

    lines.extend(["", "## Failures", ""])
    if not failures:
        lines.append("No ID mismatches or score deltas above tolerance.")
    else:
        lines.append("| Submission | Task | Fold | Problem |")
        lines.append("|---|---|---|---|")
        for row in failures:
            problem = (
                f"delta {row['max_delta']:.3e}"
                if row["id_match"]
                else f"id mismatch missing={row['missing']} extra={row['extra']}"
            )
            lines.append(
                f"| {row['submission']} | {row['task']} | {row['fold']} | {problem} |"
            )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--benchmarks-dir", type=Path, default=BENCHMARKS_DIR)
    parser.add_argument("--report", type=Path, default=REPORT)
    parser.add_argument("--limit", type=int, default=0,
                        help="Optional number of submissions to scan for smoke tests.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    metadata = read_json(METADATA_PATH)
    validation = read_json(VALIDATION_PATH)["splits"]
    truth_cache: dict[str, dict[str, Any]] = {}
    rows: list[dict[str, Any]] = []
    results_paths = sorted(args.benchmarks_dir.glob("matbench_v0.1_*/results.json.gz"))
    if args.limit:
        results_paths = results_paths[:args.limit]

    for results_path in results_paths:
        rows.extend(
            score_submission(
                results_path,
                metadata=metadata,
                validation=validation,
                truth_cache=truth_cache,
            )
        )

    summary = summarize(rows)
    write_report(args.report, rows, summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["failures"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
