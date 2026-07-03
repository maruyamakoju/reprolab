"""Replay the Matbench v0.1 TPOT-Mat steels submission from source artifacts.

The upstream submission is notebook-based. It loads a pickled TPOT pipeline,
uses ``utils.LoadExisting.cleaning`` to convert steel compositions into numeric
features, refits the pipeline on each Matbench fold, and records predictions.

This script intentionally avoids importing Matbench or matminer. The validation
split JSON and the locally cached Matminer dataset JSON are enough for the
single steels task replayed here.
"""

from __future__ import annotations

import argparse
import gzip
import importlib.util
import json
import math
import pickle
from pathlib import Path
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
MATBENCH_ROOT = ROOT / "vendor" / "matbench"
SUBMISSION_DIR = MATBENCH_ROOT / "benchmarks" / "matbench_v0.1_TPOT"
VALIDATION_PATH = MATBENCH_ROOT / "matbench" / "matbench_v0.1_validation.json"
STEELS_DATA_PATH = (
    ROOT
    / "env"
    / "jarvis"
    / "Lib"
    / "site-packages"
    / "matminer"
    / "datasets"
    / "matbench_steels.json.gz"
)
TASK = "matbench_steels"
TARGET = "yield strength"


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


def load_steels(data_path: Path) -> dict[str, dict[str, Any]]:
    raw = read_json(data_path)
    columns = raw["columns"]
    rows = raw["data"]
    ids = matbench_ids(TASK, len(rows))
    return {
        mbid: dict(zip(columns, row))
        for mbid, row in zip(ids, rows)
    }


