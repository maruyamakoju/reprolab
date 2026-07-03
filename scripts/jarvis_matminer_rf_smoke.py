"""Bounded Layer B pre-smoke for the JARVIS matminer_rf baseline.

This is intentionally not a full leaderboard regeneration. It executes the same
kind of path as the public `matminer_rf` contribution on a small deterministic
slice of the official dft_3d formation-energy split:

- load the official benchmark JSON zip;
- fetch structures through `jarvis.db.figshare.data("dft_3d")`;
- compute Matminer structure/composition features;
- fit a RandomForestRegressor;
- write test predictions and a short audit report.
"""

from __future__ import annotations

import argparse
import csv
import json
import time
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd
from jarvis.core.atoms import Atoms
from jarvis.db.figshare import data as jarvis_data
from matminer.featurizers.base import MultipleFeaturizer
from matminer.featurizers.composition import (
    ElementProperty,
    IonProperty,
    Stoichiometry,
    ValenceOrbital,
)
from matminer.featurizers.structure import (
    ChemicalOrdering,
    MaximumPackingEfficiency,
    SiteStatsFingerprint,
    StructuralHeterogeneity,
    StructureComposition,
)
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


BENCHMARK = "AI-SinglePropertyPrediction-formation_energy_peratom-dft_3d-test-mae"
JSON_NAME = "dft_3d_formation_energy_peratom.json"


def load_split(vendor: Path) -> dict:
    zip_path = (
        vendor
        / "jarvis_leaderboard"
        / "benchmarks"
        / "AI"
        / "SinglePropertyPrediction"
        / f"{JSON_NAME}.zip"
    )
    with zipfile.ZipFile(zip_path) as zf:
        return json.loads(zf.read(JSON_NAME))


def to_unitcell(structure):
    for site in structure.sites:
        site.to_unit_cell(in_place=True)
    return structure


def build_featurizer(chunksize: int) -> MultipleFeaturizer:
    featurizer = MultipleFeaturizer(
        [
            SiteStatsFingerprint.from_preset("CoordinationNumber_ward-prb-2017"),
            SiteStatsFingerprint.from_preset("LocalPropertyDifference_ward-prb-2017"),
            StructuralHeterogeneity(),
            MaximumPackingEfficiency(),
            ChemicalOrdering(),
            StructureComposition(Stoichiometry()),
            StructureComposition(ElementProperty.from_preset("magpie")),
            StructureComposition(ValenceOrbital(props=["frac"])),
            StructureComposition(IonProperty(fast=True)),
        ]
    )
    featurizer.set_chunksize(chunksize=chunksize)
    return featurizer


def featurize(rows: list[dict], chunksize: int) -> tuple[pd.DataFrame, int]:
    df = pd.DataFrame(rows)
    df["structure"] = df["structure"].apply(to_unitcell)
    base_cols = set(df.columns)
    featurizer = build_featurizer(chunksize=chunksize)
    features = featurizer.featurize_dataframe(
        df,
        "structure",
        ignore_errors=True,
        pbar=False,
    )
    feature_cols = [col for col in features.columns if col not in base_cols]
    failed = int(features[feature_cols].isna().all(axis=1).sum())
    return features[["id", "target", *feature_cols]], failed


def write_predictions(path: Path, ids: list[str], predictions: np.ndarray) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["id", "prediction"])
        for jid, pred in zip(ids, predictions):
            writer.writerow([jid, f"{float(pred):.10f}"])


