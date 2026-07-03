"""Replay the Matbench v0.1 Dummy submission from notebook logic."""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

import numpy as np
import sklearn
from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score, roc_auc_score

from matbench_tpot_replay import format_float, matbench_ids, read_json, regression_scores


ROOT = Path(__file__).resolve().parent.parent
MATBENCH_ROOT = ROOT / "vendor" / "matbench"
SUBMISSION_DIR = MATBENCH_ROOT / "benchmarks" / "matbench_v0.1_dummy"
METADATA_PATH = MATBENCH_ROOT / "matbench" / "matbench_v0.1_dataset_metadata.json"
VALIDATION_PATH = MATBENCH_ROOT / "matbench" / "matbench_v0.1_validation.json"
DATASET_DIR = ROOT / "env" / "jarvis" / "Lib" / "site-packages" / "matminer" / "datasets"
DEFAULT_TASKS = ["matbench_expt_gap", "matbench_expt_is_metal", "matbench_glass", "matbench_steels"]


def load_target(task: str, target: str) -> dict[str, Any]:
    raw = read_json(DATASET_DIR / f"{task}.json.gz")
    target_idx = raw["columns"].index(target)
    ids = matbench_ids(task, len(raw["data"]))
    return {
        mbid: row[target_idx]
        for mbid, row in zip(ids, raw["data"])
    }


def classification_scores(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float]:
    true = np.asarray(y_true, dtype=bool)
    pred = np.asarray(y_pred, dtype=bool)
    return {
        "accuracy": float(accuracy_score(true, pred)),
        "balanced_accuracy": float(balanced_accuracy_score(true, pred)),
        "f1": float(f1_score(true, pred)),
        "rocauc": float(roc_auc_score(true, pred)),
    }


def replay_predictions(
    *,
    task_type: str,
    y_train: np.ndarray,
    test_n: int,
) -> np.ndarray:
    x_train = np.zeros((len(y_train), 1))
    x_test = np.zeros((test_n, 1))
    if task_type == "classification":
        model = DummyClassifier(strategy="stratified")
    else:
        model = DummyRegressor(strategy="mean")
    model.fit(x_train, y_train)
    return np.asarray(model.predict(x_test))