def load_tpot_cleaner(submission_dir: Path) -> Any:
    utils_path = submission_dir / "utils.py"
    spec = importlib.util.spec_from_file_location("matbench_tpot_utils", utils_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"could not load {utils_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.LoadExisting()


def load_pipeline(submission_dir: Path) -> Any:
    # Required so pickle can resolve tpot.builtins.* classes normally.
    import tpot  # noqa: F401

    with (submission_dir / "tpot_best_pipeline.pkl").open("rb") as fh:
        return pickle.load(fh)


def regression_scores(y_true: np.ndarray, y_pred: np.ndarray) -> dict[str, float]:
    err = y_true - y_pred
    mask = np.abs(y_true) > 1e-5
    return {
        "mae": float(np.mean(np.abs(err))),
        "rmse": float(math.sqrt(np.mean(err**2))),
        "mape": float(np.mean(np.fabs((y_true[mask] - y_pred[mask]) / y_true[mask]))),
        "max_error": float(np.max(np.abs(err))),
    }


def format_float(value: float) -> str:
    return f"{value:.12g}"


def write_report(
    path: Path,
    *,
    rows: list[dict[str, Any]],
    max_prediction_delta: float,
    max_score_delta: float,
    args: argparse.Namespace,
) -> None:
    lines = [
        "# Matbench v0.1 TPOT steels source replay",
        "",
        "- Submission: `matbench_v0.1_TPOT` / `TPOT-Mat`",
        "- Task: `matbench_steels`",
        "- Source artifacts used: `Matbench_steel_TPOT.ipynb`, `utils.py`, `tpot_best_pipeline.pkl`, `results.json.gz`",
        f"- Python environment: `{args.python_env}`",
        f"- Audit random seed: `{args.seed}`",
        f"- Folds replayed: {len(rows)}",
        f"- Max absolute prediction delta vs submitted artifact: {max_prediction_delta:.3e}",
        f"- Max absolute score delta vs submitted artifact: {max_score_delta:.3e}",
        "",
        "## Method",
        "",
        "The replay mirrors the notebook path: load the pickled TPOT pipeline, load Matbench's steels folds, convert composition strings with the submitted `LoadExisting.cleaning` helper, refit the pipeline on each training fold, predict the held-out fold, then compare with the committed `results.json.gz` predictions and stored scores. The submitted notebook does not set a random seed; this audit sets one so the replay report is stable.",
        "",
        "## Fold comparison",
        "",
        "| Fold | Train n | Test n | Max prediction delta | Mean prediction delta | Submitted MAE | Replay MAE | MAE delta |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            "| {fold} | {train_n} | {test_n} | {max_pred_delta} | {mean_pred_delta} | {submitted_mae} | {replay_mae} | {mae_delta} |".format(
                fold=row["fold"],
                train_n=row["train_n"],
                test_n=row["test_n"],
                max_pred_delta=format_float(row["max_prediction_delta"]),
                mean_pred_delta=format_float(row["mean_prediction_delta"]),
                submitted_mae=format_float(row["submitted_mae"]),
                replay_mae=format_float(row["replay_mae"]),
                mae_delta=format_float(row["mae_delta"]),
            )
        )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--submission-dir", type=Path, default=SUBMISSION_DIR)
    parser.add_argument("--data", type=Path, default=STEELS_DATA_PATH)
    parser.add_argument("--report", type=Path, default=ROOT / "papers" / "matbench" / "layer_b_tpot_steels_replay.md")
    parser.add_argument("--folds", nargs="*", type=int, default=[0, 1, 2, 3, 4])
    parser.add_argument("--python-env", default="env/matbench-tpot")
    parser.add_argument("--seed", type=int, default=0)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    np.random.seed(args.seed)
    validation = read_json(VALIDATION_PATH)["splits"][TASK]
    submitted = read_json(args.submission_dir / "results.json.gz")["tasks"][TASK]["results"]
    data_by_id = load_steels(args.data)
    cleaner = load_tpot_cleaner(args.submission_dir)
    pipeline = load_pipeline(args.submission_dir)

    rows: list[dict[str, Any]] = []
    max_prediction_delta = 0.0
    max_score_delta = 0.0

    for fold in args.folds:
        fold_key = f"fold_{fold}"
        train_ids = validation[fold_key]["train"]
        test_ids = validation[fold_key]["test"]
        x_train_raw = [data_by_id[mbid]["composition"] for mbid in train_ids]
        y_train = np.asarray([data_by_id[mbid][TARGET] for mbid in train_ids], dtype=float)
        x_test_raw = [data_by_id[mbid]["composition"] for mbid in test_ids]
        y_test = np.asarray([data_by_id[mbid][TARGET] for mbid in test_ids], dtype=float)

        x_train = np.asarray(cleaner.cleaning(x_train_raw), dtype=np.float64)
        x_test = np.asarray(cleaner.cleaning(x_test_raw), dtype=np.float64)

        pipeline.fit(x_train, y_train)
        replay_pred = np.asarray(pipeline.predict(x_test), dtype=float)
        submitted_pred = np.asarray(
            [submitted[fold_key]["data"][mbid] for mbid in test_ids],
            dtype=float,
        )
        pred_delta = np.abs(replay_pred - submitted_pred)

        replay_scores = regression_scores(y_test, replay_pred)
        stored_scores = {k: float(v) for k, v in submitted[fold_key]["scores"].items()}
        score_delta = {
            metric: abs(stored_scores[metric] - replay_scores[metric])
            for metric in replay_scores
        }

        fold_max_pred_delta = float(np.max(pred_delta))
        fold_max_score_delta = max(score_delta.values())
        max_prediction_delta = max(max_prediction_delta, fold_max_pred_delta)
        max_score_delta = max(max_score_delta, fold_max_score_delta)
        rows.append(
            {
                "fold": fold,
                "train_n": len(train_ids),
                "test_n": len(test_ids),
                "max_prediction_delta": fold_max_pred_delta,
                "mean_prediction_delta": float(np.mean(pred_delta)),
                "submitted_mae": stored_scores["mae"],
                "replay_mae": replay_scores["mae"],
                "mae_delta": score_delta["mae"],
            }
        )

    write_report(
        args.report,
        rows=rows,
        max_prediction_delta=max_prediction_delta,
        max_score_delta=max_score_delta,
        args=args,
    )
    print(
        json.dumps(
            {
                "folds_replayed": len(rows),
                "max_prediction_delta": max_prediction_delta,
                "max_score_delta": max_score_delta,
                "report": str(args.report),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
