"""Layer A metric recomputation for selected JARVIS-Leaderboard submissions.

The JARVIS-Leaderboard stores benchmark ground truth as JSON zip files and model
submissions as CSV zip files. This script recomputes the reported MAE directly
from those public artifacts, without rebuilding the website.

Usage:
    python scripts/jarvis_score.py --vendor vendor/jarvis_leaderboard
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import zipfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DEFAULT_BENCH = "AI-SinglePropertyPrediction-formation_energy_peratom-dft_3d-test-mae"
DEFAULT_MODELS = ("kgcnn_coGN", "alignn_model", "matminer_rf")


@dataclass(frozen=True)
class BenchParts:
    category: str
    subcategory: str
    prop: str
    dataset: str
    split: str
    metric: str


def parse_benchmark_name(name: str) -> BenchParts:
    parts = name.removesuffix(".csv.zip").split("-")
    if len(parts) < 6:
        raise ValueError(f"unexpected benchmark name: {name}")
    return BenchParts(
        category=parts[0],
        subcategory=parts[1],
        prop=parts[2],
        dataset=parts[3],
        split=parts[4],
        metric=parts[5],
    )


def read_single_file_zip(path: Path) -> tuple[str, bytes]:
    with zipfile.ZipFile(path) as zf:
        names = [name for name in zf.namelist() if not name.endswith("/")]
        if len(names) != 1:
            raise ValueError(f"expected one file in {path}, found {names}")
        return names[0], zf.read(names[0])


def load_truth(root: Path, bench: BenchParts) -> tuple[dict[str, Any], dict[str, int]]:
    rel = Path("benchmarks") / bench.category / bench.subcategory / (
        f"{bench.dataset}_{bench.prop}.json.zip"
    )
    json_name, raw = read_single_file_zip(root / rel)
    expected_name = f"{bench.dataset}_{bench.prop}.json"
    if json_name != expected_name:
        raise ValueError(f"expected {expected_name} inside {rel}, found {json_name}")
    data = json.loads(raw)
    if bench.split not in data:
        raise KeyError(f"split {bench.split!r} not present in {rel}")
    sizes = {key: len(value) for key, value in data.items() if isinstance(value, dict)}
    return {str(key): value for key, value in data[bench.split].items()}, sizes


def load_predictions(root: Path, model: str, bench_name: str) -> list[dict[str, str]]:
    rel = Path("contributions") / model / f"{bench_name}.csv.zip"
    csv_name, raw = read_single_file_zip(root / rel)
    expected_name = f"{bench_name}.csv"
    text = raw.decode("utf-8")
    rows = list(csv.DictReader(text.splitlines()))
    required = {"id", "prediction"}
    if not rows or not required.issubset(rows[0]):
        raise ValueError(f"{rel} must contain columns {sorted(required)}")
    return rows


def load_metadata(root: Path, model: str) -> dict:
    path = root / "contributions" / model / "metadata.json"
    return json.loads(path.read_text(encoding="utf-8"))


def parse_official_scores(docs_path: Path) -> dict[str, str]:
    text = docs_path.read_text(encoding="utf-8")
    row_re = re.compile(
        r"<tr><td><a [^>]*>(?P<model>[^<]+)</a></td>"
        r"<td>(?P<dataset>[^<]+)</td><td>(?P<score>[^<]+)</td>",
        re.DOTALL,
    )
    return {
        match.group("model"): match.group("score").strip()
        for match in row_re.finditer(text)
    }


def within_reported_rounding(value: float, official_text: str) -> bool:
    official = float(official_text)
    decimals = len(official_text.split(".", maxsplit=1)[1]) if "." in official_text else 0
    tolerance = 0.5 * 10 ** (-decimals) + 1e-12
    return abs(value - official) <= tolerance


def normalize_label(value: Any) -> str:
    text = str(value).strip()
    try:
        number = float(text)
    except ValueError:
        return text.lower()
    if number.is_integer():
        return str(int(number))
    return f"{number:.12g}"


def score_model(root: Path, model: str, bench_name: str, truth: dict[str, Any],
                metric: str) -> dict:
    rows = load_predictions(root, model, bench_name)
    seen: set[str] = set()
    diffs: list[float] = []
    correct = 0
    extra_ids: list[str] = []

    for row in rows:
        material_id = str(row["id"])
        seen.add(material_id)
        if material_id not in truth:
            extra_ids.append(material_id)
            continue
        if metric == "mae":
            diffs.append(abs(float(row["prediction"]) - float(truth[material_id])))
        elif metric == "acc":
            correct += int(
                normalize_label(row["prediction"]) == normalize_label(truth[material_id])
            )
            diffs.append(0.0)
        else:
            raise NotImplementedError(f"metric not implemented: {metric}")

    missing_ids = sorted(set(truth) - seen)
    if not diffs:
        raise ValueError(f"no overlapping ids for {model}")
    score = sum(diffs) / len(diffs) if metric == "mae" else correct / len(diffs)
    metadata = load_metadata(root, model)
    return {
        "model": model,
        "model_name": metadata.get("model_name", model),
        "team": metadata.get("team_name", ""),
        "date": metadata.get("date_submitted", ""),
        "project_url": metadata.get("project_url", ""),
        "rows": len(rows),
        "overlap": len(diffs),
        "missing_ids": missing_ids,
        "extra_ids": extra_ids,
        "score": score,
        "max_abs_error": max(diffs) if metric == "mae" else "",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vendor", default="vendor/jarvis_leaderboard")
    parser.add_argument("--benchmark", default=DEFAULT_BENCH)
    parser.add_argument(
        "--models",
        nargs="+",
        default=list(DEFAULT_MODELS),
        help="models to score, or `all` for every model listed in the docs page",
    )
    parser.add_argument("--out", default="papers/jarvis-leaderboard/metric_check.md")
    args = parser.parse_args()

    vendor = Path(args.vendor)
    root = vendor / "jarvis_leaderboard"
    bench = parse_benchmark_name(args.benchmark)
    truth, split_sizes = load_truth(root, bench)
    docs_path = vendor / "docs" / bench.category / bench.subcategory / (
        f"{bench.dataset}_{bench.prop}.md"
    )
    official_scores = parse_official_scores(docs_path)
    models = list(official_scores) if args.models == ["all"] else args.models

    rows = []
    failures = []
    for model in models:
        result = score_model(root, model, args.benchmark, truth, bench.metric)
        official = official_scores.get(model)
        if official is None:
            ok = "missing-official"
            failures.append(f"{model}: official score not found")
        else:
            ok = "yes" if within_reported_rounding(result["score"], official) else "no"
            if ok == "no":
                failures.append(
                    f"{model}: official {official}, reproduced {result['score']:.8f}"
                )
        result["official"] = official or ""
        result["pass"] = ok
        rows.append(result)

    vendor_display = str(Path(args.vendor)).replace("\\", "/")
    ranked = sorted(
        [row for row in rows if row["official"]],
        key=lambda row: (float(row["official"]), row["model"]),
    )
    closest_pairs = []
    for left, right in zip(ranked, ranked[1:], strict=False):
        closest_pairs.append({
            "pair": f"{left['model']} to {right['model']}",
            "official_gap": abs(float(right["official"]) - float(left["official"])),
            "reproduced_gap": abs(right["score"] - left["score"]),
        })
    closest_pairs = sorted(closest_pairs, key=lambda row: row["official_gap"])[:5]

    lines = [
        "# Metric Check - JARVIS-Leaderboard Layer A",
        "",
        f"Target: `{args.benchmark}`",
        f"Vendor repo: `{vendor_display}`",
        f"Ground-truth split sizes: {split_sizes}",
        "",
        "The score is recomputed from the public submission CSV zip and benchmark JSON "
        "zip artifacts. This mirrors the upstream `rebuild.py::get_metric_value` "
        f"path for `{bench.metric}` but uses a small stdlib-only implementation.",
        f"Models scored: {len(rows)}",
        "",
        f"| model | team | official {bench.metric.upper()} | reproduced "
        f"{bench.metric.upper()} | rows | id check | pass |",
        "|---|---|---:|---:|---:|---|---|",
    ]
    for row in rows:
        id_check = (
            "exact"
            if not row["missing_ids"] and not row["extra_ids"] and row["rows"] == len(truth)
            else f"missing={len(row['missing_ids'])}, extra={len(row['extra_ids'])}"
        )
        lines.append(
            f"| {row['model']} | {row['team']} | {row['official']} | "
            f"{row['score']:.8f} | {row['rows']} | {id_check} | {row['pass']} |"
        )

    if closest_pairs:
        lines.extend([
            "",
            "## Closest adjacent scores",
            "",
            "The official page reports point estimates only; this table flags adjacent "
            f"{bench.metric.upper()} gaps that may deserve uncertainty or sensitivity "
            "checks later.",
            "",
            f"| pair | official {bench.metric.upper()} gap | reproduced "
            f"{bench.metric.upper()} gap |",
            "|---|---:|---:|",
        ])
        for pair in closest_pairs:
            lines.append(
                f"| {pair['pair']} | {pair['official_gap']:.4f} | "
                f"{pair['reproduced_gap']:.8f} |"
            )

    lines.extend([
        "",
        "## Scope",
        "",
        "- Layer A only: metric recomputation from already-published artifacts.",
        "- No model training or model execution yet.",
        "- The target was chosen because the official page exposes CSV predictions, "
        "JSON ground truth, run scripts, and metadata.",
        "",
        "## Next",
        "",
        "Next, decide whether to broaden across more JARVIS tasks or attempt one "
        "Layer B model-execution smoke for a tractable baseline.",
    ])

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print(f"\nwrote {out}")
    if failures:
        print("failures:", "; ".join(failures))
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
