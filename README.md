# ReproLab: Matbench Discovery Reproducibility Audit

ReproLab is an independent reproducibility audit of the Matbench Discovery leaderboard.

## Main result

**Layer A:** Recomputed released leaderboard metrics for 4 released models
(CHGNet, SevenNet-0, MACE-MP-0, ORB v2) from the published prediction CSVs and the
bundled WBM ground truth. **All 4/4 models reproduce the official YAML metrics exactly**
across both audited subsets — every fraction to 3 decimals and every integer
confusion-matrix count.

**Layer B:** Regenerated CHGNet predictions from model execution on a deterministic
500-structure WBM subset (500/500 relaxed, 0 failures, 9.3 min on one RTX 4090).
The regenerated formation energies match the published predictions with
**median |Δe_form| = 0.03 meV/atom** (p95 = 0.07, max = 1.08 meV/atom, pre-registered
threshold: ≤10), **100% stability-classification agreement, and zero flips**.

## Why this matters

This audit checks not just whether leaderboard numbers are internally consistent, but
whether published predictions can be regenerated from model execution on a traceable
subset. Every command is logged, every metric traces to specific code and data, and
comparison thresholds were pre-registered before the GPU runs.

## Reproducibility findings along the way

- Figshare landing URLs (`figshare.com/files/<id>`) are WAF-blocked for naive
  downloaders; the API endpoint works.
- The PyPI wheel and GitHub repo ship different module layouts under the same
  version string (`1.3.1`).
- The upstream md5 for the WBM initial-structures file is stale (it belongs to an
  older artifact) — and upstream never verifies it on download.
- Dependency drift (ruamel.yaml 0.19) breaks pymatgen config loading; pinned `<0.19`.

Details with evidence: `papers/matbench-discovery/failure_notes.md`.

ReproLab's broader goal: independent reproducibility audits of AI-for-science papers
and benchmarks — *can the code run, are the metrics reproducible, are leaderboard
values independently verifiable, what compute is required, and what fails?*

## Paper-001 — Matbench Discovery Audit

> Riebesell et al., *A framework to evaluate machine learning crystal stability
> predictions*, Nature Machine Intelligence 7, 836–847 (2025).
> Upstream: <https://github.com/janosh/matbench-discovery> (MIT).

**Claim under audit:** the leaderboard's per-model stability metrics
(F1, MAE, …). We verify them independently in two layers:

- **Layer A (CPU, deterministic):** recompute the metrics from each model's
  *published* prediction file and check they match the leaderboard values.
- **Layer B (1 GPU):** regenerate the predictions themselves by running the model
  over the WBM initial structures, then re-score.

See `papers/matbench-discovery/reproduction_plan.md` for the full metric→code→data
→command→expected→compare mapping.

## Result so far — Layer A, 4/4 models reproduce the official YAML exactly

| Model | F1 official → reproduced (uniq_protos / full) | MAE eV/atom (uniq_protos / full) |
|---|---|---|
| CHGNet | 0.613→0.613 / 0.612→0.612 | 0.063 / 0.061 |
| SevenNet-0 | 0.724→0.724 / 0.719→0.719 | 0.048 / 0.046 |
| MACE-MP-0 | 0.669→0.669 / 0.668→0.668 | 0.057 / 0.055 |
| ORB v2 | 0.880→0.880 / 0.858→0.858 | 0.028 / 0.028 |

Every reported fraction (to 3 dp) and every integer confusion-matrix count (TP/FP/TN/FN)
matches, computed **two independent ways** (a from-scratch re-implementation *and* the
upstream `stable_metrics`). Assembled report:
`reports/paper-001-matbench-discovery-audit.md`.

## Reproduce it yourself

