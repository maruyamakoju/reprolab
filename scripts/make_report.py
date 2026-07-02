"""Assemble the Paper-001 audit report from the tracked artifacts.

Concatenates metadata, environment, metric-check, failure notes and a run-log tail
into reports/paper-001-matbench-discovery-audit.md. Idempotent; run after each
experiment. Stdlib only.

Usage:
    python scripts/make_report.py
"""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAPER = ROOT / "papers" / "matbench-discovery"
OUT = ROOT / "reports" / "paper-001-matbench-discovery-audit.md"


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
    # include every per-model metric-check file (metric_check.md is CHGNet;
    # metric_check-<model>.md are the others)
    metric_sections = [
        section(f"4. Metric check — {mc.stem}", mc)
        for mc in sorted(PAPER.glob("metric_check*.md"))
    ]

    parts = [
        "# ReproLab Paper-001 — Independent Reproducibility Audit of Matbench Discovery",
        f"\n_Generated: {now}_\n",
        "> Auto-assembled from tracked artifacts by `scripts/make_report.py`.",
        section("0. Executive summary", PAPER / "summary.md"),
        section("1. Benchmark metadata", PAPER / "metadata.yaml", code=True),
        section("2. Reproduction plan", PAPER / "reproduction_plan.md"),
        section("3. Environment", PAPER / "environment.md"),
        *metric_sections,
        section("5. Failure notes", PAPER / "failure_notes.md"),
        section("6. Run log (tail)", PAPER / "run_log.md", tail=80),
    ]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(parts) + "\n", encoding="utf-8")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
