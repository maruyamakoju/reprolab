"""Assemble the Paper-003 Matbench v0.1 audit report."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
PAPER = ROOT / "papers" / "matbench"
OUT = ROOT / "reports" / "paper-003-matbench-audit.md"


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
    parts = [
        "# ReproLab Paper-003 - Matbench v0.1 Audit",
        f"\n_Generated: {now}_\n",
        "> Auto-assembled from tracked artifacts by `scripts/make_matbench_report.py`.",
        section("0. Executive summary", PAPER / "summary.md"),
        section("1. Benchmark metadata", PAPER / "metadata.yaml", code=True),
        section("2. Candidate screen", PAPER / "candidate_screen.md"),
        section("3. Reproduction plan", PAPER / "reproduction_plan.md"),
        section("4. Layer A seed score recomputation", PAPER / "layer_a_score_recompute.md"),
        section("4b. Layer A RF composition-task expansion", PAPER / "layer_a_rf_composition_tasks.md"),
        section("4c. Layer A RF small-structure-task expansion", PAPER / "layer_a_rf_structure_small_tasks.md"),
        section("4d. Layer A RF medium-structure-task expansion", PAPER / "layer_a_rf_structure_medium_tasks.md"),
        section("4e. Layer A RF all-task expansion", PAPER / "layer_a_rf_all_tasks.md"),
        section("4f. Layer A Dummy all-task expansion", PAPER / "layer_a_dummy_all_tasks.md"),
        section("4g. Layer A all-submission score scan", PAPER / "layer_a_all_submission_score_scan.md"),
        section("5. Classification prediction scan", PAPER / "classification_prediction_scan.md"),
        section("5b. Classification leaderboard metric scan", PAPER / "classification_leaderboard_metric_scan.md"),
        section("5c. Classification ROC-AUC probe", PAPER / "classification_auc_probe.md"),
        section("5d. MODNet v0.1.10 probability-AUC probe", PAPER / "layer_a_modnet_0_1_10_probability_auc_probe.md"),
        section("5e. MODNet v0.1.12 probability-AUC probe", PAPER / "layer_a_modnet_0_1_12_probability_auc_probe.md"),
        section("6. Source artifact inventory", PAPER / "source_artifact_inventory.md"),
        section("7. Layer B TPOT steels source replay", PAPER / "layer_b_tpot_steels_replay.md"),
        section("8. Upstream issue draft", ROOT / "reports" / "paper-003_upstream_issue_draft.md"),
        section("9. Run log (tail)", PAPER / "run_log.md", tail=160),
    ]
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(parts) + "\n", encoding="utf-8")
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
