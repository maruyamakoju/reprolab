# ReproLab: Matbench Discovery Reproducibility Audit

ReproLab is an independent reproducibility audit of the Matbench Discovery leaderboard.

## Main result

**Layer A:** Recomputed released leaderboard metrics for 4 released models
(CHGNet, SevenNet-0, MACE-MP-0, ORB v2) from the published prediction CSVs and the
bundled WBM ground truth. **All 4/4 models reproduce the official YAML metrics exactly**
across both audited subsets — every fraction to 3 decimals and every integer
confusion-matrix count.

**Layer B:** Regenerated predictions from model execution for **three models** on the
same deterministic 500-structure WBM subset. CHGNet: 500/500 relaxed, 0 failures,
9.3 min on one RTX 4090, **median |Δe_form| = 0.03 meV/atom** (p95 = 0.07,
max = 1.08), **100% stability-classification agreement, zero flips**. MACE-MP-0:
500/500 relaxed, 0 failures, 10.1 min, **median |Δe_form| = 0.03 meV/atom**,
**99.6% stability-classification agreement**; the three large MACE outliers are the
same MP2020 correction-drift structures identified in the ground-truth audit. ORB v2:
500/500 relaxed, 0 failures, 5.2 min, **median |Δe_form| = 0.05 meV/atom**,
**100% stability-classification agreement, zero flips** when using the YAML
`max_force: 0.02` setting.

**Layer C:** Statistical audit of the leaderboard itself (uncertainty is not reported
upstream). Paired bootstrap (B=2000, exact 32-joint-category multinomial design) puts
**95% CIs of ±0.003–0.004 F1** on the four audited models — their ranking is
statistically solid (P(flip) < 1/2000 for every pair) and survives a ±100 meV/atom
stability-threshold sweep. But applying the measured CI width to the full 60-model
leaderboard, **43 of 59 adjacent pairs are separated by less than one CI width** —
the published ordering at the top is unlikely to be statistically resolvable.
Error analysis: the three MPtrj-trained models share failure modes (pairwise error
correlation r ≈ 0.76; all-four-models-miss rate is **25× the independence
prediction**), while ORB v2 (extra training data) contributes 1,886 unique
true-positive discoveries vs ~350–390 for each of the others.

**Ground-truth audit:** recomputing `e_above_hull` from the published structure
entries + MP2020 corrections + the published 2023 MP phase diagram reproduces
**497/500** subset values to ≤0.001 meV/atom under pymatgen 2026 — but **3/500 shift
by 119–217 meV/atom and 2 stability labels flip**, traced to MP2020 anion-correction
assignment (oxidation-state guessing) drifting across pymatgen versions. The
benchmark's ground truth is not version-independent, and the ambiguity (~0.4–0.6%)
is material at the ΔF1 ≈ 0.001–0.003 gaps separating adjacent leaderboard models.

## Why this matters

This audit checks not just whether leaderboard numbers are internally consistent, but
whether published predictions can be regenerated from model execution on a traceable
subset. Every command is logged, every metric traces to specific code and data, and
comparison thresholds were pre-registered before the GPU runs.

## External validation

