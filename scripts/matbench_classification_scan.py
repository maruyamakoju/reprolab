"""Scan Matbench v0.1 submissions for classification prediction value types."""

from __future__ import annotations

import argparse
import gzip
import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
MATBENCH_ROOT = ROOT / "vendor" / "matbench"
METADATA_PATH = MATBENCH_ROOT / "matbench" / "matbench_v0.1_dataset_metadata.json"
BENCHMARKS_DIR = MATBENCH_ROOT / "benchmarks"


def read_json(path: Path) -> dict[str, Any]:
    if path.suffix == ".gz":
        with gzip.open(path, "rt", encoding="utf-8") as fh:
            return json.load(fh)
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def value_type(value: Any) -> str:
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, float):
        return "float"
    if isinstance(value, int):
        return "int"
    return type(value).__name__


def classify_counter(counter: Counter[str]) -> str:
    present = {k for k, v in counter.items() if v}
    if present == {"bool"}:
        return "all_bool"
    if present == {"float"}:
        return "all_float"
    return "mixed_" + "_".join(sorted(present))


def format_float(value: float | None) -> str:
    if value is None:
        return ""
    return f"{value:.12g}"


def scan_submission(
    submission_dir: Path, classification_tasks: list[str]
) -> list[dict[str, Any]]:
    results_path = submission_dir / "results.json.gz"
    if not results_path.exists():
        return []
    data = read_json(results_path)
    rows: list[dict[str, Any]] = []
    for task in classification_tasks:
        if task not in data["tasks"]:
            continue

        counter: Counter[str] = Counter()
        min_float: float | None = None
        max_float: float | None = None
        max_rocauc_balacc_delta = 0.0
        n_values = 0

        for fold_result in data["tasks"][task]["results"].values():
            values = list(fold_result["data"].values())
            n_values += len(values)
            counter.update(value_type(v) for v in values)
            floats = [float(v) for v in values if isinstance(v, float)]
            if floats:
                fold_min = min(floats)
                fold_max = max(floats)
                min_float = fold_min if min_float is None else min(min_float, fold_min)
                max_float = fold_max if max_float is None else max(max_float, fold_max)
            scores = fold_result.get("scores", {})
            if "rocauc" in scores and "balanced_accuracy" in scores:
                max_rocauc_balacc_delta = max(
                    max_rocauc_balacc_delta,
                    abs(float(scores["rocauc"]) - float(scores["balanced_accuracy"])),
                )

        rows.append(
            {
                "submission": submission_dir.name,
                "task": task,
                "kind": classify_counter(counter),
                "n": n_values,
                "bool": counter["bool"],
                "float": counter["float"],
                "int": counter["int"],
                "other": n_values - counter["bool"] - counter["float"] - counter["int"],
                "min_float": min_float,
                "max_float": max_float,
                "max_rocauc_balacc_delta": max_rocauc_balacc_delta,
            }
        )
    return rows


def write_report(path: Path, rows: list[dict[str, Any]], summary: dict[str, Any]) -> None:
    lines = [
        "# Matbench v0.1 classification prediction-type scan",
        "",
        f"- Submission/task records scanned: {len(rows)}",
        f"- All-bool records: {summary['all_bool']}",
        f"- All-float records: {summary['all_float']}",
        f"- Mixed-type records: {summary['mixed']}",
        f"- Records where stored ROC-AUC differs from balanced accuracy: {summary['rocauc_differs_from_balacc']}",
        "",
        "| Submission | Task | Kind | n | bool | float | min float | max float | max abs rocauc-bal_acc |",
        "|---|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            "| {submission} | {task} | {kind} | {n} | {bool} | {float} | {min_float} | {max_float} | {delta} |".format(
                submission=row["submission"],
                task=row["task"],
                kind=row["kind"],
                n=row["n"],
                bool=row["bool"],
                float=row["float"],
                min_float=format_float(row["min_float"]),
                max_float=format_float(row["max_float"]),
                delta=f"{row['max_rocauc_balacc_delta']:.3e}",
            )
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--benchmarks-dir", type=Path, default=BENCHMARKS_DIR)
    parser.add_argument("--metadata", type=Path, default=METADATA_PATH)
    parser.add_argument(
        "--report",
        type=Path,
        default=ROOT / "papers" / "matbench" / "classification_prediction_scan.md",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    metadata = read_json(args.metadata)
    classification_tasks = [
        task for task, meta in metadata.items() if meta["task_type"] == "classification"
    ]
    rows: list[dict[str, Any]] = []
    for submission_dir in sorted(args.benchmarks_dir.glob("matbench_v0.1_*")):
        rows.extend(scan_submission(submission_dir, classification_tasks))

    summary = {
        "records": len(rows),
        "all_bool": sum(1 for row in rows if row["kind"] == "all_bool"),
        "all_float": sum(1 for row in rows if row["kind"] == "all_float"),
        "mixed": sum(1 for row in rows if row["kind"].startswith("mixed")),
        "rocauc_differs_from_balacc": sum(
            1 for row in rows if row["max_rocauc_balacc_delta"] > 1e-15
        ),
    }
    write_report(args.report, rows, summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
