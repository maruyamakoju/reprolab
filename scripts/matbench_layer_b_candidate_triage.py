"""Rank Matbench v0.1 submissions for the next bounded Layer B replay."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

from matbench_submission_inventory import read_json, text_for_scan


ROOT = Path(__file__).resolve().parent.parent
BENCHMARKS = ROOT / "vendor" / "matbench" / "benchmarks"
REPORT = ROOT / "papers" / "matbench" / "layer_b_candidate_triage.md"

SOURCE_EXTS = {".py", ".ipynb", ".sh", ".yml", ".yaml", ".txt", ".md"}
SAVED_MODEL_EXTS = {".pkl", ".joblib", ".h5", ".pt", ".pth", ".ckpt", ".sav", ".onnx"}
LOW_COST_TASKS = {
    "matbench_steels",
    "matbench_expt_gap",
    "matbench_expt_is_metal",
    "matbench_glass",
    "matbench_jdft2d",
    "matbench_phonons",
}
LARGE_MP_TASKS = {"matbench_mp_e_form", "matbench_mp_gap", "matbench_mp_is_metal"}

SEED_TOKENS = ("random_state", "np.random.seed", "torch.manual_seed", "manual_seed", "random.seed", "seed=")
FIT_TOKENS = (".fit(", "fit(")
PREDICT_TOKENS = (".predict(", "predict(")
HEAVY_DEP_TOKENS = (
    "alignn",
    "crabnet",
    "cuda",
    "dgl",
    "kgcnn",
    "megnet",
    "modnet",
    "ray",
    "tensorflow",
    "torch",
    "torch-geometric",
)
CPU_DEP_TOKENS = ("numpy", "pandas", "scikit-learn", "sklearn", "xgboost")
EXTERNAL_TOKENS = ("git+", "github.com", "git clone", "gptchem", "openai")
CONFLICTING_AUTOML_TOKENS = ("auto-sklearn", "autosklearn")


def md(text: Any) -> str:
    return str(text).replace("|", "/").replace("\n", " ")


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def list_text(items: list[str], *, limit: int = 4) -> str:
    if len(items) <= limit:
        return ", ".join(items)
    return ", ".join(items[:limit]) + f", +{len(items) - limit} more"


def requirement_items(info: dict[str, Any]) -> list[str]:
    reqs = info.get("requirements", {})
    if isinstance(reqs, dict):
        py_reqs = reqs.get("python", [])
        if isinstance(py_reqs, str):
            return [py_reqs]
        if isinstance(py_reqs, list):
            return [str(item) for item in py_reqs]
    if isinstance(reqs, str):
        return [reqs]
    return []


def token_hit(text: str, tokens: tuple[str, ...]) -> bool:
    lowered = text.lower()
    for token in tokens:
        token = token.lower()
        if any(ch in token for ch in "+=/()"):
            if token in lowered:
                return True
            continue
        pattern = rf"(?<![a-z0-9_]){re.escape(token)}(?![a-z0-9_])"
        if re.search(pattern, lowered):
            return True
    return False


def summarize(path: Path) -> dict[str, Any]:
    info_path = path / "info.json"
    results_path = path / "results.json.gz"
    info = read_json(info_path) if info_path.exists() else {}
    results = read_json(results_path) if results_path.exists() else {}
    tasks = sorted(results.get("tasks", {}))
    all_files = [p for p in path.rglob("*") if p.is_file()]
    source_files = [
        p
        for p in all_files
        if p.name not in {"info.json", "results.json.gz"} and p.suffix.lower() in SOURCE_EXTS
    ]
    saved_model_files = [
        p
        for p in all_files
        if p.name not in {"info.json", "results.json.gz"} and p.suffix.lower() in SAVED_MODEL_EXTS
    ]
    scan_text = "\n".join(text_for_scan(p) for p in source_files if p.suffix.lower() in SOURCE_EXTS)
    reqs = requirement_items(info)
    req_text = " ".join(reqs)
    combined = f"{req_text}\n{scan_text}\n{info.get('notes', '')}\n{info.get('algorithm', '')}"

    return {
        "name": path.name,
        "algorithm": info.get("algorithm", ""),
        "tasks": tasks,
        "task_count": len(tasks),
        "low_cost_task_count": sum(task in LOW_COST_TASKS for task in tasks),
        "large_mp_task_count": sum(task in LARGE_MP_TASKS for task in tasks),
        "source_files": [rel(p, path) for p in sorted(source_files)],
        "saved_model_files": [rel(p, path) for p in sorted(saved_model_files)],
        "requirements": reqs,
        "has_run_py": any(p.name.lower() == "run.py" for p in source_files),
        "has_notebook": any(p.suffix.lower() == ".ipynb" for p in source_files),
        "has_seed_signal": token_hit(scan_text, SEED_TOKENS),
        "has_fit_signal": token_hit(scan_text, FIT_TOKENS),
        "has_predict_signal": token_hit(scan_text, PREDICT_TOKENS),
        "has_heavy_deps": token_hit(combined, HEAVY_DEP_TOKENS),
        "has_cpu_deps": token_hit(req_text, CPU_DEP_TOKENS),
        "has_external_signal": token_hit(combined, EXTERNAL_TOKENS),
        "has_conflicting_automl": token_hit(combined, CONFLICTING_AUTOML_TOKENS),
    }


def score(row: dict[str, Any]) -> tuple[int, list[str]]:
    value = 0
    reasons: list[str] = []
    if row["task_count"] == 1:
        value += 25
        reasons.append("one task")
    elif row["task_count"] <= 4:
        value += 10
        reasons.append("few tasks")
    else:
        penalty = min(20, (row["task_count"] - 4) * 2)
        value -= penalty
        reasons.append(f"{row['task_count']} tasks")

    if row["low_cost_task_count"] == row["task_count"] and row["task_count"]:
        value += 15
        reasons.append("all low-cost tasks")
    elif row["low_cost_task_count"]:
        value += 5
        reasons.append("some low-cost tasks")
    if row["large_mp_task_count"]:
        penalty = 5 * row["large_mp_task_count"]
        value -= penalty
        reasons.append("large MP task")

    if row["has_run_py"]:
        value += 15
        reasons.append("run.py")
    if row["has_notebook"]:
        value += 8
        reasons.append("notebook")
    if row["saved_model_files"]:
        value += 25
        reasons.append("saved model")
    if row["has_seed_signal"]:
        value += 10
        reasons.append("seed signal")
    if row["has_fit_signal"] and row["has_predict_signal"]:
        value += 8
        reasons.append("fit/predict path")
    if row["has_cpu_deps"] and not row["has_heavy_deps"]:
        value += 12
        reasons.append("CPU deps")
    if row["has_heavy_deps"]:
        value -= 30
        reasons.append("heavy deps")
    if row["has_external_signal"]:
        value -= 12
        reasons.append("external path")
    if row["has_conflicting_automl"]:
        value -= 20
        reasons.append("AutoML env conflict")
    if not row["source_files"]:
        value -= 20
        reasons.append("no source")

    return max(0, min(100, value)), reasons


def priority(row: dict[str, Any]) -> str:
    if row["name"] == "matbench_v0.1_TPOT":
        return "already replayed"
    if row["name"] == "matbench_v0.1_dummy":
        return "positive-control candidate"
    if row["score"] >= 70:
        return "high"
    if row["score"] >= 45:
        return "medium"
    return "low"


def recommendation(row: dict[str, Any]) -> str:
    name = row["name"]
    if name == "matbench_v0.1_TPOT":
        return "Already used for the first bounded Layer B replay."
    if name == "matbench_v0.1_RFLR":
        return "Best next nontrivial CPU replay target: one steels task, simple deps, seed signal."
    if name == "matbench_v0.1_dummy":
        return "Use as an exact-source positive control if a low-novelty replay is useful."
    if name == "matbench_v0.1_lattice_xgboost":
        return "Bounded one-task baseline, but large MP e_form data and notebook-only source."
    if name == "matbench_v0.1_rf":
        return "Useful reference runner, but all 13 tasks and unseeded RF make exact replay unlikely."
    if row["has_conflicting_automl"]:
        return "Defer for now; Auto-sklearn environment conflicts make this a poor next smoke."
    if row["has_heavy_deps"]:
        return "Defer for now; dependency stack is heavier than needed for the next bounded pass."
    if row["has_external_signal"]:
        return "Defer for now; source path depends on external repository or service state."
    if row["score"] >= 45:
        return "Inspect source manually before environment build."
    return "Low priority for bounded Layer B replay."


def classify_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out = []
    for row in rows:
        row = dict(row)
        row["score"], row["score_reasons"] = score(row)
        row["priority"] = priority(row)
        row["recommendation"] = recommendation(row)
        out.append(row)
    return sorted(out, key=lambda r: (-r["score"], r["name"].lower()))


def write_report(path: Path, rows: list[dict[str, Any]]) -> None:
    counts = Counter(row["priority"] for row in rows)
    next_rows = [
        row
        for row in rows
        if row["name"] != "matbench_v0.1_TPOT"
        and (
            row["priority"] in {"high", "positive-control candidate"}
            or (
                row["priority"] == "medium"
                and not row["has_conflicting_automl"]
                and not row["has_heavy_deps"]
                and not row["has_external_signal"]
            )
        )
    ]
    lines = [
        "# Matbench v0.1 Layer B candidate triage",
        "",
        "This ranks public Matbench v0.1 submission artifacts for the next bounded source replay after the TPOT-Mat smoke. The score is a triage heuristic, not a claim about scientific quality.",
        "",
        f"- Submissions checked: {len(rows)}",
        f"- High-priority candidates: {counts['high']}",
        f"- Medium-priority candidates: {counts['medium']}",
        f"- Low-priority candidates: {counts['low']}",
        f"- Already replayed: {counts['already replayed']}",
        f"- Positive-control candidates: {counts['positive-control candidate']}",
        "",
        "## Decision",
        "",
        "`matbench_v0.1_RFLR` is the best next nontrivial bounded CPU replay target. It has one small `matbench_steels` task, simple scikit-learn/numpy/matbench requirements, a notebook source path, and seed/fit/predict signals. It has no saved fold-level model artifact, so prediction identity is not guaranteed, but it is the cleanest next source-execution probe.",
        "",
        "`matbench_v0.1_dummy` is the best positive-control replay target if an exact source-path check is needed, but it has low novelty. `matbench_v0.1_lattice_xgboost` is a plausible later one-task baseline, but it targets the large `matbench_mp_e_form` task and is notebook-only.",
        "",
        "## Next candidates",
        "",
        "| Rank | Submission | Tasks | Score | Priority | Evidence | Recommendation |",
        "|---:|---|---|---:|---|---|---|",
    ]
    for rank, row in enumerate(next_rows[:8], start=1):
        lines.append(
            "| {rank} | {name} | {tasks} | {score} | {priority} | {evidence} | {rec} |".format(
                rank=rank,
                name=md(row["name"]),
                tasks=md(list_text(row["tasks"], limit=3)),
                score=row["score"],
                priority=md(row["priority"]),
                evidence=md(", ".join(row["score_reasons"])),
                rec=md(row["recommendation"]),
            )
        )

    lines.extend([
        "",
        "## Full ranking",
        "",
        "| Submission | Algorithm | Tasks | Source | Saved models | Score | Priority | Recommendation |",
        "|---|---|---:|---|---|---:|---|---|",
    ])
    for row in rows:
        lines.append(
            "| {name} | {algo} | {tasks} | {source} | {models} | {score} | {priority} | {rec} |".format(
                name=md(row["name"]),
                algo=md(row["algorithm"]),
                tasks=row["task_count"],
                source=md(list_text(row["source_files"]) or ""),
                models=md(list_text(row["saved_model_files"]) or ""),
                score=row["score"],
                priority=md(row["priority"]),
                rec=md(row["recommendation"]),
            )
        )

    lines.extend([
        "",
        "## Scoring notes",
        "",
        "The heuristic rewards one-task scope, low-cost tasks, direct source runners, notebooks, saved model artifacts, seed signals, fit/predict signals, and simple CPU dependencies. It penalizes large MP tasks, heavy neural stacks, external repository/service paths, many-task submissions, and missing source.",
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
        if submission.is_dir():
            rows.append(summarize(submission))
    ranked = classify_rows(rows)
    write_report(args.report, ranked)
    print(json.dumps({
        "submissions": len(ranked),
        "report": str(args.report),
        "top_non_tpot": [row["name"] for row in ranked if row["name"] != "matbench_v0.1_TPOT"][:5],
        "priorities": dict(Counter(row["priority"] for row in ranked)),
    }, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
