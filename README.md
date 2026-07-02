# ReproLab

Independent reproducibility audits of AI-for-science papers and benchmarks.
We answer, for a real published result: *can the code run, are the metrics
reproducible, are leaderboard values independently verifiable, what compute is
required, and what fails?*

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

## Reproduce it yourself

```bash
# 1. clone this repo, then clone the upstream benchmark into vendor/ (git-ignored)
git clone --depth 1 https://github.com/janosh/matbench-discovery \
    vendor/matbench-discovery

# 2. isolated environment (never use system Python)
python -m venv .venv
. .venv/Scripts/activate         # Windows;  use  source .venv/bin/activate  on Linux/mac
pip install matbench-discovery   # brings the official stable_metrics + deps

# 3. snapshot the environment
python scripts/capture_env.py

# 4. Layer A: recompute CHGNet discovery metrics and diff vs the official YAML
python scripts/run_command.py --note "layerA chgnet" -- \
    python scripts/compare_metrics.py --model chgnet-0.3.0 \
        --subsets unique_prototypes full_test_set

# 5. assemble the report
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
- [x] **Layer A — 3 models checked, all reproduce the official YAML exactly**
      (both subsets; integer confusion counts identical; independent + upstream agree)
      - CHGNet: uniq_protos F1 0.613 / MAE 0.063 · full F1 0.612 / MAE 0.061
      - SevenNet-0: uniq_protos F1 0.724 / MAE 0.048 · full F1 0.719 / MAE 0.046
      - MACE-MP-0: uniq_protos F1 0.669 / MAE 0.057 · full F1 0.668 / MAE 0.055
- [ ] Interim report generated + README polished for external readers
- [ ] Fourth model (ORB) / GPU Layer B: regenerate predictions and re-score

## Rules
See `CLAUDE.md`. Short version: log every command, trace every metric to code,
no secrets, no bypass-permissions, no wet-lab, no materials generation.
