"""Inventory Matbench v0.1 leaderboard submission artifacts."""

from __future__ import annotations

import argparse
import gzip
import json
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
BENCHMARKS = ROOT / "vendor" / "matbench" / "benchmarks"
REPORT = ROOT / "papers" / "matbench" / "source_artifact_inventory.md"

SOURCE_EXTS = {".py", ".ipynb", ".sh", ".yml", ".yaml", ".txt", ".md"}
MODEL_EXTS = {".pkl", ".joblib", ".h5", ".pt", ".pth", ".ckpt", ".json"}
KEYWORDS = {
    "seed": ("random_state", "np.random.seed", "seed=", "seed "),
    "fit": (".fit(", "fit("),
    "predict": (".predict(", "predict("),
    "pickle": ("pickle", "joblib"),
    "external_repo": ("github.com", "git clone"),
}


def read_json(path: Path) -> dict[str, Any]:
    if path.suffix == ".gz":
        with gzip.open(path, "rt", encoding="utf-8") as fh:
            return json.load(fh)
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def text_for_scan(path: Path) -> str:
    if path.suffix.lower() == ".ipynb":
        try:
            notebook = json.loads(path.read_text(encoding="utf-8", errors="ignore"))
        except json.JSONDecodeError:
            return ""
        cells = notebook.get("cells", [])
        return "\n".join(
            "".join(cell.get("source", []))
            for cell in cells
            if cell.get("cell_type") in {"code", "markdown"}
        )
    return path.read_text(encoding="utf-8", errors="ignore")


def summarize_submission(path: Path) -> dict[str, Any]:
    files = [p for p in path.iterdir() if p.is_file()]
    info_path = path / "info.json"
    results_path = path / "results.json.gz"
    info = read_json(info_path) if info_path.exists() else {}
    results = read_json(results_path) if results_path.exists() else {}
    tasks = sorted(results.get("tasks", {}))

    source_files = [
        p for p in files
        if p.name not in {"info.json", "results.json.gz"} and p.suffix.lower() in SOURCE_EXTS
    ]
    model_files = [
        p for p in files
        if p.name not in {"info.json", "results.json.gz"} and p.suffix.lower() in MODEL_EXTS
    ]

    scan_text = "\n".join(text_for_scan(p) for p in source_files if p.suffix.lower() in SOURCE_EXTS)
    keyword_hits = {
        name: any(token.lower() in scan_text.lower() for token in tokens)
        for name, tokens in KEYWORDS.items()
    }
    requirements = info.get("requirements", {})
    python_reqs = requirements.get("python", []) if isinstance(requirements, dict) else []

    return {
        "name": path.name,
        "algorithm": info.get("algorithm", ""),
        "tasks": tasks,
        "task_count": len(tasks),
        "source_files": [p.name for p in sorted(source_files)],
        "model_files": [p.name for p in sorted(model_files)],
        "has_run_py": any(p.name.lower() == "run.py" for p in source_files),
        "has_notebook": any(p.suffix.lower() == ".ipynb" for p in source_files),
        "has_pickle_or_joblib": any(p.suffix.lower() in {".pkl", ".joblib"} for p in model_files),
        "python_requirements": python_reqs,
        "keyword_hits": keyword_hits,
        "notes": info.get("notes", ""),
    }


def disposition(row: dict[str, Any]) -> str:
    req_text = " ".join(str(x).lower() for x in row["python_requirements"])
    source_text = " ".join(row["source_files"]).lower()
    if row["has_pickle_or_joblib"] and row["task_count"] <= 1:
        return "best bounded replay candidate"
    if "autosklearn" in req_text or "auto-sklearn" in req_text:
        return "dependency-conflicting AutoML runner"
    if "tensorflow" in req_text or "torch" in req_text or "kgcnn" in req_text:
        return "heavy neural dependency path"
    if "modnet" in req_text or "modnet" in source_text:
        return "external/heavy MODNet path"
    if row["has_run_py"]:
        return "source runner present; inspect manually"
    if row["has_notebook"]:
        return "notebook-only source"
    return "artifact-only or unclear source path"


def write_report(path: Path, rows: list[dict[str, Any]]) -> None:
    dispositions = Counter(row["disposition"] for row in rows)
    source_counts = Counter()
    for row in rows:
        if row["has_run_py"]:
            source_counts["run.py"] += 1
        if row["has_notebook"]:
            source_counts["notebook"] += 1
        if row["has_pickle_or_joblib"]:
            source_counts["pickle_or_joblib"] += 1

    lines = [
        "# Matbench v0.1 source artifact inventory",
        "",
        f"- Submission directories scanned: {len(rows)}",
        f"- Direct `run.py` files: {source_counts['run.py']}",
        f"- Notebook sources: {source_counts['notebook']}",
        f"- Pickle/joblib model artifacts: {source_counts['pickle_or_joblib']}",
        "",
        "## Disposition counts",
        "",
        "| Disposition | Count |",
        "|---|---:|",
    ]
    for name, count in sorted(dispositions.items()):
        lines.append(f"| {name} | {count} |")

    lines.extend([
        "",
        "## Submission inventory",
        "",
        "| Submission | Algorithm | Tasks | Source artifacts | Model artifacts | Signals | Disposition |",
        "|---|---|---:|---|---|---|---|",
    ])
    for row in rows:
        signals = []
        for name, hit in row["keyword_hits"].items():
            if hit:
                signals.append(name)
        lines.append(
            "| {name} | {algorithm} | {task_count} | {source} | {models} | {signals} | {disp} |".format(
                name=row["name"],
                algorithm=str(row["algorithm"]).replace("|", "/"),
                task_count=row["task_count"],
                source=", ".join(row["source_files"]) or "",
                models=", ".join(row["model_files"]) or "",
                signals=", ".join(signals) or "",
                disp=row["disposition"],
            )
        )

    lines.extend([
        "",
        "## Interpretation",
        "",
        "`matbench_v0.1_TPOT` stands out as the best bounded Layer B target because it has one small task, a notebook, a submitted helper, and a pickled pipeline artifact. Many other submissions are either notebook-only without saved fold-level models, full-run AutoML paths, or neural/external repositories with heavier dependencies.",
    ])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--benchmarks", type=Path, default=BENCHMARKS)
    parser.add_argument("--report", type=Path, default=REPORT)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    rows = []
    for submission in sorted(args.benchmarks.glob("matbench_v0.1_*")):
        if not submission.is_dir():
            continue
        row = summarize_submission(submission)
        row["disposition"] = disposition(row)
        rows.append(row)
    write_report(args.report, rows)
    print(json.dumps({
        "submissions": len(rows),
        "report": str(args.report),
        "dispositions": dict(Counter(row["disposition"] for row in rows)),
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