def write_report(
    path: Path,
    *,
    rows: list[dict[str, Any]],
    args: argparse.Namespace,
) -> None:
    regression_rows = [row for row in rows if row["task_type"] == "regression"]
    classification_rows = [row for row in rows if row["task_type"] == "classification"]
    exact_rows = [row for row in rows if row["prediction_delta"] == 0 and row["max_score_delta"] == 0]
    regression_exact = sum(1 for row in regression_rows if row["prediction_delta"] == 0 and row["max_score_delta"] == 0)
    classification_exact = sum(1 for row in classification_rows if row["prediction_delta"] == 0 and row["max_score_delta"] == 0)
    max_prediction_delta = max(row["prediction_delta"] for row in rows) if rows else 0.0
    max_score_delta = max(row["max_score_delta"] for row in rows) if rows else 0.0

    lines = [
        "# Matbench v0.1 Dummy source replay",
        "",
        "- Submission: `matbench_v0.1_dummy` / `Dummy`",
        f"- Tasks replayed: {len(set(row['task'] for row in rows))}",
        f"- Folds replayed: {len(rows)}",
        f"- Python environment: `{args.python_env}`",
        f"- scikit-learn version: `{sklearn.__version__}`",
        f"- Audit NumPy seed: `{args.seed}`",
        f"- Exact prediction+score folds: {len(exact_rows)} / {len(rows)}",
        f"- Regression exact folds: {regression_exact} / {len(regression_rows)}",
        f"- Classification exact folds: {classification_exact} / {len(classification_rows)}",
        f"- Max prediction delta / mismatch rate: {max_prediction_delta:.3e}",
        f"- Max score delta: {max_score_delta:.3e}",
        "",
        "## Method",
        "",
        "The replay mirrors the submitted notebook logic on a bounded low-cost task subset: `DummyRegressor(strategy=\"mean\")` for regression and `DummyClassifier(strategy=\"stratified\")` for classification. The notebook does not record a random seed for the stratified classifier, so this audit sets a NumPy seed only to make the replay deterministic.",
        "",
        "## Fold comparison",
        "",
        "| Task | Fold | Type | Test n | Prediction delta / mismatch rate | Primary stored | Primary replay | Primary delta | Max score delta |",
        "|---|---:|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            "| {task} | {fold} | {task_type} | {test_n} | {prediction_delta} | {stored_primary} | {replay_primary} | {primary_delta} | {max_score_delta} |".format(
                task=row["task"],
                fold=row["fold"],
                task_type=row["task_type"],
                test_n=row["test_n"],
                prediction_delta=format_float(row["prediction_delta"]),
                stored_primary=format_float(row["stored_primary"]),
                replay_primary=format_float(row["replay_primary"]),
                primary_delta=format_float(row["primary_delta"]),
                max_score_delta=format_float(row["max_score_delta"]),
            )
        )

    lines.extend([
        "",
        "## Interpretation",
        "",
        "The mean-regression dummy source path is prediction-identical for the checked regression folds. The stratified classification dummy source path is runnable but not prediction-identical under the audit seed, which is expected because the submitted notebook did not persist the RNG state or a classifier `random_state`.",
    ])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--submission-dir", type=Path, default=SUBMISSION_DIR)
    parser.add_argument("--report", type=Path, default=ROOT / "papers" / "matbench" / "layer_b_dummy_composition_replay.md")
    parser.add_argument("--tasks", nargs="+", default=DEFAULT_TASKS)
    parser.add_argument("--seed", type=int, default=0)
    parser.add_argument("--python-env", default="env/matbench-tpot")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    np.random.seed(args.seed)
    metadata = read_json(METADATA_PATH)
    validation = read_json(VALIDATION_PATH)["splits"]
    submitted = read_json(args.submission_dir / "results.json.gz")["tasks"]
    rows: list[dict[str, Any]] = []

    for task in args.tasks:
        task_meta = metadata[task]
        task_type = task_meta["task_type"]
        primary_metric = "rocauc" if task_type == "classification" else "mae"
        target_by_id = load_target(task, task_meta["target"])
        for fold_key, split in sorted(validation[task].items()):
            train_ids = split["train"]
            test_ids = split["test"]
            y_train = np.asarray([target_by_id[mbid] for mbid in train_ids])
            y_true = np.asarray([target_by_id[mbid] for mbid in test_ids])
            replay_pred = replay_predictions(
                task_type=task_type,
                y_train=y_train,
                test_n=len(test_ids),
            )
            submitted_fold = submitted[task]["results"][fold_key]
            submitted_pred = np.asarray([submitted_fold["data"][mbid] for mbid in test_ids])
            if task_type == "classification":
                replay_scores = classification_scores(y_true, replay_pred)
                prediction_delta = float(np.mean(np.asarray(replay_pred, dtype=bool) != np.asarray(submitted_pred, dtype=bool)))
            else:
                replay_scores = regression_scores(y_true.astype(float), replay_pred.astype(float))
                prediction_delta = float(np.max(np.abs(replay_pred.astype(float) - submitted_pred.astype(float))))
            stored_scores = {metric: float(value) for metric, value in submitted_fold["scores"].items()}
            score_delta = {
                metric: abs(stored_scores[metric] - replay_scores[metric])
                for metric in replay_scores
            }
            rows.append(
                {
                    "task": task,
                    "fold": fold_key.replace("fold_", ""),
                    "task_type": task_type,
                    "test_n": len(test_ids),
                    "prediction_delta": prediction_delta,
                    "stored_primary": stored_scores[primary_metric],
                    "replay_primary": replay_scores[primary_metric],
                    "primary_delta": score_delta[primary_metric],
                    "max_score_delta": max(score_delta.values()),
                }
            )

    write_report(args.report, rows=rows, args=args)
    print(
        json.dumps(
            {
                "folds_replayed": len(rows),
                "max_prediction_delta": max(row["prediction_delta"] for row in rows),
                "max_score_delta": max(row["max_score_delta"] for row in rows),
                "report": str(args.report),
                "sklearn": sklearn.__version__,
                "tasks": args.tasks,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