def write_report(path: Path, summary: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Layer B Pre-smoke - JARVIS matminer_rf",
        "",
        f"Target: `{BENCHMARK}`",
        "",
        "Status: passed. This is a bounded CPU execution-path smoke, not a full",
        "leaderboard reproduction and not a claim to reproduce the official",
        "`matminer_rf` MAE.",
        "",
        "## Result",
        "",
        f"- Train rows: {summary['train_rows']}",
        f"- Test rows: {summary['test_rows']}",
        f"- Feature columns: {summary['feature_columns']}",
        f"- All-NaN feature rows: {summary['all_nan_feature_rows']}",
        f"- Random forest trees: {summary['trees']}",
        f"- Subset MAE: {summary['mae']:.8f}",
        f"- Runtime seconds: {summary['seconds']:.1f}",
        f"- Prediction CSV: `{summary['pred_out']}`",
        "",
        "## Scope",
        "",
        "- Uses the official benchmark train/test split, truncated deterministically",
        "  to the first `--train-size` train ids and first `--test-size` test ids.",
        "- Uses JARVIS `dft_3d` structures fetched by `jarvis-tools`.",
        "- Uses the same broad Matminer feature family and RF hyperparameters as the",
        "  public `matminer_rf` script, but does not run the full 55k-row test page.",
        "- Intended to prove the Layer B execution path is viable in an isolated env.",
        "",
        "## Sample ids",
        "",
        f"- First train id: `{summary['first_train_id']}`",
        f"- First test id: `{summary['first_test_id']}`",
        "",
    ]
    path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vendor", default="vendor/jarvis_leaderboard")
    parser.add_argument("--train-size", type=int, default=32)
    parser.add_argument("--test-size", type=int, default=16)
    parser.add_argument("--trees", type=int, default=100)
    parser.add_argument("--chunksize", type=int, default=8)
    parser.add_argument(
        "--pred-out",
        default="experiments/jarvis-leaderboard/matminer_rf_smoke/predictions.csv",
    )
    parser.add_argument(
        "--out",
        default="papers/jarvis-leaderboard/layer_b_matminer_rf_smoke.md",
    )
    args = parser.parse_args()

    t0 = time.time()
    split = load_split(Path(args.vendor))
    train_items = list(split["train"].items())[: args.train_size]
    test_items = list(split["test"].items())[: args.test_size]
    needed_ids = [jid for jid, _ in train_items + test_items]

    records = {entry["jid"]: entry for entry in jarvis_data("dft_3d")}
    missing = [jid for jid in needed_ids if jid not in records]
    if missing:
        raise RuntimeError(f"missing JARVIS structures for ids: {missing[:5]}")

    rows = []
    for split_name, items in [("train", train_items), ("test", test_items)]:
        for jid, target in items:
            rows.append(
                {
                    "id": jid,
                    "split": split_name,
                    "target": float(target),
                    "structure": Atoms.from_dict(records[jid]["atoms"]).pymatgen_converter(),
                }
            )

    feature_df, failed = featurize(rows, chunksize=args.chunksize)
    feature_cols = [col for col in feature_df.columns if col not in {"id", "target"}]

    train_df = feature_df.iloc[: len(train_items)]
    test_df = feature_df.iloc[len(train_items) :]
    model = Pipeline(
        [
            ("imputer", SimpleImputer()),
            ("scaler", StandardScaler()),
            (
                "model",
                RandomForestRegressor(
                    n_estimators=args.trees,
                    max_features=1 / 3,
                    n_jobs=-1,
                    bootstrap=False,
                    random_state=0,
                ),
            ),
        ]
    )
    model.fit(train_df[feature_cols], train_df["target"].to_numpy())
    predictions = model.predict(test_df[feature_cols])
    mae = float(mean_absolute_error(test_df["target"].to_numpy(), predictions))

    pred_out = Path(args.pred_out)
    write_predictions(pred_out, test_df["id"].tolist(), predictions)

    summary = {
        "benchmark": BENCHMARK,
        "train_rows": len(train_items),
        "test_rows": len(test_items),
        "feature_columns": len(feature_cols),
        "all_nan_feature_rows": failed,
        "trees": args.trees,
        "mae": mae,
        "seconds": time.time() - t0,
        "pred_out": str(pred_out),
        "first_train_id": train_items[0][0],
        "first_test_id": test_items[0][0],
    }
    write_report(Path(args.out), summary)
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
