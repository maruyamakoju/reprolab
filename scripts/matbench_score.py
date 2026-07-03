"""Recompute Matbench v0.1 fold scores from saved prediction artifacts.

This intentionally avoids importing the Matbench package's scoring wrappers. It uses
the released metadata/split JSON plus matminer datasets as the source of targets, and
then mirrors the metric formulas used by Matbench v0.1.
"""

from __future__ import annotations

import argparse
import gzip
import json
import math
from pathlib import Path
from typing import Any

import numpy as np
from matminer.datasets import load_dataset
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    f1_score,
    roc_auc_score,
)

ROOT = Path(__file__).resolve().parent.parent
MATBENCH_ROOT = ROOT / "vendor" / "matbench"
METADATA_PATH = MATBENCH_ROOT / "matbench" / "matbench_v0.1_dataset_metadata.json"
VALIDATION_PATH = MATBENCH_ROOT / "matbench" / "matbench_v0.1_validation.json"

REG_METRICS = ("mae", "rmse", "mape", "max_error")
CLF_METRICS = ("accuracy", "balanced_accuracy", "f1", "rocauc")
FOLD_DIST_METRICS = ("mean", "max", "min", "std")
CLF_THRESH = 0.5


def read_json(path: Path) -> dict[str, Any]:
    if path.suffix == ".gz":
        with gzip.open(path, "rt", encoding="utf-8") as fh:
            return json.load(fh)
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def matbench_ids(dataset_name: str, n_rows: int) -> list[str]:
    n_zeros = math.floor(math.log(n_rows, 10)) + 1
    prefix = dataset_name.replace("matbench", "mb").replace("_", "-")
    return [f"{prefix}-{idx + 1:0{n_zeros}d}" for idx in range(n_rows)]


def load_truth(dataset_name: str, metadata: dict[str, Any]) -> dict[str, Any]:
    df = load_dataset(dataset_name)
    df.index = matbench_ids(dataset_name, len(df))
    return df[metadata[dataset_name]["target"]].to_dict()


def mean_absolute_percentage_error(y_true: list[float], y_pred: list[float]) -> float:
    true = np.asarray(y_true, dtype=float)
    pred = np.asarray(y_pred, dtype=float)
    mask = np.abs(true) > 1e-5
    return float(np.mean(np.fabs((true[mask] - pred[mask]) / true[mask])))


def regression_scores(y_true: list[Any], y_pred: list[Any]) -> dict[str, float]:
    true = np.asarray(y_true, dtype=float)
    pred = np.asarray(y_pred, dtype=float)
    err = true - pred
    return {
        "mae": float(np.mean(np.abs(err))),
        "rmse": float(math.sqrt(np.mean(err**2))),
        "mape": mean_absolute_percentage_error(true.tolist(), pred.tolist()),
        "max_error": float(np.max(np.abs(err))),
    }


def to_probability_labels(values: list[Any]) -> list[float]:
    return [1.0 if bool(v) else 0.0 for v in values]


def to_class_labels(values: list[float]) -> list[bool]:
    return (np.asarray(values, dtype=float) > CLF_THRESH).tolist()


def classification_scores(y_true: list[Any], y_pred: list[Any]) -> dict[str, float]:
    """Mirror matbench.data_ops.score_array, including prediction mutation order."""
    true = [bool(v) for v in y_true]
    pred: list[Any] = list(y_pred)
    computed: dict[str, float] = {}

    for metric in CLF_METRICS:
        if metric == "rocauc":
            roc_true: list[Any] = true
            if isinstance(pred[0], float):
                roc_true = to_probability_labels(true)
            computed[metric] = float(roc_auc_score(roc_true, pred))
        else:
            if isinstance(pred[0], float):
                pred = to_class_labels(pred)
            if metric == "accuracy":
                computed[metric] = float(accuracy_score(true, pred))
            elif metric == "balanced_accuracy":
                computed[metric] = float(balanced_accuracy_score(true, pred))
            elif metric == "f1":
                computed[metric] = float(f1_score(true, pred))
            else:
                raise AssertionError(metric)
    return computed


def probability_auc(y_true: list[Any], y_pred: list[Any]) -> float | None:
    if not y_pred or not isinstance(y_pred[0], float):
        return None
    return float(roc_auc_score([bool(v) for v in y_true], y_pred))


def score_arrays(y_true: list[Any], y_pred: list[Any], task_type: str) -> dict[str, float]:
    if task_type == "regression":
        return regression_scores(y_true, y_pred)
    if task_type == "classification":
        return classification_scores(y_true, y_pred)
    raise ValueError(f"unknown task_type: {task_type}")


def aggregate_folds(fold_scores: list[dict[str, float]]) -> dict[str, dict[str, float]]:
    if not fold_scores:
        return {}
    metrics = fold_scores[0].keys()
    aggregate: dict[str, dict[str, float]] = {}
    for metric in metrics:
        values = np.asarray([fs[metric] for fs in fold_scores], dtype=float)
        aggregate[metric] = {
            op: float(getattr(np, op)(values)) for op in FOLD_DIST_METRICS
        }
    return aggregate