```bash
# 1. clone this repo, then clone the upstream benchmark into vendor/ (git-ignored).
#    We audited upstream commit eaa7550 (2026-07-02); a --depth 1 clone gets current
#    HEAD, so check `git -C vendor/matbench-discovery log -1` and note any drift.
git clone --depth 1 https://github.com/janosh/matbench-discovery \
    vendor/matbench-discovery

# 2. isolated environment (never use system Python)
python -m venv .venv
. .venv/Scripts/activate         # Windows;  use  source .venv/bin/activate  on Linux/mac
pip install matbench-discovery   # brings the official stable_metrics + deps
# exact versions we ran with (incl. Layer B extras + the ruamel.yaml<0.19 pin):
#   papers/matbench-discovery/requirements-frozen.txt

# 3. snapshot the environment
python scripts/capture_env.py

# 4. Layer A — split download from compute (avoids a rare native crash on Windows),
#    then recompute + diff vs the official YAML. Repeat --model for each:
#    chgnet-0.3.0, sevennet-0, mace-mp-0, orb-v2
#    (invoke the venv python by ABSOLUTE path — run_command.py's subprocess
#    cannot resolve a relative .venv/Scripts/python.exe on Windows)
python scripts/compare_metrics.py --model chgnet-0.3.0 --download-only
python scripts/run_command.py --note "layerA chgnet" -- \
    python scripts/compare_metrics.py --model chgnet-0.3.0 \
        --subsets unique_prototypes full_test_set

# 5. assemble the report (includes every metric_check*.md)
python scripts/make_report.py
```

Ground truth (`data/wbm/2023-12-13-wbm-summary.csv.gz`) ships in the upstream clone;
the CHGNet prediction file is downloaded from Figshare on first run.

> **Note:** the PyPI wheel and the GitHub HEAD both call themselves `1.3.1` but ship
> different module layouts. We therefore audit the **cloned repo** (the leaderboard's
> source) and use `pip install matbench-discovery` only to provide dependencies;
> `compare_metrics.py` puts the clone first on `sys.path`. See
> `papers/matbench-discovery/failure_notes.md`.

## Status (2026-07-02)

- [x] Upstream repo cloned + pinned (`vendor/`, commit `eaa7550`)
- [x] Evaluation path identified at code level (see reproduction plan)
- [x] Target metric selected: CHGNet `unique_prototypes` F1 = 0.613, MAE = 0.063
- [x] First run command defined (`compare_metrics.py`)
- [x] Env built (venv, Python 3.11.9) + `matbench-discovery` installed (exit 0)
- [x] Wiring verified: `stable_metrics` imports; ground-truth rows (256,963) and
      uniq-proto rows (215,488) match the YAML confusion-matrix totals exactly
- [x] **Layer A — 4 models checked, all reproduce the official YAML exactly**
      (both subsets; integer confusion counts identical; independent + upstream agree)
      - CHGNet: uniq_protos F1 0.613 / MAE 0.063 · full F1 0.612 / MAE 0.061
      - SevenNet-0: uniq_protos F1 0.724 / MAE 0.048 · full F1 0.719 / MAE 0.046
      - MACE-MP-0: uniq_protos F1 0.669 / MAE 0.057 · full F1 0.668 / MAE 0.055
      - ORB v2: uniq_protos F1 0.880 / MAE 0.028 · full F1 0.858 / MAE 0.028
- [x] Interim report generated (`reports/paper-001-…md`) + README polished for readers
- [x] Layer A closed at 4/4 (`v0.1-layer-a`)
- [x] Layer B pre-smoke passed: 20/20 ids, run-to-run GPU variance ≤0.232 meV/atom
      (`metric_check-layer-b-chgnet-presmoke.md`)
- [x] **Layer B smoke passed at n=500** (`v0.2-layer-b-smoke`): 500/500 relaxed,
      0 failures, 9.3 min on RTX 4090 (mean 1.06 s/structure); median |Δe_form| =
      0.03 meV/atom vs published (p95 0.07, max 1.08), 100% classification agreement,
      zero flips; subset-level discovery metrics identical
      (`metric_check-layer-b-chgnet-smoke500.md`)
- [x] External-path self-audit: a fresh clone of this public repo, following the
      steps above verbatim (fresh venv + upstream clone + Figshare download),
      reproduces CHGNet Layer A exactly — 22/22 checks, 0 mismatches (run_log.md)
- [ ] Next: Layer B for a second model (ORB / MACE), or Paper-002 — pending external
      feedback

## Rules
See `CLAUDE.md`. Short version: log every command, trace every metric to code,
no secrets, no bypass-permissions, no wet-lab, no materials generation.
