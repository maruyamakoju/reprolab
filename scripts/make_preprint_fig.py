"""Build the Layer C resolution figure for the preprint.

Single panel, print/grayscale-friendly, colorblind-safe (Okabe-Ito accent):
histogram of the 59 adjacent-rank F1 gaps across the full leaderboard
(recomputed here from the vendor model YAMLs) against the widest measured
paired-bootstrap 95% CI width among the four audited models, 0.0078 F1. Gaps
below that line are within the statistical noise the leaderboard does not report.

The gap data is regenerated from the clone so the figure and the "43 of 59"
claim in the text share one source. Prints the reproduced count for verification.

Usage:
    python scripts/make_preprint_fig.py --repo vendor/matbench-discovery \
        --out preprint/fig_resolution
"""

from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import yaml  # noqa: E402

# Okabe-Ito colorblind-safe palette (subset), assigned in fixed order by entity.
OKABE = {
    "blue": "#0072B2",
    "vermillion": "#D55E00",
    "green": "#009E73",
    "orange": "#E69F00",
}
INK = "#222222"
MUTED = "#666666"
GRIDGRAY = "#D6D6D6"
BARFILL = "#BFBFBF"

CI_WIDTH = 0.0078  # widest measured 95% CI width among the four audited models


def leaderboard_f1(repo: Path) -> list[tuple[str, float]]:
    """(model_name, uniq_protos F1) for every model YAML with discovery metrics."""
    rows = []
    for path in sorted(repo.glob("models/**/*.yml")):
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
            f1 = data["metrics"]["discovery"]["unique_prototypes"]["F1"]
            rows.append((data.get("model_name", path.stem), float(f1)))
        except (KeyError, TypeError, ValueError, yaml.YAMLError):
            continue
    return sorted(rows, key=lambda r: -r[1])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default="vendor/matbench-discovery")
    ap.add_argument("--out", default="preprint/fig_resolution")
    args = ap.parse_args()

    root = Path(__file__).resolve().parent.parent
    repo = (root / args.repo).resolve()

    board = leaderboard_f1(repo)
    f1s = [f for _, f in board]
    gaps = [round(f1s[i] - f1s[i + 1], 4) for i in range(len(f1s) - 1)]
    n_below = sum(g < CI_WIDTH for g in gaps)
    print(f"leaderboard models with uniq-protos F1: {len(board)}")
    print(f"adjacent pairs: {len(gaps)}; below one CI width ({CI_WIDTH}): {n_below}")

    plt.rcParams.update({
        "font.size": 9.5,
        "axes.edgecolor": MUTED,
        "axes.linewidth": 0.8,
        "xtick.color": INK,
        "ytick.color": INK,
        "text.color": INK,
        "axes.labelcolor": INK,
    })

    fig, ax = plt.subplots(figsize=(6.4, 3.3))

    bins = [i * 0.001 for i in range(0, 21)]  # 0 .. 0.020, 1 mF1-scale bins
    # shade the "within one CI width" region, then draw bars on top
    ax.axvspan(0, CI_WIDTH, color=OKABE["vermillion"], alpha=0.06, zorder=0)
    ax.hist(gaps, bins=bins, color=BARFILL, edgecolor="white", linewidth=0.7,
            zorder=2)
    ax.axvline(CI_WIDTH, color=OKABE["vermillion"], lw=2.0, zorder=3)

    ymax = 9
    ax.set_ylim(0, ymax)
    ax.annotate(
        f"widest measured\n95% CI width = {CI_WIDTH:g} F1",
        xy=(CI_WIDTH, 6.0), xytext=(0.0122, 7.4),
        color=OKABE["vermillion"], fontsize=8.5, va="center", ha="left",
        arrowprops=dict(arrowstyle="-", color=OKABE["vermillion"], lw=1.0),
    )
    ax.text(0.0122, 4.9,
            f"{n_below} of {len(gaps)} adjacent\nleaderboard gaps fall\n"
            "below one CI width",
            color=INK, fontsize=9, va="center", ha="left")

    ax.set_xlim(0, 0.020)
    ax.set_xticks([i * 0.005 for i in range(5)])
    ax.set_yticks(range(0, ymax + 1, 2))
    ax.set_xlabel("adjacent-rank F1 gap on the 60-model leaderboard")
    ax.set_ylabel("number of model pairs")
    ax.grid(axis="y", color=GRIDGRAY, lw=0.6, zorder=1)
    ax.set_axisbelow(True)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.set_title("Most adjacent leaderboard gaps are within bootstrap noise",
                 fontsize=10, loc="left", pad=8)

    fig.tight_layout()
    out = (root / args.out)
    fig.savefig(out.with_suffix(".pdf"))
    fig.savefig(out.with_suffix(".png"), dpi=200)
    print(f"wrote {out.with_suffix('.pdf')} and .png")


if __name__ == "__main__":
    main()
