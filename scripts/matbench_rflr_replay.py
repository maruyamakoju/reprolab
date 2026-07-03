"""Replay the Matbench v0.1 RF-Regex steels submission from source artifacts."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

import numpy as np
import sklearn
from sklearn.ensemble import RandomForestRegressor

from matbench_tpot_replay import format_float, matbench_ids, read_json, regression_scores


ROOT = Path(__file__).resolve().parent.parent
MATBENCH_ROOT = ROOT / "vendor" / "matbench"
SUBMISSION_DIR = MATBENCH_ROOT / "benchmarks" / "matbench_v0.1_RFLR"
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
ELEMENT_COLUMNS = ("C", "Mn", "Si", "Cr", "Ni", "Mo", "V", "N", "Nb", "Co", "W", "Al", "Ti")


def load_steels(data_path: Path) -> dict[str, dict[str, Any]]:
    raw = read_json(data_path)
    columns = raw["columns"]
    rows = raw["data"]
    ids = matbench_ids(TASK, len(rows))
    return {mbid: dict(zip(columns, row)) for mbid, row in zip(ids, rows)}


def convert_features(compositions: list[str]) -> np.ndarray:
    features = np.empty((len(compositions), len(ELEMENT_COLUMNS)))
    for idx, composition in enumerate(compositions):
        numbers = re.findall(r"(?:\d*\.\d+|\d+)", composition)
        elements = re.findall(r"(\w+?)(?:\d*\.\d+|\d+)", composition)
        for col_idx, element in enumerate(ELEMENT_COLUMNS):
            value = 0.0
            for found_idx, found_element in enumerate(elements):
                if found_element == element:
                    value = float(numbers[found_idx])
            features[idx, col_idx] = value
    return features


def replay_fold(
    *,
    train_ids: list[str],
    test_ids: list[str],
    data_by_id: dict[str, dict[str, Any]],
) -> tuple[np.ndarray, np.ndarray, dict[str, float]]:
    x_train_raw = [data_by_id[mbid]["composition"] for mbid in train_ids]
    y_train = np.asarray([data_by_id[mbid][TARGET] for mbid in train_ids], dtype=float)
    x_test_raw = [data_by_id[mbid]["composition"] for mbid in test_ids]
    y_test = np.asarray([data_by_id[mbid][TARGET] for mbid in test_ids], dtype=float)

    model = RandomForestRegressor(n_estimators=30, random_state=1)
    model.fit(convert_features(x_train_raw), y_train)
    predictions = np.asarray(model.predict(convert_features(x_test_raw)), dtype=float)
    return y_test, predictions, regression_scores(y_test, predictions)


def write_report(
    path: Path,
    *,
    rows: list[dict[str, Any]],
    max_prediction_delta: float,
    max_score_delta: float,
    args: argparse.Namespace,
) -> None:
    exact = max_prediction_delta < 1e-12 and max_score_delta < 1e-12
    interpretation = (
        "The source replay is prediction-identical to the submitted artifact."
        if exact
        else "The source path is runnable, but this environment does not regenerate the submitted predictions exactly."
    )
    lines = [
        "# Matbench v0.1 RFLR steels source replay",
        "",
        "- Submission: `matbench_v0.1_RFLR` / `RF-Regex Steels`",
        "- Task: `matbench_steels`",
        "- Source artifacts used: `Matbench_Steels_RFLR.ipynb`, `results.json.gz`",
        f"- Python environment: `{args.python_env}`",
        f"- scikit-learn version: `{sklearn.__version__}`",
        "- Model: `RandomForestRegressor(n_estimators=30, random_state=1)`",
        f"- Folds replayed: {len(rows)}",
        f"- Max absolute prediction delta vs submitted artifact: {max_prediction_delta:.3e}",
        f"- Max absolute score delta vs submitted artifact: {max_score_delta:.3e}",
        "",
        "## Method",
        "",
        "The replay mirrors the submitted notebook: convert each steel composition string into 13 fixed element-fraction columns with the notebook regex, fit a 30-tree scikit-learn random forest with `random_state=1` on each official training fold, predict the held-out fold, then compare with the committed `results.json.gz` predictions and stored scores.",
        "",
        "## Fold comparison",
        "",
        "| Fold | Train n | Test n | Max prediction delta | Mean prediction delta | Submitted MAE | Replay MAE | MAE delta | Max score delta |",
        "|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            "| {fold} | {train_n} | {test_n} | {max_pred_delta} | {mean_pred_delta} | {submitted_mae} | {replay_mae} | {mae_delta} | {max_score_delta} |".format(
                fold=row["fold"],
                train_n=row["train_n"],
                test_n=row["test_n"],
                max_pred_delta=format_float(row["max_prediction_delta"]),
                mean_pred_delta=format_float(row["mean_prediction_delta"]),
                submitted_mae=format_float(row["submitted_mae"]),
                replay_mae=format_float(row["replay_mae"]),
                mae_delta=format_float(row["mae_delta"]),
                max_score_delta=format_float(row["max_score_delta"]),
            )
        )
    lines.extend(["", "## Interpretation", "", interpretation])
    if args.extra_note:
        lines.extend(["", "## Version note", "", args.extra_note])
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--submission-dir", type=Path, default=SUBMISSION_DIR)
    parser.add_argument("--data", type=Path, default=STEELS_DATA_PATH)
    parser.add_argument("--report", type=Path, default=ROOT / "papers" / "matbench" / "layer_b_rflr_steels_replay.md")
    parser.add_argument("--folds", nargs="*", type=int, default=[0, 1, 2, 3, 4])
    parser.add_argument("--python-env", default="env/jarvis")
    parser.add_argument("--extra-note", default="")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    validation = read_json(VALIDATION_PATH)["splits"][TASK]
    submitted = read_json(args.submission_dir / "results.json.gz")["tasks"][TASK]["results"]
    data_by_id = load_steels(args.data)

    rows: list[dict[str, Any]] = []
    max_prediction_delta = 0.0
    max_score_delta = 0.0

    for fold in args.folds:
        fold_key = f"fold_{fold}"
        train_ids = validation[fold_key]["train"]
        test_ids = validation[fold_key]["test"]
        y_test, replay_pred, replay_scores = replay_fold(
            train_ids=train_ids,
            test_ids=test_ids,
            data_by_id=data_by_id,
        )
        submitted_pred = np.asarray([submitted[fold_key]["data"][mbid] for mbid in test_ids], dtype=float)
        stored_scores = {metric: float(value) for metric, value in submitted[fold_key]["scores"].items()}
        pred_delta = np.abs(replay_pred - submitted_pred)
        score_delta = {
            metric: abs(stored_scores[metric] - replay_scores[metric])
            for metric in replay_scores
        }
        fold_max_prediction_delta = float(np.max(pred_delta))
        fold_max_score_delta = max(score_delta.values())
        max_prediction_delta = max(max_prediction_delta, fold_max_prediction_delta)
        max_score_delta = max(max_score_delta, fold_max_score_delta)
        rows.append(
            {
                "fold": fold,
                "train_n": len(train_ids),
                "test_n": len(test_ids),
                "max_prediction_delta": fold_max_prediction_delta,
                "mean_prediction_delta": float(np.mean(pred_delta)),
                "submitted_mae": stored_scores["mae"],
                "replay_mae": replay_scores["mae"],
                "mae_delta": score_delta["mae"],
                "max_score_delta": fold_max_score_delta,
            }
        )
        if len(y_test) != len(test_ids):
            raise AssertionError("unexpected test target length")

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
                "sklearn": sklearn.__version__,
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
