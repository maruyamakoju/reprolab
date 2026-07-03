"""Assemble the Paper-002 JARVIS-Leaderboard audit report."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PAPER = ROOT / "papers" / "jarvis-leaderboard"
OUT = ROOT / "reports" / "paper-002-jarvis-leaderboard-audit.md"


def section(title: str, path: Path, *, code: bool = False, tail: int | None = None) -> str:
    if not path.exists():
        return f"\n## {title}\n\n_(missing: {path.relative_to(ROOT)})_\n"
    text = path.read_text(encoding="utf-8")
    if tail is not None:
        text = "\n".join(text.splitlines()[-tail:])
    body = f"```\n{text}\n```" if code else text
    return f"\n## {title}\n\n{body}\n"


def main() -> None:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    metric_sections = [
        section(f"5. Metric check - {path.stem}", path)
        for path in sorted(PAPER.glob("metric_check*.md"))
    ]
    parts = [
        "# ReproLab Paper-002 - JARVIS-Leaderboard Audit",
        f"\n_Generated: {now}_\n",
        "> Auto-assembled from tracked artifacts by `scripts/make_jarvis_report.py`.",
        section("0. Executive summary", PAPER / "summary.md"),
        section("1. Benchmark metadata", PAPER / "metadata.yaml", code=True),
        section("2. Reproduction plan", PAPER / "reproduction_plan.md"),
        section("3. Layer B execution-path probe", PAPER / "layer_b_probe.md"),
        section("4. Layer B bounded matminer_rf pre-smoke",
                PAPER / "layer_b_matminer_rf_smoke.md"),
        section("4b. Layer C point-gap map", PAPER / "layer_c_resolution.md"),
        *metric_sections,
        section("6. Run log (tail)", PAPER / "run_log.md", tail=120),
    ]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(parts) + "\n", encoding="utf-8")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
