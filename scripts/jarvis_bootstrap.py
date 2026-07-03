"""Paired bootstrap checks for close JARVIS-Leaderboard adjacent pairs."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import numpy as np

from jarvis_score import (
    load_predictions,
    load_truth,
    normalize_label,
    parse_benchmark_name,
    to_float_vector,
)


LOWER_IS_BETTER = {"mae", "multimae"}
HIGHER_IS_BETTER = {"acc"}


def parse_metric_report(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    target = re.search(r"Target: `([^`]+)`", text).group(1)
    metric = parse_benchmark_name(target).metric
    rows = []
    for line in text.splitlines():
        if not line.startswith("| ") or "|---" in line or " official " in line:
            continue
        parts = [part.strip() for part in line.strip("|").split("|")]
        if len(parts) != 7:
            continue
        model, _team, official, reproduced, row_count, _id_check, passed = parts
        if passed != "yes":
            continue
        rows.append(
            {
                "model": model,
                "official": float(official),
                "reproduced": float(reproduced),
                "rows": int(row_count),
            }
        )
    return {"path": path, "target": target, "metric": metric, "rows": rows}


def adjacent_pairs(report: dict) -> list[dict]:
    metric = report["metric"]
    if metric in LOWER_IS_BETTER:
        ranked = sorted(report["rows"], key=lambda row: row["official"])
    elif metric in HIGHER_IS_BETTER:
        ranked = sorted(report["rows"], key=lambda row: row["official"], reverse=True)
    else:
        raise ValueError(f"unsupported metric: {metric}")

    pairs = []
    for better, worse in zip(ranked, ranked[1:]):
        pairs.append(
            {
                "target": report["target"],
                "metric": metric,
                "better": better["model"],
                "worse": worse["model"],
                "official_gap": abs(better["official"] - worse["official"]),
                "reproduced_gap": abs(better["reproduced"] - worse["reproduced"]),
            }
        )
    return pairs


def prediction_map(root: Path, model: str, target: str) -> dict[str, str]:
    return {str(row["id"]): row["prediction"] for row in load_predictions(root, model, target)}


def paired_advantages(root: Path, pair: dict) -> np.ndarray:
    bench = parse_benchmark_name(pair["target"])
    truth, _sizes = load_truth(root, bench)
    better = prediction_map(root, pair["better"], pair["target"])
    worse = prediction_map(root, pair["worse"], pair["target"])
    truth_ids = set(truth)
    if set(better) != truth_ids or set(worse) != truth_ids:
        raise ValueError(
            f"id mismatch for {pair['target']} {pair['better']} vs {pair['worse']}"
        )

    values = []
    for material_id in sorted(truth):
        if bench.metric == "mae":
            true = float(truth[material_id])
            better_err = abs(float(better[material_id]) - true)
            worse_err = abs(float(worse[material_id]) - true)
            values.append(worse_err - better_err)
        elif bench.metric == "acc":
            true_label = normalize_label(truth[material_id])
            better_ok = normalize_label(better[material_id]) == true_label
            worse_ok = normalize_label(worse[material_id]) == true_label
            values.append(float(better_ok) - float(worse_ok))
        elif bench.metric == "multimae":
            true_vec = to_float_vector(truth[material_id])
            better_vec = to_float_vector(better[material_id])
            worse_vec = to_float_vector(worse[material_id])
            if len(true_vec) != len(better_vec) or len(true_vec) != len(worse_vec):
                raise ValueError(f"vector length mismatch for {pair['target']}")
            for true, better_pred, worse_pred in zip(true_vec, better_vec, worse_vec):
                values.append(abs(worse_pred - true) - abs(better_pred - true))
        else:
            raise ValueError(f"unsupported metric: {bench.metric}")
    return np.asarray(values, dtype=float)


def bootstrap(values: np.ndarray, *, draws: int, seed: int) -> dict:
    rng = np.random.default_rng(seed)
    n = len(values)
    samples = np.empty(draws, dtype=float)
    chunk = max(1, min(draws, 200))
    pos = 0
    while pos < draws:
        take = min(chunk, draws - pos)
        idx = rng.integers(0, n, size=(take, n), dtype=np.int32)
        samples[pos:pos + take] = values[idx].mean(axis=1)
        pos += take
    observed = float(values.mean())
    return {
        "observed": observed,
        "ci_low": float(np.quantile(samples, 0.025)),
        "ci_high": float(np.quantile(samples, 0.975)),
        "std": float(samples.std(ddof=1)),
        "p_tie_or_reversal": float((samples <= 0).mean()),
    }


def target_label(target: str) -> str:
    parts = target.split("-")
    if len(parts) >= 5:
        return f"{parts[1]} / {parts[2]} / {parts[3]}"
    return target


def write_report(results: list[dict], out: Path, *, draws: int, seed: int) -> None:
    lines = [
        "# Layer C Bootstrap - JARVIS Close Adjacent Pairs",
        "",
        "This is a paired, nonparametric bootstrap over fixed public test rows for",
        "the closest adjacent pairs identified by `layer_c_resolution.md`.",
        "",
        "It is not a retraining uncertainty estimate and does not sample alternate",
        "train/validation/test splits. It only tests whether the observed paired",
        "test-row advantage of the official higher-ranked model is stable under",
        "resampling of the published test set.",
        "",
        "## Settings",
        "",
        f"- Bootstrap draws: {draws}",
        f"- Seed: {seed}",
        f"- Pairs checked: {len(results)}",
        "",
        "## Results",
        "",
        "| rank | target | metric | official pair | rows | official gap | paired advantage | 95% CI | P(tie/reversal) |",
        "|---:|---|---|---|---:|---:|---:|---:|---:|",
    ]
    for idx, row in enumerate(results, start=1):
        pair_name = f"{row['better']} over {row['worse']}"
        lines.append(
            "| "
            + " | ".join(
                [
                    str(idx),
                    f"`{target_label(row['target'])}`",
                    row["metric"].upper(),
                    pair_name,
                    str(row["rows"]),
                    f"{row['official_gap']:.8f}",
                    f"{row['observed']:.8f}",
                    f"[{row['ci_low']:.8f}, {row['ci_high']:.8f}]",
                    f"{row['p_tie_or_reversal']:.4f}",
                ]
            )
            + " |"
        )

    unstable = [row for row in results if row["ci_low"] <= 0 <= row["ci_high"]]
    lines += [
        "",
        "## Interpretation",
        "",
        f"- Pairs whose 95% CI includes zero: {len(unstable)} / {len(results)}",
        "- `paired advantage` is positive when the official higher-ranked model has",
        "  the better metric on the resampled test set.",
        "- For MAE/MULTIMAE, advantage is mean(error_lower-ranked - error_higher-ranked).",
        "- For ACC, advantage is mean(correct_higher-ranked - correct_lower-ranked).",
        "- A high `P(tie/reversal)` means the official adjacent ordering is fragile",
        "  under this fixed-test-set bootstrap.",
        "",
    ]
    if unstable:
        lines += [
            "Pairs with CI crossing zero:",
            "",
            "| target | metric | pair | 95% CI | P(tie/reversal) |",
            "|---|---|---|---:|---:|",
        ]
        for row in unstable:
            lines.append(
                "| "
                + " | ".join(
                    [
                        f"`{target_label(row['target'])}`",
                        row["metric"].upper(),
                        f"{row['better']} over {row['worse']}",
                        f"[{row['ci_low']:.8f}, {row['ci_high']:.8f}]",
                        f"{row['p_tie_or_reversal']:.4f}",
                    ]
                )
                + " |"
            )
        lines.append("")

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vendor", default="vendor/jarvis_leaderboard")
    parser.add_argument("--root", default="papers/jarvis-leaderboard")
    parser.add_argument("--top", type=int, default=20)
    parser.add_argument("--draws", type=int, default=2000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--out",
        default="papers/jarvis-leaderboard/layer_c_bootstrap.md",
    )
    args = parser.parse_args()

    paper_root = Path(args.root)
    vendor_root = Path(args.vendor) / "jarvis_leaderboard"
    reports = [parse_metric_report(path) for path in sorted(paper_root.glob("metric_check*.md"))]
    pairs = [pair for report in reports for pair in adjacent_pairs(report)]
    pairs.sort(key=lambda pair: pair["official_gap"])
    selected = pairs[: args.top]

    results = []
    for idx, pair in enumerate(selected):
        values = paired_advantages(vendor_root, pair)
        stats = bootstrap(values, draws=args.draws, seed=args.seed + idx)
        results.append({
            **pair,
            **stats,
            "rows": len(values),
        })

    write_report(results, Path(args.out), draws=args.draws, seed=args.seed)
    print(
        {
            "pairs": len(results),
            "draws": args.draws,
            "ci_cross_zero": sum(row["ci_low"] <= 0 <= row["ci_high"] for row in results),
            "out": args.out,
        }
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