- Upstream issue filed with the stale-md5 / unverified-checksum finding:
  [janosh/matbench-discovery#357](https://github.com/janosh/matbench-discovery/issues/357)
  and fix submitted as
  [PR #359](https://github.com/janosh/matbench-discovery/pull/359)
  (response pending)
- Upstream issue filed with the ground-truth pymatgen-version-dependence finding:
  [janosh/matbench-discovery#358](https://github.com/janosh/matbench-discovery/issues/358)
  and docs note submitted as
  [PR #360](https://github.com/janosh/matbench-discovery/pull/360)
  (response pending)
- External handoff packet:
  `reports/external_release_packet.md`

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
# exact versions we ran with (incl. Layer B CHGNet/MACE extras + ruamel.yaml<0.19):
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

## Status (2026-07-03)

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
- [x] **Layer B CHGNet smoke passed at n=500** (`v0.2-layer-b-smoke`):
      500/500 relaxed,
      0 failures, 9.3 min on RTX 4090 (mean 1.06 s/structure); median |Δe_form| =
      0.03 meV/atom vs published (p95 0.07, max 1.08), 100% classification agreement,
      zero flips; subset-level discovery metrics identical
      (`metric_check-layer-b-chgnet-smoke500.md`)
- [x] **Layer B second-model smoke passed for MACE-MP-0 at n=500**:
      500/500 relaxed, 0 failures, 10.1 min on RTX 4090 (mean 1.18 s/structure);
      median |Δe_form| = 0.03 meV/atom vs published, 99.6% classification agreement
      (2 flips). Three large e_form outliers (max 216.65 meV/atom) coincide with the
      MP2020 correction-version drift already isolated in Layer C; outside those,
      agreement is at CSV-rounding scale. The second flip is a 0.1 meV/atom
      threshold-boundary case (`metric_check-layer-b-mace-mp-0-smoke500.md`).
- [x] **Layer B third-model smoke passed for ORB v2 at n=500**:
      500/500 relaxed, 0 failures, 5.2 min on RTX 4090 (mean 0.60 s/structure);
      median |Δe_form| = 0.05 meV/atom vs published, p95 0.17, max 16.86,
      100% classification agreement and zero flips. ORB reproduced with the YAML
      `max_force: 0.02`; the upstream runner default `force_max=0.05` failed the
      two-structure pre-smoke (`metric_check-layer-b-orb-v2-smoke500-fmax002.md`).
- [x] External-path self-audit: a fresh clone of this public repo, following the
      steps above verbatim (fresh venv + upstream clone + Figshare download),
      reproduces CHGNet Layer A exactly — 22/22 checks, 0 mismatches (run_log.md)
- [x] **Layer C — statistical audit** (`layer_c_statistical_audit.md`): bootstrap CIs
      + ranking significance, threshold sensitivity ±100 meV, cross-model error
      correlation / joint-blind-spot quantification, leaderboard-resolution analysis
      (43/59 adjacent pairs closer than one CI width)
- [x] External release packet added (`reports/external_release_packet.md`)
- [x] Paper-002 candidate selected and Layer A expanded across 14 JARVIS benchmarks:
      101/101 submissions reproduce official MAE/ACC/MULTIMAE within displayed
      rounding, with exact CSV-vs-JSON test-id agreement
      (`papers/jarvis-leaderboard/summary.md`)
- [x] JARVIS Layer B execution-path probe: current shared venv lacks the JARVIS
      runner stack, dependency dry-run succeeds, and public baseline scripts need
      light adaptation before a clean dft_3d smoke (`layer_b_probe.md`)
- [x] JARVIS Layer B bounded pre-smoke: isolated `env/jarvis`, 2048 train / 512 test
      dft_3d formation-energy slice, 273 Matminer features, 100-tree RF, 0 all-NaN
      feature rows, subset MAE 0.24470625 (`layer_b_matminer_rf_smoke.md`)
- [x] JARVIS leaderboard-resolution map: 87 adjacent pairs across the 14 checked
      pages; 29 gaps are <=0.005 and 38 are <=0.010 in metric units
      (`layer_c_resolution.md`)
- [x] JARVIS paired bootstrap on the 20 closest adjacent pairs: 17/20 95% CIs
      include zero under fixed-test-set resampling (`layer_c_bootstrap.md`)
- [x] Paper-003 candidate selected: Matbench v0.1, with public `results.json.gz`,
      `info.json`, and source/notebook artifacts in the official repo
- [x] Matbench Layer A seed passed: RF-SCM/Magpie `matbench_steels` +
      `matbench_expt_is_metal`, 10 folds checked, max score delta 1.110e-16
      (`papers/matbench/layer_a_score_recompute.md`)
- [x] Matbench classification ROC-AUC probe: 11/27 classification submission-task
      records store float predictions, but all stored `rocauc` values equal
      balanced accuracy; MODNet raw-probability AUC is higher by 0.030-0.122 mean
      AUC depending on task/version (`papers/matbench/classification_auc_probe.md`)
- [x] Matbench classification leaderboard display scan: all 3 classification
      per-task tables put `mean rocauc` first, and all 27 displayed rows have
      `mean rocauc == mean balanced_accuracy`
      (`papers/matbench/classification_leaderboard_metric_scan.md`)
- [x] Matbench upstream issue draft prepared for the classification `rocauc`
      behavior (`reports/paper-003_upstream_issue_draft.md`; draft only, not posted)
- [x] Matbench RF composition-task Layer A expanded: 4 tasks, 20 folds, max
      stored-vs-recomputed score delta 1.110e-16
      (`papers/matbench/layer_a_rf_composition_tasks.md`)
- [x] Matbench RF small-structure-task Layer A expanded: `matbench_jdft2d` +
      `matbench_phonons`, 10 folds, max stored-vs-recomputed score delta 0
      (`papers/matbench/layer_a_rf_structure_small_tasks.md`)
- [x] Matbench RF medium-structure-task Layer A expanded: `matbench_dielectric`,
      `matbench_log_gvrh`, `matbench_log_kvrh`, 15 folds, max
      stored-vs-recomputed score delta 0
      (`papers/matbench/layer_a_rf_structure_medium_tasks.md`)
- [x] Matbench RF all-task Layer A completed: 13 tasks, 65 folds, max
      stored-vs-recomputed score delta 1.776e-15
      (`papers/matbench/layer_a_rf_all_tasks.md`)
- [x] Matbench Dummy all-task Layer A completed: 13 tasks, 65 folds, max
      stored-vs-recomputed score delta 3.553e-15
      (`papers/matbench/layer_a_dummy_all_tasks.md`)
- [x] Matbench all-submission Layer A scan completed: 28 submissions, 180
      submission-task records, 900 folds; 179/180 records match to numerical
      precision, with one GN-OA `matbench_mp_e_form` MAPE-only exception
      (`papers/matbench/layer_a_all_submission_score_scan.md`)
- [x] Matbench GN-OA MAPE exception isolated: MAE/RMSE/max error match, stored
      MAPE only differs (`papers/matbench/layer_a_gn_oa_mape_probe.md`)
- [x] Matbench GN-OA MAPE upstream issue draft prepared
      (`reports/paper-003_gn_oa_mape_issue_draft.md`; draft only, not posted)
- [x] Matbench bounded Layer B source replay: TPOT-Mat `matbench_steels` notebook
      path runs end-to-end from the submitted pickle and helper, but does not
      regenerate the committed predictions exactly; seed-0 replay mean MAE 79.094
      vs submitted mean MAE 79.947 (`papers/matbench/layer_b_tpot_steels_replay.md`)
- [x] Matbench RFLR `matbench_steels` source replay: submitted notebook logic
      regenerates all five folds exactly under scikit-learn 1.2.2
      (`papers/matbench/layer_b_rflr_steels_replay.md`)
- [x] Matbench source artifact inventory: 28 submission directories scanned; 11
      direct `run.py` files, 14 notebooks, and only 1 pickle/joblib model artifact
      (`papers/matbench/source_artifact_inventory.md`)
- [x] Matbench Layer B candidate triage: selected `matbench_v0.1_RFLR`, then
      replayed it exactly; remaining positive-control target is `matbench_v0.1_dummy`
      (`papers/matbench/layer_b_candidate_triage.md`)
- [x] Paper-003 assembled report and external packet added
      (`reports/paper-003-matbench-audit.md`,
      `reports/paper-003-external_release_packet.md`)
- [ ] Next: decide whether to post the Matbench upstream issue drafts

## Paper-002 Candidate — JARVIS-Leaderboard

Initial target selected while Paper-001 upstream feedback is pending:
JARVIS-Leaderboard `AI/SinglePropertyPrediction/dft_3d_formation_energy_peratom`.
The first slice mirrors Paper-001 Layer A: recompute published MAE values directly
from the public JSON ground truth and CSV prediction zips, before any model execution.

Layer A result: 14 benchmark pages, 101 total submissions; all reproduce the
official MAE/ACC/MULTIMAE within displayed rounding, and every CSV id set exactly
matches the corresponding JSON test split.

Layer B pre-smoke: public runners exist but are not one-command fits for the audited
dft_3d target in the shared venv. In an isolated JARVIS env, a bounded
`matminer_rf`-style CPU smoke passed on a deterministic 2048 train / 512 test slice.

Layer C map: adjacent official point estimates are often close in the checked
pages: 29/87 adjacent gaps are <=0.005 and 38/87 are <=0.010 in metric units.
For the 20 closest adjacent pairs, a paired bootstrap over fixed public test rows
finds that 17/20 95% CIs include zero.

Artifacts:

- Assembled report: `reports/paper-002-jarvis-leaderboard-audit.md`
- External packet: `reports/paper-002-external_release_packet.md`
- Outreach draft: `reports/paper-002_outreach_draft.md`
- Upstream issue draft: `reports/paper-002_upstream_issue_draft.md`
- Summary: `papers/jarvis-leaderboard/summary.md`
- Plan: `papers/jarvis-leaderboard/reproduction_plan.md`
- Metadata: `papers/jarvis-leaderboard/metadata.yaml`
- Layer B probe: `papers/jarvis-leaderboard/layer_b_probe.md`
- Layer B pre-smoke: `papers/jarvis-leaderboard/layer_b_matminer_rf_smoke.md`
- Layer C resolution map: `papers/jarvis-leaderboard/layer_c_resolution.md`
- Layer C bootstrap: `papers/jarvis-leaderboard/layer_c_bootstrap.md`
- Metric check: `papers/jarvis-leaderboard/metric_check.md`
- Script: `scripts/jarvis_score.py`
- Layer B script: `scripts/jarvis_matminer_rf_smoke.py`
- Layer C script: `scripts/jarvis_resolution.py`
- Layer C bootstrap script: `scripts/jarvis_bootstrap.py`
- Report script: `scripts/make_jarvis_report.py`

## Paper-003 Candidate — Matbench v0.1

Initial target selected while Paper-001/Paper-002 upstream feedback is pending:
Matbench v0.1, using the official repository's committed leaderboard submission
artifacts. Each submission directory is expected to contain `results.json.gz`,
`info.json`, and source code or a notebook.

Layer A seed result: for `matbench_v0.1_rf`, `scripts/matbench_score.py`
recomputed all fold scores for the four low-cost composition tasks
(`matbench_expt_gap`, `matbench_expt_is_metal`, `matbench_glass`,
`matbench_steels`) plus two small structure tasks (`matbench_jdft2d`,
`matbench_phonons`) and three medium structure tasks (`matbench_dielectric`,
`matbench_log_gvrh`, `matbench_log_kvrh`) from released predictions, official split
IDs, and Matminer targets. The same check now passes on all 13 RF tasks and 65
folds, with max absolute delta 1.776e-15. The all-task check also passes for the
dummy baseline across another 65 folds, with max absolute delta 3.553e-15.
The all-submission scan covers 28 submissions, 180 submission-task records, and
900 folds; 179/180 records match to numerical precision, with one GN-OA
`matbench_mp_e_form` MAPE-only exception.

Classification metric probe: 11/27 classification submission-task records store
float predictions, but every checked stored `rocauc` value equals balanced accuracy.
For MODNet probability outputs on two small classification tasks, raw-probability
ROC-AUC is higher than the stored field by 0.030-0.122 mean AUC. The generated
classification per-task leaderboards display `mean rocauc` as the first metric
column.

Layer B source replay: `matbench_v0.1_TPOT` for `matbench_steels` can be executed
from the public notebook artifacts in a pinned TPOT/sklearn environment. It is not
prediction-identical: the notebook refits stochastic estimators without a submitted
random seed. With audit seed 0, replay mean MAE is 79.094 vs submitted mean MAE
79.947.

Second Layer B replay: `matbench_v0.1_RFLR` for `matbench_steels` is
prediction-identical under scikit-learn 1.2.2. The replay mirrors the submitted
regex composition featurizer and 30-tree random forest, with max prediction delta
0 and max score delta 0 across all five folds.

Layer B candidate triage: after TPOT-Mat, `matbench_v0.1_RFLR` was selected and
then replayed exactly; `matbench_v0.1_dummy` is the remaining positive-control
target.

Artifacts:

- Assembled report: `reports/paper-003-matbench-audit.md`
- External packet: `reports/paper-003-external_release_packet.md`
- Summary: `papers/matbench/summary.md`
- Plan: `papers/matbench/reproduction_plan.md`
- Metadata: `papers/matbench/metadata.yaml`
- Candidate screen: `papers/matbench/candidate_screen.md`
- Layer A seed report: `papers/matbench/layer_a_score_recompute.md`
- RF composition-task report: `papers/matbench/layer_a_rf_composition_tasks.md`
- RF small-structure-task report: `papers/matbench/layer_a_rf_structure_small_tasks.md`
- RF medium-structure-task report: `papers/matbench/layer_a_rf_structure_medium_tasks.md`
- RF all-task report: `papers/matbench/layer_a_rf_all_tasks.md`
- Dummy all-task report: `papers/matbench/layer_a_dummy_all_tasks.md`
- All-submission score scan: `papers/matbench/layer_a_all_submission_score_scan.md`
- GN-OA MAPE exception probe: `papers/matbench/layer_a_gn_oa_mape_probe.md`
- GN-OA MAPE issue draft: `reports/paper-003_gn_oa_mape_issue_draft.md`
- Classification AUC probe: `papers/matbench/classification_auc_probe.md`
- Classification prediction scan: `papers/matbench/classification_prediction_scan.md`
- Classification leaderboard metric scan:
  `papers/matbench/classification_leaderboard_metric_scan.md`
- Source artifact inventory: `papers/matbench/source_artifact_inventory.md`
- Layer B candidate triage: `papers/matbench/layer_b_candidate_triage.md`
- Layer B TPOT steels replay: `papers/matbench/layer_b_tpot_steels_replay.md`
- Layer B RFLR steels replay: `papers/matbench/layer_b_rflr_steels_replay.md`
- Classification ROC-AUC issue draft: `reports/paper-003_upstream_issue_draft.md`
- Script: `scripts/matbench_score.py`
- All-submission score scan script: `scripts/matbench_all_results_score_scan.py`
- Layer B replay script: `scripts/matbench_tpot_replay.py`
- Layer B RFLR replay script: `scripts/matbench_rflr_replay.py`
- Layer B triage script: `scripts/matbench_layer_b_candidate_triage.py`
- Classification scan script: `scripts/matbench_classification_scan.py`
- Leaderboard metric scan script: `scripts/matbench_leaderboard_metric_scan.py`
- Submission inventory script: `scripts/matbench_submission_inventory.py`
- Report script: `scripts/make_matbench_report.py`

## Rules
See `CLAUDE.md`. Short version: log every command, trace every metric to code,
no secrets, no bypass-permissions, no wet-lab, no materials generation.