def format_float(value: float | None) -> str:
    if value is None:
        return ""
    return f"{value:.12g}"


def write_report(
    path: Path,
    *,
    results_path: Path,
    rows: list[dict[str, Any]],
    task_aggregates: dict[str, dict[str, dict[str, float]]],
    max_abs_delta: float,
) -> None:
    lines = [
        "# Matbench v0.1 score recomputation",
        "",
        f"- Results artifact: `{results_path.as_posix()}`",
        f"- Fold scores checked: {len(rows)}",
        f"- Max absolute stored-vs-recomputed score delta: {max_abs_delta:.3e}",
        "",
        "## Fold checks",
        "",
        "| Task | Fold | n | Prediction type | Max score delta | Stored rocauc | Probability rocauc |",
        "|---|---:|---:|---|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            "| {task} | {fold} | {n} | {pred_type} | {max_delta:.3e} | {rocauc} | {proba_rocauc} |".format(
                task=row["task"],
                fold=row["fold"],
                n=row["n"],
                pred_type=row["pred_type"],
                max_delta=row["max_delta"],
                rocauc=format_float(row.get("stored_rocauc")),
                proba_rocauc=format_float(row.get("probability_rocauc")),
            )
        )

    lines.extend(["", "## Recomputed fold aggregates", ""])
    for task, metrics in task_aggregates.items():
        lines.extend([f"### {task}", ""])
        lines.append("| Metric | mean | max | min | std |")
        lines.append("|---|---:|---:|---:|---:|")
        for metric, values in metrics.items():
            lines.append(
                "| {metric} | {mean} | {max_} | {min_} | {std} |".format(
                    metric=metric,
                    mean=format_float(values["mean"]),
                    max_=format_float(values["max"]),
                    min_=format_float(values["min"]),
                    std=format_float(values["std"]),
                )
            )
        lines.append("")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--results",
        type=Path,
        default=MATBENCH_ROOT / "benchmarks" / "matbench_v0.1_rf" / "results.json.gz",
        help="Path to a Matbench results.json or results.json.gz artifact.",
    )
    parser.add_argument(
        "--tasks",
        nargs="+",
        default=["matbench_steels", "matbench_expt_is_metal"],
        help="Task names to check. Use 'all' to check every task in the artifact.",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=ROOT / "papers" / "matbench" / "layer_a_score_recompute.md",
        help="Markdown report path.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    metadata = read_json(METADATA_PATH)
    validation = read_json(VALIDATION_PATH)["splits"]
    results = read_json(args.results)

    tasks = list(results["tasks"]) if args.tasks == ["all"] else args.tasks
    rows: list[dict[str, Any]] = []
    task_aggregates: dict[str, dict[str, dict[str, float]]] = {}
    max_abs_delta = 0.0

    for task in tasks:
        task_meta = metadata[task]
        truth_by_id = load_truth(task, metadata)
        fold_scores_for_aggregate: list[dict[str, float]] = []

        for fold_key, fold_result in sorted(results["tasks"][task]["results"].items()):
            expected_ids = validation[task][fold_key]["test"]
            predictions_by_id = fold_result["data"]
            expected_set = set(expected_ids)
            predicted_set = set(predictions_by_id)
            if expected_set != predicted_set:
                missing = sorted(expected_set - predicted_set)[:5]
                extra = sorted(predicted_set - expected_set)[:5]
                raise ValueError(
                    f"{task} {fold_key}: prediction ids do not match split ids; "
                    f"missing={missing}, extra={extra}"
                )

            y_true = [truth_by_id[mbid] for mbid in expected_ids]
            y_pred = [predictions_by_id[mbid] for mbid in expected_ids]
            recomputed = score_arrays(y_true, y_pred, task_meta["task_type"])
            stored = {k: float(v) for k, v in fold_result["scores"].items()}
            deltas = {
                metric: abs(stored[metric] - recomputed[metric])
                for metric in recomputed
            }
            fold_max_delta = max(deltas.values())
            max_abs_delta = max(max_abs_delta, fold_max_delta)
            fold_scores_for_aggregate.append(recomputed)

            proba_auc = (
                probability_auc(y_true, y_pred)
                if task_meta["task_type"] == "classification"
                else None
            )
            rows.append(
                {
                    "task": task,
                    "fold": fold_key.replace("fold_", ""),
                    "n": len(expected_ids),
                    "pred_type": type(y_pred[0]).__name__,
                    "max_delta": fold_max_delta,
                    "stored_rocauc": stored.get("rocauc"),
                    "probability_rocauc": proba_auc,
                }
            )

        task_aggregates[task] = aggregate_folds(fold_scores_for_aggregate)

    write_report(
        args.report,
        results_path=args.results,
        rows=rows,
        task_aggregates=task_aggregates,
        max_abs_delta=max_abs_delta,
    )
    print(
        json.dumps(
            {
                "results": str(args.results),
                "tasks": tasks,
                "folds_checked": len(rows),
                "max_abs_delta": max_abs_delta,
                "report": str(args.report),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0 if max_abs_delta < 1e-12 else 1


if __name__ == "__main__":
    raise SystemExit(main())
