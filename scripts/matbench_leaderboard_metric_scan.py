"""Inspect Matbench classification leaderboard tables for displayed metric fields."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
MATBENCH_ROOT = ROOT / "vendor" / "matbench"
METADATA_PATH = MATBENCH_ROOT / "matbench" / "matbench_v0.1_dataset_metadata.json"
LEADERBOARD_DIR = MATBENCH_ROOT / "docs_src" / "Leaderboards Per-Task"


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def clean_cell(value: str) -> str:
    value = value.strip().replace("**", "")
    match = re.match(r"\[(?P<label>.+?)\]\(.+?\)", value)
    return match.group("label") if match else value


def parse_float_cell(value: str) -> float:
    return float(clean_cell(value))


def parse_table(path: Path) -> list[dict[str, Any]]:
    lines = path.read_text(encoding="utf-8").splitlines()
    header_idx = next(
        idx for idx, line in enumerate(lines) if line.startswith("| algorithm |")
    )
    headers = [cell.strip() for cell in lines[header_idx].strip("|").split("|")]
    rows: list[dict[str, Any]] = []
    for line in lines[header_idx + 2 :]:
        if not line.startswith("|"):
            break
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        record = dict(zip(headers, cells))
        rows.append(
            {
                "algorithm": clean_cell(record["algorithm"]),
                "mean_rocauc": parse_float_cell(record["mean rocauc"]),
                "std_rocauc": parse_float_cell(record["std rocauc"]),
                "mean_f1": parse_float_cell(record["mean f1"]),
                "mean_balanced_accuracy": parse_float_cell(
                    record["mean balanced_accuracy"]
                ),
            }
        )
    return rows


def write_report(path: Path, rows: list[dict[str, Any]], summary: dict[str, Any]) -> None:
    lines = [
        "# Matbench v0.1 classification leaderboard metric scan",
        "",
        f"- Classification leaderboard tables scanned: {summary['tasks']}",
        f"- Displayed algorithm rows scanned: {summary['rows']}",
        f"- Rows where displayed mean rocauc differs from mean balanced_accuracy: {summary['displayed_rocauc_differs_from_balacc']}",
        "",
        "| Task | Algorithm | mean rocauc | mean balanced_accuracy | displayed delta |",
        "|---|---|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            "| {task} | {algorithm} | {mean_rocauc:.4f} | {mean_balanced_accuracy:.4f} | {delta:.4f} |".format(
                task=row["task"],
                algorithm=row["algorithm"],
                mean_rocauc=row["mean_rocauc"],
                mean_balanced_accuracy=row["mean_balanced_accuracy"],
                delta=row["mean_rocauc"] - row["mean_balanced_accuracy"],
            )
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--metadata", type=Path, default=METADATA_PATH)
    parser.add_argument("--leaderboard-dir", type=Path, default=LEADERBOARD_DIR)
    parser.add_argument(
        "--report",
        type=Path,
        default=ROOT / "papers" / "matbench" / "classification_leaderboard_metric_scan.md",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    metadata = read_json(args.metadata)
    classification_tasks = [
        task for task, meta in metadata.items() if meta["task_type"] == "classification"
    ]
    rows: list[dict[str, Any]] = []
    for task in classification_tasks:
        path = args.leaderboard_dir / f"matbench_v0.1_{task}.md"
        for row in parse_table(path):
            row["task"] = task
            rows.append(row)
    summary = {
        "tasks": len(classification_tasks),
        "rows": len(rows),
        "displayed_rocauc_differs_from_balacc": sum(
            1
            for row in rows
            if abs(row["mean_rocauc"] - row["mean_balanced_accuracy"]) > 0
        ),
    }
    write_report(args.report, rows, summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
