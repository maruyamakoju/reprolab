"""Leaderboard point-gap analysis for JARVIS Layer A reports."""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from statistics import median


LOWER_IS_BETTER = {"MAE", "MULTIMAE"}
HIGHER_IS_BETTER = {"ACC"}


def parse_report(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    target = re.search(r"Target: `([^`]+)`", text).group(1)
    models_scored = int(re.search(r"Models scored: ([0-9]+)", text).group(1))
    header = re.search(
        r"\| model \| team \| official ([A-Z]+) \| reproduced ([A-Z]+) \|",
        text,
    )
    if not header:
        raise ValueError(f"could not parse metric table header in {path}")
    metric = header.group(1)
    rows = []
    for line in text.splitlines():
        if not line.startswith("| ") or "|---" in line or " official " in line:
            continue
        parts = [part.strip() for part in line.strip("|").split("|")]
        if len(parts) != 7:
            continue
        model, team, official, reproduced, row_count, id_check, passed = parts
        if passed != "yes":
            continue
        rows.append(
            {
                "model": model,
                "team": team,
                "official": float(official),
                "reproduced": float(reproduced),
                "rows": int(row_count),
                "id_check": id_check,
            }
        )
    if len(rows) != models_scored:
        raise ValueError(f"parsed {len(rows)} rows but expected {models_scored} in {path}")
    return {"path": path, "target": target, "metric": metric, "rows": rows}


def adjacent_pairs(report: dict) -> list[dict]:
    metric = report["metric"]
    reverse = metric in HIGHER_IS_BETTER
    if metric not in LOWER_IS_BETTER | HIGHER_IS_BETTER:
        raise ValueError(f"unsupported metric: {metric}")
    ranked = sorted(report["rows"], key=lambda row: row["official"], reverse=reverse)
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
                "models": len(ranked),
            }
        )
    return pairs


def target_label(target: str) -> str:
    parts = target.split("-")
    if len(parts) >= 5:
        return f"{parts[1]} / {parts[2]} / {parts[3]}"
    return target


def write_report(reports: list[dict], out: Path) -> None:
    all_pairs = [pair for report in reports for pair in adjacent_pairs(report)]
    all_pairs.sort(key=lambda pair: pair["official_gap"])

    lines = [
        "# Leaderboard Resolution - JARVIS Layer A",
        "",
        "This is a point-gap analysis of the 14 checked JARVIS-Leaderboard pages.",
        "It is not an uncertainty estimate. It only asks how close adjacent official",
        "point estimates are after sorting each page by its metric direction.",
        "",
        "## Aggregate",
        "",
        f"- Reports checked: {len(reports)}",
        f"- Submissions checked: {sum(len(report['rows']) for report in reports)}",
        f"- Adjacent pairs: {len(all_pairs)}",
        f"- Adjacent gaps <= 0.001: {sum(pair['official_gap'] <= 0.001 for pair in all_pairs)}",
        f"- Adjacent gaps <= 0.005: {sum(pair['official_gap'] <= 0.005 for pair in all_pairs)}",
        f"- Adjacent gaps <= 0.010: {sum(pair['official_gap'] <= 0.010 for pair in all_pairs)}",
        "",
        "## Per-page Summary",
        "",
        "| target | metric | models | adjacent pairs | min gap | median gap | gaps <= 0.001 | gaps <= 0.005 | closest pair |",
        "|---|---|---:|---:|---:|---:|---:|---:|---|",
    ]

    for report in sorted(reports, key=lambda item: item["target"]):
        pairs = adjacent_pairs(report)
        if pairs:
            gaps = [pair["official_gap"] for pair in pairs]
            closest = min(pairs, key=lambda pair: pair["official_gap"])
            closest_pair = f"{closest['better']} to {closest['worse']}"
            min_gap = f"{min(gaps):.8f}"
            median_gap = f"{median(gaps):.8f}"
        else:
            gaps = []
            closest_pair = "n/a"
            min_gap = "n/a"
            median_gap = "n/a"
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{target_label(report['target'])}`",
                    report["metric"],
                    str(len(report["rows"])),
                    str(len(pairs)),
                    min_gap,
                    median_gap,
                    str(sum(gap <= 0.001 for gap in gaps)),
                    str(sum(gap <= 0.005 for gap in gaps)),
                    closest_pair,
                ]
            )
            + " |"
        )

    lines += [
        "",
        "## Closest Adjacent Pairs",
        "",
        "| rank | target | metric | pair | official gap | reproduced gap |",
        "|---:|---|---|---|---:|---:|",
    ]
    for idx, pair in enumerate(all_pairs[:20], start=1):
        lines.append(
            "| "
            + " | ".join(
                [
                    str(idx),
                    f"`{target_label(pair['target'])}`",
                    pair["metric"],
                    f"{pair['better']} to {pair['worse']}",
                    f"{pair['official_gap']:.8f}",
                    f"{pair['reproduced_gap']:.8f}",
                ]
            )
            + " |"
        )

    lines += [
        "",
        "## Interpretation",
        "",
        "The checked pages contain many adjacent point estimates below 0.005 in metric",
        "units. Those small gaps are the natural targets for a later uncertainty,",
        "split-sensitivity, or bootstrap-style analysis. Layer A already established",
        "that these point estimates are internally reproducible from public artifacts.",
        "",
    ]
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default="papers/jarvis-leaderboard")
    parser.add_argument(
        "--out",
        default="papers/jarvis-leaderboard/layer_c_resolution.md",
    )
    args = parser.parse_args()

    root = Path(args.root)
    reports = [parse_report(path) for path in sorted(root.glob("metric_check*.md"))]
    write_report(reports, Path(args.out))
    total_pairs = sum(max(0, len(report["rows"]) - 1) for report in reports)
    print(
        {
            "reports": len(reports),
            "submissions": sum(len(report["rows"]) for report in reports),
            "adjacent_pairs": total_pairs,
            "out": args.out,
        }
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
