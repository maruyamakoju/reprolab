# ReproLab Paper-003 - Matbench v0.1 Audit

_Generated: 2026-07-04 13:35 UTC_

> Auto-assembled from tracked artifacts by `scripts/make_matbench_report.py`.

## 0. Executive summary

# Summary - Matbench v0.1 Paper-003 Candidate

Status: candidate selected; Layer A all-submission scan completed; bounded Layer B source replays and Layer C leaderboard-resolution map completed.

## Result

The first audit slice recomputes stored Matbench v0.1 fold scores from public
prediction artifacts rather than rerunning a model. For the RF-SCM/Magpie baseline
(`matbench_v0.1_rf`), `scripts/matbench_score.py` now checks all four low-cost
composition tasks:

| task | type | folds | max score delta |
|---|---|---:|---:|
| `matbench_expt_gap` | regression | 5 | 0 |
| `matbench_steels` | regression | 5 | 0 |
| `matbench_expt_is_metal` | classification | 5 | 1.110e-16 |
| `matbench_glass` | classification | 5 | 1.110e-16 |

Across all 20 checked folds, the max absolute stored-vs-recomputed score delta is
`1.1102230246251565e-16`.

Report: `layer_a_rf_composition_tasks.md`.

The RF baseline check now also covers two small structure tasks:
`matbench_jdft2d` and `matbench_phonons`. Across those 10 additional folds, the
max stored-vs-recomputed score delta is `0.0`.

Report: `layer_a_rf_structure_small_tasks.md`.

It also covers three medium structure tasks: `matbench_dielectric`,
`matbench_log_gvrh`, and `matbench_log_kvrh`. Across those 15 folds, the max
stored-vs-recomputed score delta is `0.0`.

Report: `layer_a_rf_structure_medium_tasks.md`.

Finally, the same scoring script was run over all 13 tasks in the RF baseline
artifact. Across all 65 folds, the max stored-vs-recomputed score delta is
`1.7763568394002505e-15`.

Report: `layer_a_rf_all_tasks.md`.

The all-task check was then repeated for the `matbench_v0.1_dummy` submission.
Across another 65 folds, the max stored-vs-recomputed score delta is
`3.552713678800501e-15`. The all-task Layer A scope is now 2 submissions, 26
submission-task pairs, and 130 folds.

Report: `layer_a_dummy_all_tasks.md`.

The final Layer A pass scans every local Matbench v0.1 `results.json.gz` artifact:
28 submissions, 180 submission-task records, and 900 folds. 179/180
submission-task records match stored scores to numerical precision. The only
exception is `matbench_v0.1_GN-OA` on `matbench_mp_e_form`: all five folds have
stored MAPE values that differ from recomputed Matbench MAPE, while MAE, RMSE, and
max error match exactly. All 135 classification folds in the scan have stored
`rocauc == balanced_accuracy`.

Report: `layer_a_all_submission_score_scan.md`.
Exception probe: `layer_a_gn_oa_mape_probe.md`.
Draft issue: `../../reports/paper-003_gn_oa_mape_issue_draft.md`.

## Layer B source replay

`scripts/matbench_submission_inventory.py` scanned 28 Matbench v0.1 submission
directories before the source replay. It found 11 direct `run.py` files, 14
notebook sources, and only one pickle/joblib model artifact. `matbench_v0.1_TPOT`
stands out as the best bounded replay candidate because it has one small task, a
notebook, a submitted helper, and a pickled TPOT pipeline.

After the TPOT replay, `scripts/matbench_layer_b_candidate_triage.py` ranked all
28 submissions for bounded source replays. It selected `matbench_v0.1_RFLR` as
the best nontrivial CPU target and `matbench_v0.1_dummy` as the low-novelty
positive-control target; both were then replayed.

Triage report: `layer_b_candidate_triage.md`.

The RFLR replay then mirrors the submitted notebook's regex composition featurizer
and `RandomForestRegressor(n_estimators=30, random_state=1)`. Under
`env/matbench-tpot` with scikit-learn `1.2.2`, it regenerates all five submitted
folds exactly: max prediction delta `0.0` and max score delta `0.0`. A logged
control run under `env/jarvis` with scikit-learn `1.9.0` was runnable but
non-identical, so this source replay is environment-sensitive.

RFLR replay report: `layer_b_rflr_steels_replay.md`.

The Dummy positive-control replay covers the four low-cost composition tasks. The
mean-regression dummy path is exact for all 10 checked regression folds. The
stratified classification dummy path is runnable but non-identical for all 10
checked classification folds under audit seed 0, as expected because the notebook
does not persist RNG state or set `DummyClassifier(random_state=...)`.

Dummy replay report: `layer_b_dummy_composition_replay.md`.

The first bounded source-execution probe targets `matbench_v0.1_TPOT`, a
notebook-based TPOT-Mat submission for `matbench_steels`. The replay script loads
the submitted `tpot_best_pipeline.pkl`, uses the submitted `utils.py` composition
cleaner, refits the pipeline on each official training fold, predicts the held-out
folds, and compares against the committed `results.json.gz`.

Outcome: the execution path is runnable in an isolated `env/matbench-tpot`
environment with `numpy==1.23.5`, `scikit-learn==1.2.2`, `tpot==0.11.7`, and
`xgboost==1.7.6`, but the submitted predictions are not regenerated exactly. With
audit seed 0, the five-fold replay has max absolute prediction delta `162.894`,
mean absolute prediction delta averaged across folds `17.893`, submitted mean MAE
`79.947`, and replay mean MAE `79.094`.

Interpretation: this is a useful Layer B smoke because the public source path can
be executed end-to-end. It is not a prediction-identical reproduction; the notebook
refits stochastic estimators without fixing a random seed.

Report: `layer_b_tpot_steels_replay.md`.

## Layer C leaderboard resolution

`scripts/matbench_leaderboard_resolution.py` ranks all 180 submission-task rows by
the primary stored metric (`mae` for regression, stored `rocauc` for
classification) and compares each adjacent mean gap with a fold-level standard
error proxy from the five paired fold-score differences.

Across 167 adjacent leaderboard pairs, 6 are exact ties, 68 have gaps no larger
than one fold-SE proxy, and 87 have gaps no larger than two fold-SE proxies. This
is a resolution screen, not a formal significance test. The classification caveat
remains: stored `rocauc` behaves as thresholded-label AUC / balanced accuracy for
the checked records.

Layer C report: `layer_c_leaderboard_resolution.md`.

A fold-bootstrap follow-up checks the 25 closest adjacent pairs from the
resolution map. All 25 have 95% bootstrap CIs that include zero, and all 25 have
`P(bootstrapped gap <= 0) >= 0.05`; 6 are exact adjacent ties in the stored fold
scores.

Layer C bootstrap report: `layer_c_fold_bootstrap.md`.

## Interpretation

This is a positive seed result: the RF baseline's saved predictions, official split
IDs, Matminer targets, and Matbench metric formulas are mutually consistent for one
small regression task and one small classification task.

The classification seed stores hard boolean predictions, so ROC-AUC equals balanced
accuracy. A follow-up scan found that 11/27 classification submission-task records
store float predictions, but every checked stored `rocauc` value is still equal to
balanced accuracy. The three classification per-task leaderboard tables also display
`mean rocauc` as the first metric column, with all 27 displayed rows equal to mean
balanced accuracy. For MODNet probability outputs, raw-probability ROC-AUC is higher
than the stored `rocauc` by 0.030-0.122 mean AUC depending on task/version. This is
reproducible from the Matbench v0.1 scoring order and is documented in
`classification_auc_probe.md`.

## Artifacts

- Assembled report: `../../reports/paper-003-matbench-audit.md`
- External packet: `../../reports/paper-003-external_release_packet.md`
- Plan: `reproduction_plan.md`
- Candidate screen: `candidate_screen.md`
- Metadata: `metadata.yaml`
- Layer A seed report: `layer_a_score_recompute.md`
- RF composition-task report: `layer_a_rf_composition_tasks.md`
- RF small-structure-task report: `layer_a_rf_structure_small_tasks.md`
- RF medium-structure-task report: `layer_a_rf_structure_medium_tasks.md`
- RF all-task report: `layer_a_rf_all_tasks.md`
- Dummy all-task report: `layer_a_dummy_all_tasks.md`
- All-submission score scan: `layer_a_all_submission_score_scan.md`
- GN-OA MAPE exception probe: `layer_a_gn_oa_mape_probe.md`
- GN-OA MAPE issue draft: `../../reports/paper-003_gn_oa_mape_issue_draft.md`
- Classification AUC probe: `classification_auc_probe.md`
- Classification prediction scan: `classification_prediction_scan.md`
- Classification leaderboard metric scan: `classification_leaderboard_metric_scan.md`
- Source artifact inventory: `source_artifact_inventory.md`
- Layer B candidate triage: `layer_b_candidate_triage.md`
- Layer B TPOT steels replay: `layer_b_tpot_steels_replay.md`
- Layer B RFLR steels replay: `layer_b_rflr_steels_replay.md`
- Layer B Dummy composition replay: `layer_b_dummy_composition_replay.md`
- Layer C leaderboard resolution: `layer_c_leaderboard_resolution.md`
- Layer C fold bootstrap: `layer_c_fold_bootstrap.md`
- Classification ROC-AUC issue draft: `../../reports/paper-003_upstream_issue_draft.md`
- Script: `../../scripts/matbench_score.py`
- All-submission score scan script: `../../scripts/matbench_all_results_score_scan.py`
- Layer B replay script: `../../scripts/matbench_tpot_replay.py`
- Layer B RFLR replay script: `../../scripts/matbench_rflr_replay.py`
- Layer B Dummy replay script: `../../scripts/matbench_dummy_replay.py`
- Layer B triage script: `../../scripts/matbench_layer_b_candidate_triage.py`
- Layer C resolution script: `../../scripts/matbench_leaderboard_resolution.py`
- Layer C bootstrap script: `../../scripts/matbench_leaderboard_fold_bootstrap.py`
- Classification scan script: `../../scripts/matbench_classification_scan.py`
- Leaderboard metric scan script: `../../scripts/matbench_leaderboard_metric_scan.py`
- Submission inventory script: `../../scripts/matbench_submission_inventory.py`
- Report script: `../../scripts/make_matbench_report.py`
- Run log: `run_log.md`



## 1. Benchmark metadata

```
# ReproLab Paper-003 candidate - Matbench v0.1
paper:
  title: "Benchmarking Materials Property Prediction Methods: The Matbench Test Set and Automatminer Reference Algorithm"
  venue: npj Computational Materials
  volume_article: 6, 138
  year: 2020
  doi: https://doi.org/10.1038/s41524-020-00406-3

benchmark:
  name: Matbench v0.1
  repo: https://github.com/materialsproject/matbench
  repo_commit_pinned: 936176db18ca4cd7b38cbd957c017a5bac770c6b
  website: https://matbench.materialsproject.org
  docs_submission: https://matbench.materialsproject.org/How%20To%20Use/3submit/
  benchmark_info: https://matbench.materialsproject.org/Benchmark%20Info/matbench_v0.1/
  license: modified BSD license file in upstream repo
  domain: materials property prediction benchmarks
  tasks: 13

reports:
  assembled_report: reports/paper-003-matbench-audit.md
  external_packet: reports/paper-003-external_release_packet.md
  report_script: scripts/make_matbench_report.py

artifact_model:
  required_submission_files:
    - results.json.gz
    - info.json
    - source code or notebook
  local_submission_root: vendor/matbench/benchmarks
  seed_submission: matbench_v0.1_rf
  seed_results: vendor/matbench/benchmarks/matbench_v0.1_rf/results.json.gz

task_under_audit:
  layer_a_seed_tasks:
    - matbench_steels
    - matbench_expt_is_metal
  metrics_regression:
    - mae
    - rmse
    - mape
    - max_error
  metrics_classification:
    - accuracy
    - balanced_accuracy
    - f1
    - rocauc

layer_a_seed:
  status: passed
  script: scripts/matbench_score.py
  report: papers/matbench/layer_a_score_recompute.md
  environment: env/jarvis
  submission: matbench_v0.1_rf
  tasks_checked: 2
  folds_checked: 10
  max_abs_stored_vs_recomputed_delta: 1.1102230246251565e-16

layer_a_rf_composition:
  status: passed
  script: scripts/matbench_score.py
  report: papers/matbench/layer_a_rf_composition_tasks.md
  environment: env/jarvis
  submission: matbench_v0.1_rf
  tasks_checked: 4
  folds_checked: 20
  tasks:
    - matbench_expt_gap
    - matbench_expt_is_metal
    - matbench_glass
    - matbench_steels
  max_abs_stored_vs_recomputed_delta: 1.1102230246251565e-16

layer_a_rf_small_structure:
  status: passed
  script: scripts/matbench_score.py
  report: papers/matbench/layer_a_rf_structure_small_tasks.md
  environment: env/jarvis
  submission: matbench_v0.1_rf
  tasks_checked: 2
  folds_checked: 10
  tasks:
    - matbench_jdft2d
    - matbench_phonons
  max_abs_stored_vs_recomputed_delta: 0.0

layer_a_rf_medium_structure:
  status: passed
  script: scripts/matbench_score.py
  report: papers/matbench/layer_a_rf_structure_medium_tasks.md
  environment: env/jarvis
  submission: matbench_v0.1_rf
  tasks_checked: 3
  folds_checked: 15
  tasks:
    - matbench_dielectric
    - matbench_log_gvrh
    - matbench_log_kvrh
  max_abs_stored_vs_recomputed_delta: 0.0

layer_a_rf_all_tasks:
  status: passed
  script: scripts/matbench_score.py
  report: papers/matbench/layer_a_rf_all_tasks.md
  environment: env/jarvis
  submission: matbench_v0.1_rf
  tasks_checked: 13
  folds_checked: 65
  max_abs_stored_vs_recomputed_delta: 1.7763568394002505e-15

layer_a_dummy_all_tasks:
  status: passed
  script: scripts/matbench_score.py
  report: papers/matbench/layer_a_dummy_all_tasks.md
  environment: env/jarvis
  submission: matbench_v0.1_dummy
  tasks_checked: 13
  folds_checked: 65
  max_abs_stored_vs_recomputed_delta: 3.552713678800501e-15

layer_a_all_submission_score_scan:
  status: completed_with_one_mape_only_exception
  script: scripts/matbench_all_results_score_scan.py
  report: papers/matbench/layer_a_all_submission_score_scan.md
  environment: env/jarvis
  submissions_checked: 28
  submission_task_records_checked: 180
  folds_checked: 900
  max_abs_stored_vs_recomputed_delta: 12.168624707070679
  failing_folds_at_1e_12: 5
  failing_submission: matbench_v0.1_GN-OA
  failing_task: matbench_mp_e_form
  failing_metric: mape
  passing_submission_task_records: 179
  classification_folds_checked: 135
  classification_folds_rocauc_equal_balanced_accuracy: 135
  exception_probe: papers/matbench/layer_a_gn_oa_mape_probe.md
  exception_issue_draft: reports/paper-003_gn_oa_mape_issue_draft.md

classification_auc_probe:
  status: completed
  scan_script: scripts/matbench_classification_scan.py
  scan_report: papers/matbench/classification_prediction_scan.md
  finding_report: papers/matbench/classification_auc_probe.md
  upstream_issue_draft: reports/paper-003_upstream_issue_draft.md
  classification_submission_task_records: 27
  all_bool_records: 16
  all_float_records: 11
  mixed_records: 0
  records_where_stored_rocauc_differs_from_balanced_accuracy: 0
  leaderboard_scan_script: scripts/matbench_leaderboard_metric_scan.py
  leaderboard_scan_report: papers/matbench/classification_leaderboard_metric_scan.md
  classification_leaderboard_tables: 3
  classification_leaderboard_rows: 27
  displayed_rocauc_rows_differing_from_balanced_accuracy: 0
  modnet_probability_auc_probe:
    modnet_v0_1_10:
      expt_is_metal_stored_mean: 0.9160515032798
      expt_is_metal_probability_auc_mean: 0.9725462640508
      glass_stored_mean: 0.810676338874
      glass_probability_auc_mean: 0.9329484035962
    modnet_v0_1_12:
      expt_is_metal_stored_mean: 0.9160515032798
      expt_is_metal_probability_auc_mean: 0.9725462640508
      glass_stored_mean: 0.9603111829242
      glass_probability_auc_mean: 0.9898761972560001

source_artifact_inventory:
  status: completed
  script: scripts/matbench_submission_inventory.py
  report: papers/matbench/source_artifact_inventory.md
  submission_directories_scanned: 28
  direct_run_py_files: 11
  notebook_sources: 14
  pickle_or_joblib_model_artifacts: 1
  best_bounded_replay_candidate: matbench_v0.1_TPOT

layer_b_candidate_triage:
  status: completed
  script: scripts/matbench_layer_b_candidate_triage.py
  report: papers/matbench/layer_b_candidate_triage.md
  submissions_checked: 28
  already_replayed:
    - matbench_v0.1_TPOT
    - matbench_v0.1_RFLR
    - matbench_v0.1_dummy
  selected_nontrivial_cpu_replay_candidate: matbench_v0.1_RFLR
  selected_candidate_task: matbench_steels
  selected_candidate_priority_before_replay: high
  selected_candidate_score: 78
  selected_candidate_replay_result: prediction_identical
  positive_control_replay: matbench_v0.1_dummy
  positive_control_replay_scope: low_cost_composition_subset
  medium_priority_candidates: 1
  low_priority_candidates: 24

layer_b_tpot_steels:
  status: source_replay_completed_non_identical
  script: scripts/matbench_tpot_replay.py
  report: papers/matbench/layer_b_tpot_steels_replay.md
  environment: env/matbench-tpot
  submission: matbench_v0.1_TPOT
  task: matbench_steels
  folds_replayed: 5
  audit_random_seed: 0
  max_abs_prediction_delta: 162.894287109375
  mean_abs_prediction_delta_mean_across_folds: 17.89280359568
  submitted_mae_mean: 79.94681065716
  replay_mae_mean: 79.09383529924
  max_abs_score_delta: 24.770214843749955
  max_mae_delta: 5.20293162512
  interpretation: runnable notebook path, but submitted predictions are not exactly regenerated because the source refits unseeded stochastic estimators

layer_b_rflr_steels:
  status: source_replay_prediction_identical
  script: scripts/matbench_rflr_replay.py
  report: papers/matbench/layer_b_rflr_steels_replay.md
  environment: env/matbench-tpot
  sklearn_version: 1.2.2
  submission: matbench_v0.1_RFLR
  task: matbench_steels
  folds_replayed: 5
  max_abs_prediction_delta: 0.0
  max_abs_score_delta: 0.0
  version_sensitivity_check:
    environment: env/jarvis
    sklearn_version: 1.9.0
    max_abs_prediction_delta: 108.58666666666704
    max_abs_score_delta: 22.306666666666843
  interpretation: notebook source path regenerates committed predictions exactly under the checked sklearn 1.2.2 environment

layer_b_dummy_composition:
  status: source_replay_regression_exact_classification_non_identical
  script: scripts/matbench_dummy_replay.py
  report: papers/matbench/layer_b_dummy_composition_replay.md
  environment: env/matbench-tpot
  sklearn_version: 1.2.2
  submission: matbench_v0.1_dummy
  tasks:
    - matbench_expt_gap
    - matbench_expt_is_metal
    - matbench_glass
    - matbench_steels
  folds_replayed: 20
  exact_prediction_and_score_folds: 10
  regression_exact_folds: 10
  classification_exact_folds: 0
  max_prediction_delta_or_mismatch_rate: 0.5020325203252033
  max_score_delta: 0.04486766627873349
  audit_numpy_seed: 0
  interpretation: mean-regression dummy replay is exact, stratified classification replay is non-identical because the notebook did not persist RNG state

layer_c_leaderboard_resolution:
  status: completed
  script: scripts/matbench_leaderboard_resolution.py
  report: papers/matbench/layer_c_leaderboard_resolution.md
  submission_task_rows_ranked: 180
  tasks_ranked: 13
  adjacent_pairs: 167
  exact_adjacent_ties: 6
  adjacent_gaps_lte_1_fold_se_proxy: 68
  adjacent_gaps_lte_2_fold_se_proxy: 87
  regression_adjacent_pairs: 143
  classification_adjacent_pairs: 24
  primary_metric_regression: mae
  primary_metric_classification: stored rocauc
  classification_metric_caveat: stored rocauc behaves as thresholded-label AUC / balanced accuracy for checked records
  interpretation: leaderboard-resolution screen, not a formal significance test

layer_c_fold_bootstrap:
  status: completed
  script: scripts/matbench_leaderboard_fold_bootstrap.py
  report: papers/matbench/layer_c_fold_bootstrap.md
  source_resolution_report: papers/matbench/layer_c_leaderboard_resolution.md
  adjacent_pairs_checked: 25
  bootstrap_draws_per_pair: 20000
  rng_seed: 0
  bootstrap_ci_95_including_zero: 25
  p_bootstrapped_gap_lte_zero_gte_0_05: 25
  exact_adjacent_ties_in_checked_set: 6
  interpretation: all closest adjacent pairs are unresolved under this coarse five-fold bootstrap screen

candidate_screen:
  status: selected
  report: papers/matbench/candidate_screen.md
  reason: public results.json.gz artifacts, info.json metadata, and source files are committed for many leaderboard submissions
  main_risk: full all-task verification can require loading large structure datasets

```


## 2. Candidate screen

# Paper-003 candidate screen - Matbench v0.1

Status: selected as the next audit target on 2026-07-03.

## Why this candidate

Matbench v0.1 is a strong Paper-003 candidate because the official repository
commits the exact leaderboard submission artifacts needed for a CPU-first audit:
`results.json.gz`, `info.json`, and source code or notebooks under
`benchmarks/matbench_v0.1_*`.

The official submission docs require those three artifacts for leaderboard
submissions. The repository also includes the benchmark metadata JSON and
validation split JSON, while the targets are loadable through Matminer datasets.
That gives the same first move used in Paper-001 and Paper-002: recompute published
scores from released predictions before attempting model execution.

## Initial slice

Seed submission: `matbench_v0.1_rf` (RF-SCM/Magpie reference baseline).

Seed tasks:

| task | type | rows | reason |
|---|---|---:|---|
| `matbench_steels` | regression | 312 | small composition task; fast target load |
| `matbench_expt_is_metal` | classification | 4,921 | small classification task; checks non-regression metrics |

Result: `scripts/matbench_score.py` recomputed 10 fold scores from
`results.json.gz`, official split IDs, and Matminer targets. The max absolute
stored-vs-recomputed score delta is `1.1102230246251565e-16`.

Report: `layer_a_score_recompute.md`.

## Candidate comparison

| candidate | disposition | reason |
|---|---|---|
| Matbench v0.1 | selected | public prediction artifacts and source files are committed per submission |
| Open Catalyst Project | defer | scientifically strong but larger data/model path and less direct for a quick prediction-artifact audit |
| Open MatSci ML Toolkit | defer | useful framework, but less direct as a single leaderboard-with-predictions target |
| matbench-genmetrics | defer | relevant to generative materials evaluation, but the current audit line is property-prediction leaderboard reproducibility |

## Risks and notes

- Full all-task score recomputation can become heavy because the structure tasks
  include large pymatgen object datasets.
- The shared `.venv` lacks `matminer`; the current seed uses the already available
  isolated `env/jarvis`. A dedicated `env/matbench` can be created if this audit
  grows.
- `scripts/run_command.py` originally used second-level raw-log names; two parallel
  commands collided while scouting. It now uses microsecond-level names.
- The first runnable source-code candidate is `matbench_v0.1_TPOT`. Its notebook
  path can be replayed for `matbench_steels`, but it refits stochastic estimators
  without a submitted random seed, so public-source execution does not regenerate
  the committed predictions exactly.
- `source_artifact_inventory.md` records the broader source-artifact scan: 28
  submission directories, 11 direct `run.py` files, 14 notebooks, and one
  pickle/joblib model artifact.



## 3. Reproduction plan

# Reproduction Plan - Matbench v0.1 (Paper-003 candidate)

Status: candidate selected and Layer A seed passed on 2026-07-03.

## 0. Why this candidate

Matbench v0.1 has 13 curated materials property prediction tasks and many public
leaderboard submissions. The upstream repository stores submission directories
under `benchmarks/`, each with `results.json.gz`, `info.json`, and source code or
a notebook. This makes it possible to audit the published scores directly from
released prediction artifacts.

## 1. Initial target

Submission:
`vendor/matbench/benchmarks/matbench_v0.1_rf/results.json.gz`

Tasks:

| task | type | metric family | folds |
|---|---|---|---:|
| `matbench_steels` | regression | MAE/RMSE/MAPE/max error | 5 |
| `matbench_expt_is_metal` | classification | accuracy/balanced accuracy/F1/ROC-AUC | 5 |

## 2. Metric path

Released artifact:
`results.json.gz` stores, for each task and fold, an ID-to-prediction map plus the
stored fold scores.

Truth source:

1. `vendor/matbench/matbench/matbench_v0.1_dataset_metadata.json` gives the target
   column and task type.
2. `vendor/matbench/matbench/matbench_v0.1_validation.json` gives the official
   train/test split IDs.
3. `matminer.datasets.load_dataset(task)` loads the raw target data.
4. Matbench IDs are regenerated with the upstream convention
   `matbench_* -> mb-*` plus 1-indexed zero-padded row numbers.

Scoring:

- Regression: MAE, RMSE, masked MAPE with `abs(y_true) > 1e-5`, max absolute error.
- Classification: accuracy, balanced accuracy, F1, ROC-AUC following the Matbench
  v0.1 metric order and threshold behavior.
- Fold aggregates use NumPy `mean`, `max`, `min`, and population `std`.

Script:
`scripts/matbench_score.py`

## 3. Command

```bash
python scripts/run_command.py --paper matbench \
  --note "paper003 recompute Matbench RF scores for steels and expt_is_metal" -- \
  env/jarvis/Scripts/python.exe scripts/matbench_score.py \
    --results vendor/matbench/benchmarks/matbench_v0.1_rf/results.json.gz \
    --tasks matbench_steels matbench_expt_is_metal \
    --report papers/matbench/layer_a_score_recompute.md
```

## 4. Pass criteria

- Prediction IDs exactly match the official validation split test IDs for every
  checked fold.
- Recomputed fold scores match stored fold scores to numerical precision
  (`max_abs_delta < 1e-12`).
- Any mismatch becomes a blocker note before broadening the audit.

## 5. Current result

The seed check passed:

| submission | tasks | folds | max absolute score delta | report |
|---|---:|---:|---:|---|
| `matbench_v0.1_rf` | 2 | 10 | 1.110e-16 | `layer_a_score_recompute.md` |
| `matbench_v0.1_rf` composition tasks | 4 | 20 | 1.110e-16 | `layer_a_rf_composition_tasks.md` |
| `matbench_v0.1_rf` small structure tasks | 2 | 10 | 0.000e+00 | `layer_a_rf_structure_small_tasks.md` |
| `matbench_v0.1_rf` medium structure tasks | 3 | 15 | 0.000e+00 | `layer_a_rf_structure_medium_tasks.md` |
| `matbench_v0.1_rf` all tasks | 13 | 65 | 1.776e-15 | `layer_a_rf_all_tasks.md` |
| `matbench_v0.1_dummy` all tasks | 13 | 65 | 3.553e-15 | `layer_a_dummy_all_tasks.md` |
| all local submissions | 180 submission-task records | 900 | 12.169 MAPE-only exception | `layer_a_all_submission_score_scan.md` |

The classification predictions in the RF baseline are stored as hard booleans, so
the stored ROC-AUC equals balanced accuracy for the checked classification task.

## 6. Classification ROC-AUC probe

`scripts/matbench_classification_scan.py` inspected the classification prediction
types in every local public submission artifact. It found 27 classification
submission-task records: 16 all-bool, 11 all-float, 0 mixed. In all 27 records,
stored `rocauc` equals balanced accuracy within numerical precision.

For two small MODNet classification tasks, `scripts/matbench_score.py` also computed
ROC-AUC using the raw float predictions. Stored fold scores still reproduced exactly,
but probability ROC-AUC was higher than the stored `rocauc`:

| submission | task | stored rocauc mean | probability rocauc mean | mean gap |
|---|---|---:|---:|---:|
| `matbench_v0.1_modnet_v0.1.10` | `matbench_expt_is_metal` | 0.916052 | 0.972546 | 0.056495 |
| `matbench_v0.1_modnet_v0.1.10` | `matbench_glass` | 0.810676 | 0.932948 | 0.122272 |
| `matbench_v0.1_modnet_v0.1.12` | `matbench_expt_is_metal` | 0.916052 | 0.972546 | 0.056495 |
| `matbench_v0.1_modnet_v0.1.12` | `matbench_glass` | 0.960311 | 0.989876 | 0.029565 |

Interpretation: the stored scores are reproducible, but the `rocauc` field appears
to be thresholded-label AUC for float-prediction submissions because the Matbench
v0.1 metric loop converts predictions to labels before reaching `rocauc`.

Reports:

- `classification_prediction_scan.md`
- `classification_leaderboard_metric_scan.md`
- `classification_auc_probe.md`
- `layer_a_modnet_0_1_10_probability_auc_probe.md`
- `layer_a_modnet_0_1_12_probability_auc_probe.md`

## 7. Bounded Layer B source replay

Submission:
`vendor/matbench/benchmarks/matbench_v0.1_TPOT`

Task:
`matbench_steels`

Environment setup used:

```bash
python -m venv env/matbench-tpot
env/matbench-tpot/Scripts/python.exe -m pip install \
  numpy==1.23.5 scipy scikit-learn==1.2.2 xgboost==1.7.6 pandas==1.5.1
env/matbench-tpot/Scripts/python.exe -m pip install \
  tpot==0.11.7 deap update_checker tqdm stopit
env/matbench-tpot/Scripts/python.exe -m pip install numpy==1.23.5 --force-reinstall
```

The final numpy reinstall is needed because the TPOT import dependencies pulled a
newer numpy that is ABI-incompatible with `scikit-learn==1.2.2`.

Command:

```bash
python scripts/run_command.py --paper matbench \
  --note "paper003 replay TPOT steels all folds seeded" -- \
  env/matbench-tpot/Scripts/python.exe scripts/matbench_tpot_replay.py \
    --report papers/matbench/layer_b_tpot_steels_replay.md \
    --seed 0
```

Result: the notebook execution path is runnable when using an environment close to
the submitted requirements (`numpy==1.23.5`, `scikit-learn==1.2.2`,
`tpot==0.11.7`, `xgboost==1.7.6`). The replay loads the submitted TPOT pickle,
uses the submitted composition-cleaning helper, refits each fold, predicts the
held-out split, and compares against the committed predictions.

The replay is not prediction-identical. With audit seed 0, max absolute prediction
delta is `162.894`, the mean absolute prediction delta averaged across folds is
`17.893`, submitted mean MAE is `79.947`, and replay mean MAE is `79.094`. The
source notebook does not set a random seed while refitting stochastic estimators,
so exact prediction regeneration is not expected from the public artifact alone.

Report:
`layer_b_tpot_steels_replay.md`

## 8. Next

1. Post the upstream issue only if the user explicitly asks.
2. Optionally broaden Layer A to selected structure tasks if compute/data download
   cost is acceptable.
3. If deeper Layer B is needed, choose submissions with fixed seeds or saved
   fold-level model artifacts before attempting larger structure tasks.



## 4. Layer A seed score recomputation

# Matbench v0.1 score recomputation

- Results artifact: `vendor/matbench/benchmarks/matbench_v0.1_rf/results.json.gz`
- Fold scores checked: 10
- Max absolute stored-vs-recomputed score delta: 1.110e-16

## Fold checks

| Task | Fold | n | Prediction type | Max score delta | Stored rocauc | Probability rocauc |
|---|---:|---:|---|---:|---:|---:|
| matbench_steels | 0 | 63 | float | 0.000e+00 |  |  |
| matbench_steels | 1 | 63 | float | 0.000e+00 |  |  |
| matbench_steels | 2 | 62 | float | 0.000e+00 |  |  |
| matbench_steels | 3 | 62 | float | 0.000e+00 |  |  |
| matbench_steels | 4 | 62 | float | 0.000e+00 |  |  |
| matbench_expt_is_metal | 0 | 985 | bool | 0.000e+00 | 0.924829110219 |  |
| matbench_expt_is_metal | 1 | 984 | bool | 0.000e+00 | 0.916632239941 |  |
| matbench_expt_is_metal | 2 | 984 | bool | 1.110e-16 | 0.909481120383 |  |
| matbench_expt_is_metal | 3 | 984 | bool | 1.110e-16 | 0.922746426506 |  |
| matbench_expt_is_metal | 4 | 984 | bool | 1.110e-16 | 0.909605056598 |  |

## Recomputed fold aggregates

### matbench_steels

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| mae | 103.512486062 | 114.63311746 | 85.6694031746 | 11.0367786926 |
| rmse | 149.383944441 | 196.358570629 | 113.154922817 | 27.4893431478 |
| mape | 0.0744721297401 | 0.0807437889227 | 0.0653807405884 | 0.0056047478171 |
| max_error | 594.98156 | 1121.1276 | 362.663 | 278.700159881 |

### matbench_expt_is_metal

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| accuracy | 0.916681936363 | 0.924873096447 | 0.909552845528 | 0.00641463134 |
| balanced_accuracy | 0.916658790729 | 0.924829110219 | 0.909481120383 | 0.00640450234832 |
| f1 | 0.915855162513 | 0.923553719008 | 0.907580477674 | 0.00628063358071 |
| rocauc | 0.916658790729 | 0.924829110219 | 0.909481120383 | 0.00640450234832 |



## 4b. Layer A RF composition-task expansion

# Matbench v0.1 score recomputation

- Results artifact: `vendor/matbench/benchmarks/matbench_v0.1_rf/results.json.gz`
- Fold scores checked: 20
- Max absolute stored-vs-recomputed score delta: 1.110e-16

## Fold checks

| Task | Fold | n | Prediction type | Max score delta | Stored rocauc | Probability rocauc |
|---|---:|---:|---|---:|---:|---:|
| matbench_expt_gap | 0 | 921 | float | 0.000e+00 |  |  |
| matbench_expt_gap | 1 | 921 | float | 0.000e+00 |  |  |
| matbench_expt_gap | 2 | 921 | float | 0.000e+00 |  |  |
| matbench_expt_gap | 3 | 921 | float | 0.000e+00 |  |  |
| matbench_expt_gap | 4 | 920 | float | 0.000e+00 |  |  |
| matbench_expt_is_metal | 0 | 985 | bool | 0.000e+00 | 0.924829110219 |  |
| matbench_expt_is_metal | 1 | 984 | bool | 0.000e+00 | 0.916632239941 |  |
| matbench_expt_is_metal | 2 | 984 | bool | 1.110e-16 | 0.909481120383 |  |
| matbench_expt_is_metal | 3 | 984 | bool | 1.110e-16 | 0.922746426506 |  |
| matbench_expt_is_metal | 4 | 984 | bool | 1.110e-16 | 0.909605056598 |  |
| matbench_glass | 0 | 1136 | bool | 0.000e+00 | 0.886006937775 |  |
| matbench_glass | 1 | 1136 | bool | 0.000e+00 | 0.840239093344 |  |
| matbench_glass | 2 | 1136 | bool | 1.110e-16 | 0.849521474334 |  |
| matbench_glass | 3 | 1136 | bool | 1.110e-16 | 0.852619367766 |  |
| matbench_glass | 4 | 1136 | bool | 0.000e+00 | 0.865116401698 |  |
| matbench_steels | 0 | 63 | float | 0.000e+00 |  |  |
| matbench_steels | 1 | 63 | float | 0.000e+00 |  |  |
| matbench_steels | 2 | 62 | float | 0.000e+00 |  |  |
| matbench_steels | 3 | 62 | float | 0.000e+00 |  |  |
| matbench_steels | 4 | 62 | float | 0.000e+00 |  |  |

## Recomputed fold aggregates

### matbench_expt_gap

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| mae | 0.446054992487 | 0.481156868621 | 0.434542420557 | 0.0176552424643 |
| rmse | 0.824300735345 | 0.943523224093 | 0.781867354239 | 0.0601326123053 |
| mape | 0.369492377556 | 0.43851001849 | 0.304356979438 | 0.0470475962382 |
| max_error | 6.046496 | 9.5428 | 4.71216 | 1.76997564717 |

### matbench_expt_is_metal

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| accuracy | 0.916681936363 | 0.924873096447 | 0.909552845528 | 0.00641463134 |
| balanced_accuracy | 0.916658790729 | 0.924829110219 | 0.909481120383 | 0.00640450234832 |
| f1 | 0.915855162513 | 0.923553719008 | 0.907580477674 | 0.00628063358071 |
| rocauc | 0.916658790729 | 0.924829110219 | 0.909481120383 | 0.00640450234832 |

### matbench_glass

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| accuracy | 0.895422535211 | 0.919894366197 | 0.884683098592 | 0.0130969823334 |
| balanced_accuracy | 0.858700654983 | 0.886006937775 | 0.840239093344 | 0.0158041991609 |
| f1 | 0.927798088561 | 0.944881889764 | 0.919975565058 | 0.00908698827732 |
| rocauc | 0.858700654983 | 0.886006937775 | 0.840239093344 | 0.0158041991609 |

### matbench_steels

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| mae | 103.512486062 | 114.63311746 | 85.6694031746 | 11.0367786926 |
| rmse | 149.383944441 | 196.358570629 | 113.154922817 | 27.4893431478 |
| mape | 0.0744721297401 | 0.0807437889227 | 0.0653807405884 | 0.0056047478171 |
| max_error | 594.98156 | 1121.1276 | 362.663 | 278.700159881 |



## 4c. Layer A RF small-structure-task expansion

# Matbench v0.1 score recomputation

- Results artifact: `vendor/matbench/benchmarks/matbench_v0.1_rf/results.json.gz`
- Fold scores checked: 10
- Max absolute stored-vs-recomputed score delta: 0.000e+00

## Fold checks

| Task | Fold | n | Prediction type | Max score delta | Stored rocauc | Probability rocauc |
|---|---:|---:|---|---:|---:|---:|
| matbench_jdft2d | 0 | 128 | float | 0.000e+00 |  |  |
| matbench_jdft2d | 1 | 127 | float | 0.000e+00 |  |  |
| matbench_jdft2d | 2 | 127 | float | 0.000e+00 |  |  |
| matbench_jdft2d | 3 | 127 | float | 0.000e+00 |  |  |
| matbench_jdft2d | 4 | 127 | float | 0.000e+00 |  |  |
| matbench_phonons | 0 | 253 | float | 0.000e+00 |  |  |
| matbench_phonons | 1 | 253 | float | 0.000e+00 |  |  |
| matbench_phonons | 2 | 253 | float | 0.000e+00 |  |  |
| matbench_phonons | 3 | 253 | float | 0.000e+00 |  |  |
| matbench_phonons | 4 | 253 | float | 0.000e+00 |  |  |

## Recomputed fold aggregates

### matbench_jdft2d

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| mae | 50.04399974 | 66.2421301222 | 42.7472945267 | 8.62712887611 |
| rmse | 112.265975486 | 159.638986052 | 72.7391490957 | 36.7066225573 |
| mape | 5.23911546788 | 23.7624894676 | 0.43823538542 | 9.26294774418 |
| max_error | 718.045733692 | 1538.60726856 | 295.743678511 | 453.647322018 |

### matbench_phonons

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| mae | 67.6126142422 | 82.3862649649 | 58.6036107598 | 8.9899908374 |
| rmse | 146.276431864 | 172.801458959 | 122.15658115 | 21.4751689658 |
| mape | 0.118485135116 | 0.134769893668 | 0.104049045388 | 0.00979558791325 |
| max_error | 1270.68885897 | 2024.7301119 | 861.90049904 | 402.730658047 |



## 4d. Layer A RF medium-structure-task expansion

# Matbench v0.1 score recomputation

- Results artifact: `vendor/matbench/benchmarks/matbench_v0.1_rf/results.json.gz`
- Fold scores checked: 15
- Max absolute stored-vs-recomputed score delta: 0.000e+00

## Fold checks

| Task | Fold | n | Prediction type | Max score delta | Stored rocauc | Probability rocauc |
|---|---:|---:|---|---:|---:|---:|
| matbench_dielectric | 0 | 953 | float | 0.000e+00 |  |  |
| matbench_dielectric | 1 | 953 | float | 0.000e+00 |  |  |
| matbench_dielectric | 2 | 953 | float | 0.000e+00 |  |  |
| matbench_dielectric | 3 | 953 | float | 0.000e+00 |  |  |
| matbench_dielectric | 4 | 952 | float | 0.000e+00 |  |  |
| matbench_log_gvrh | 0 | 2198 | float | 0.000e+00 |  |  |
| matbench_log_gvrh | 1 | 2198 | float | 0.000e+00 |  |  |
| matbench_log_gvrh | 2 | 2197 | float | 0.000e+00 |  |  |
| matbench_log_gvrh | 3 | 2197 | float | 0.000e+00 |  |  |
| matbench_log_gvrh | 4 | 2197 | float | 0.000e+00 |  |  |
| matbench_log_kvrh | 0 | 2198 | float | 0.000e+00 |  |  |
| matbench_log_kvrh | 1 | 2198 | float | 0.000e+00 |  |  |
| matbench_log_kvrh | 2 | 2197 | float | 0.000e+00 |  |  |
| matbench_log_kvrh | 3 | 2197 | float | 0.000e+00 |  |  |
| matbench_log_kvrh | 4 | 2197 | float | 0.000e+00 |  |  |

## Recomputed fold aggregates

### matbench_dielectric

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| mae | 0.419578159259 | 0.52198700518 | 0.304162451401 | 0.0750037451263 |
| rmse | 1.85382481618 | 2.98323049778 | 0.785044337763 | 0.770049375991 |
| mape | 0.139968218264 | 0.188632999374 | 0.10574510663 | 0.0288667979365 |
| max_error | 34.8805599225 | 59.1201445981 | 14.5978573183 | 16.9979726853 |

### matbench_log_gvrh

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| mae | 0.103998778594 | 0.106730986524 | 0.102382766772 | 0.00158833792656 |
| rmse | 0.154040121902 | 0.160123342295 | 0.149548591245 | 0.00365247845886 |
| mape | 0.0807614737326 | 0.0832065562181 | 0.0776724866644 | 0.0018807671835 |
| max_error | 1.15770278575 | 1.69423726872 | 0.904052794872 | 0.284521613255 |

### matbench_log_kvrh

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| mae | 0.0819825484217 | 0.0862696399472 | 0.0783141445137 | 0.00271972565089 |
| rmse | 0.145360912566 | 0.150255516099 | 0.138320059166 | 0.00462831988118 |
| mape | 0.054592530708 | 0.0607661711246 | 0.050921152629 | 0.00348070098442 |
| max_error | 1.37315631231 | 1.76416363754 | 1.11891531674 | 0.231105610567 |



## 4e. Layer A RF all-task expansion

# Matbench v0.1 score recomputation

- Results artifact: `vendor/matbench/benchmarks/matbench_v0.1_rf/results.json.gz`
- Fold scores checked: 65
- Max absolute stored-vs-recomputed score delta: 1.776e-15

## Fold checks

| Task | Fold | n | Prediction type | Max score delta | Stored rocauc | Probability rocauc |
|---|---:|---:|---|---:|---:|---:|
| matbench_dielectric | 0 | 953 | float | 0.000e+00 |  |  |
| matbench_dielectric | 1 | 953 | float | 0.000e+00 |  |  |
| matbench_dielectric | 2 | 953 | float | 0.000e+00 |  |  |
| matbench_dielectric | 3 | 953 | float | 0.000e+00 |  |  |
| matbench_dielectric | 4 | 952 | float | 0.000e+00 |  |  |
| matbench_expt_gap | 0 | 921 | float | 0.000e+00 |  |  |
| matbench_expt_gap | 1 | 921 | float | 0.000e+00 |  |  |
| matbench_expt_gap | 2 | 921 | float | 0.000e+00 |  |  |
| matbench_expt_gap | 3 | 921 | float | 0.000e+00 |  |  |
| matbench_expt_gap | 4 | 920 | float | 0.000e+00 |  |  |
| matbench_expt_is_metal | 0 | 985 | bool | 0.000e+00 | 0.924829110219 |  |
| matbench_expt_is_metal | 1 | 984 | bool | 0.000e+00 | 0.916632239941 |  |
| matbench_expt_is_metal | 2 | 984 | bool | 1.110e-16 | 0.909481120383 |  |
| matbench_expt_is_metal | 3 | 984 | bool | 1.110e-16 | 0.922746426506 |  |
| matbench_expt_is_metal | 4 | 984 | bool | 1.110e-16 | 0.909605056598 |  |
| matbench_glass | 0 | 1136 | bool | 0.000e+00 | 0.886006937775 |  |
| matbench_glass | 1 | 1136 | bool | 0.000e+00 | 0.840239093344 |  |
| matbench_glass | 2 | 1136 | bool | 1.110e-16 | 0.849521474334 |  |
| matbench_glass | 3 | 1136 | bool | 1.110e-16 | 0.852619367766 |  |
| matbench_glass | 4 | 1136 | bool | 0.000e+00 | 0.865116401698 |  |
| matbench_jdft2d | 0 | 128 | float | 0.000e+00 |  |  |
| matbench_jdft2d | 1 | 127 | float | 0.000e+00 |  |  |
| matbench_jdft2d | 2 | 127 | float | 0.000e+00 |  |  |
| matbench_jdft2d | 3 | 127 | float | 0.000e+00 |  |  |
| matbench_jdft2d | 4 | 127 | float | 0.000e+00 |  |  |
| matbench_log_gvrh | 0 | 2198 | float | 0.000e+00 |  |  |
| matbench_log_gvrh | 1 | 2198 | float | 0.000e+00 |  |  |
| matbench_log_gvrh | 2 | 2197 | float | 0.000e+00 |  |  |
| matbench_log_gvrh | 3 | 2197 | float | 0.000e+00 |  |  |
| matbench_log_gvrh | 4 | 2197 | float | 0.000e+00 |  |  |
| matbench_log_kvrh | 0 | 2198 | float | 0.000e+00 |  |  |
| matbench_log_kvrh | 1 | 2198 | float | 0.000e+00 |  |  |
| matbench_log_kvrh | 2 | 2197 | float | 0.000e+00 |  |  |
| matbench_log_kvrh | 3 | 2197 | float | 0.000e+00 |  |  |
| matbench_log_kvrh | 4 | 2197 | float | 0.000e+00 |  |  |
| matbench_mp_e_form | 0 | 26551 | float | 1.110e-16 |  |  |
| matbench_mp_e_form | 1 | 26551 | float | 0.000e+00 |  |  |
| matbench_mp_e_form | 2 | 26550 | float | 2.220e-16 |  |  |
| matbench_mp_e_form | 3 | 26550 | float | 1.110e-16 |  |  |
| matbench_mp_e_form | 4 | 26550 | float | 1.388e-17 |  |  |
| matbench_mp_gap | 0 | 21223 | float | 1.776e-15 |  |  |
| matbench_mp_gap | 1 | 21223 | float | 0.000e+00 |  |  |
| matbench_mp_gap | 2 | 21223 | float | 0.000e+00 |  |  |
| matbench_mp_gap | 3 | 21222 | float | 1.776e-15 |  |  |
| matbench_mp_gap | 4 | 21222 | float | 1.776e-15 |  |  |
| matbench_mp_is_metal | 0 | 21223 | bool | 0.000e+00 | 0.902515493193 |  |
| matbench_mp_is_metal | 1 | 21223 | bool | 0.000e+00 | 0.896777056389 |  |
| matbench_mp_is_metal | 2 | 21223 | bool | 0.000e+00 | 0.898733815358 |  |
| matbench_mp_is_metal | 3 | 21222 | bool | 1.110e-16 | 0.899366668787 |  |
| matbench_mp_is_metal | 4 | 21222 | bool | 0.000e+00 | 0.898371847031 |  |
| matbench_perovskites | 0 | 3786 | float | 0.000e+00 |  |  |
| matbench_perovskites | 1 | 3786 | float | 0.000e+00 |  |  |
| matbench_perovskites | 2 | 3786 | float | 0.000e+00 |  |  |
| matbench_perovskites | 3 | 3785 | float | 0.000e+00 |  |  |
| matbench_perovskites | 4 | 3785 | float | 0.000e+00 |  |  |
| matbench_phonons | 0 | 253 | float | 0.000e+00 |  |  |
| matbench_phonons | 1 | 253 | float | 0.000e+00 |  |  |
| matbench_phonons | 2 | 253 | float | 0.000e+00 |  |  |
| matbench_phonons | 3 | 253 | float | 0.000e+00 |  |  |
| matbench_phonons | 4 | 253 | float | 0.000e+00 |  |  |
| matbench_steels | 0 | 63 | float | 0.000e+00 |  |  |
| matbench_steels | 1 | 63 | float | 0.000e+00 |  |  |
| matbench_steels | 2 | 62 | float | 0.000e+00 |  |  |
| matbench_steels | 3 | 62 | float | 0.000e+00 |  |  |
| matbench_steels | 4 | 62 | float | 0.000e+00 |  |  |

## Recomputed fold aggregates

### matbench_dielectric

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| mae | 0.419578159259 | 0.52198700518 | 0.304162451401 | 0.0750037451263 |
| rmse | 1.85382481618 | 2.98323049778 | 0.785044337763 | 0.770049375991 |
| mape | 0.139968218264 | 0.188632999374 | 0.10574510663 | 0.0288667979365 |
| max_error | 34.8805599225 | 59.1201445981 | 14.5978573183 | 16.9979726853 |

### matbench_expt_gap

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| mae | 0.446054992487 | 0.481156868621 | 0.434542420557 | 0.0176552424643 |
| rmse | 0.824300735345 | 0.943523224093 | 0.781867354239 | 0.0601326123053 |
| mape | 0.369492377556 | 0.43851001849 | 0.304356979438 | 0.0470475962382 |
| max_error | 6.046496 | 9.5428 | 4.71216 | 1.76997564717 |

### matbench_expt_is_metal

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| accuracy | 0.916681936363 | 0.924873096447 | 0.909552845528 | 0.00641463134 |
| balanced_accuracy | 0.916658790729 | 0.924829110219 | 0.909481120383 | 0.00640450234832 |
| f1 | 0.915855162513 | 0.923553719008 | 0.907580477674 | 0.00628063358071 |
| rocauc | 0.916658790729 | 0.924829110219 | 0.909481120383 | 0.00640450234832 |

### matbench_glass

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| accuracy | 0.895422535211 | 0.919894366197 | 0.884683098592 | 0.0130969823334 |
| balanced_accuracy | 0.858700654983 | 0.886006937775 | 0.840239093344 | 0.0158041991609 |
| f1 | 0.927798088561 | 0.944881889764 | 0.919975565058 | 0.00908698827732 |
| rocauc | 0.858700654983 | 0.886006937775 | 0.840239093344 | 0.0158041991609 |

### matbench_jdft2d

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| mae | 50.04399974 | 66.2421301222 | 42.7472945267 | 8.62712887611 |
| rmse | 112.265975486 | 159.638986052 | 72.7391490957 | 36.7066225573 |
| mape | 5.23911546788 | 23.7624894676 | 0.43823538542 | 9.26294774418 |
| max_error | 718.045733692 | 1538.60726856 | 295.743678511 | 453.647322018 |

### matbench_log_gvrh

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| mae | 0.103998778594 | 0.106730986524 | 0.102382766772 | 0.00158833792656 |
| rmse | 0.154040121902 | 0.160123342295 | 0.149548591245 | 0.00365247845886 |
| mape | 0.0807614737326 | 0.0832065562181 | 0.0776724866644 | 0.0018807671835 |
| max_error | 1.15770278575 | 1.69423726872 | 0.904052794872 | 0.284521613255 |

### matbench_log_kvrh

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| mae | 0.0819825484217 | 0.0862696399472 | 0.0783141445137 | 0.00271972565089 |
| rmse | 0.145360912566 | 0.150255516099 | 0.138320059166 | 0.00462831988118 |
| mape | 0.054592530708 | 0.0607661711246 | 0.050921152629 | 0.00348070098442 |
| max_error | 1.37315631231 | 1.76416363754 | 1.11891531674 | 0.231105610567 |

### matbench_mp_e_form

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| mae | 0.116450238243 | 0.117945584401 | 0.115797966884 | 0.000798121161187 |
| rmse | 0.241940247639 | 0.245915868682 | 0.237323137793 | 0.00335752922832 |
| mape | 0.679807113796 | 0.933100288396 | 0.506812454973 | 0.149239730501 |
| max_error | 4.11834095889 | 5.43820297872 | 2.93736137858 | 0.800820896985 |

### matbench_mp_gap

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| mae | 0.345156150814 | 0.351217869437 | 0.341694434699 | 0.00332691657799 |
| rmse | 0.612501885046 | 0.627629509615 | 0.604668073226 | 0.00785109927504 |
| mape | 7.63147228584 | 11.9090490977 | 4.35469060744 | 2.68347073039 |
| max_error | 6.39584315417 | 7.0601086 | 5.92008807086 | 0.418177009281 |

### matbench_mp_is_metal

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| accuracy | 0.905063466294 | 0.907977194553 | 0.902747019743 | 0.00167604998183 |
| balanced_accuracy | 0.899152976151 | 0.902515493193 | 0.896777056389 | 0.00188589705907 |
| f1 | 0.88664732113 | 0.890520769101 | 0.883862255233 | 0.00217933157754 |
| rocauc | 0.899152976151 | 0.902515493193 | 0.896777056389 | 0.00188589705907 |

### matbench_perovskites

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| mae | 0.235500182628 | 0.239509685601 | 0.229107455746 | 0.00344641995434 |
| rmse | 0.334613028166 | 0.339431954877 | 0.32924887781 | 0.00441961063639 |
| mape | 0.267833188583 | 0.288835902682 | 0.241102775512 | 0.016844798769 |
| max_error | 2.557712 | 2.88704 | 2.20832 | 0.218511273338 |

### matbench_phonons

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| mae | 67.6126142422 | 82.3862649649 | 58.6036107598 | 8.9899908374 |
| rmse | 146.276431864 | 172.801458959 | 122.15658115 | 21.4751689658 |
| mape | 0.118485135116 | 0.134769893668 | 0.104049045388 | 0.00979558791325 |
| max_error | 1270.68885897 | 2024.7301119 | 861.90049904 | 402.730658047 |

### matbench_steels

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| mae | 103.512486062 | 114.63311746 | 85.6694031746 | 11.0367786926 |
| rmse | 149.383944441 | 196.358570629 | 113.154922817 | 27.4893431478 |
| mape | 0.0744721297401 | 0.0807437889227 | 0.0653807405884 | 0.0056047478171 |
| max_error | 594.98156 | 1121.1276 | 362.663 | 278.700159881 |



## 4f. Layer A Dummy all-task expansion

# Matbench v0.1 score recomputation

- Results artifact: `vendor/matbench/benchmarks/matbench_v0.1_dummy/results.json.gz`
- Fold scores checked: 65
- Max absolute stored-vs-recomputed score delta: 3.553e-15

## Fold checks

| Task | Fold | n | Prediction type | Max score delta | Stored rocauc | Probability rocauc |
|---|---:|---:|---|---:|---:|---:|
| matbench_dielectric | 0 | 953 | float | 0.000e+00 |  |  |
| matbench_dielectric | 1 | 953 | float | 0.000e+00 |  |  |
| matbench_dielectric | 2 | 953 | float | 0.000e+00 |  |  |
| matbench_dielectric | 3 | 953 | float | 0.000e+00 |  |  |
| matbench_dielectric | 4 | 952 | float | 0.000e+00 |  |  |
| matbench_expt_gap | 0 | 921 | float | 0.000e+00 |  |  |
| matbench_expt_gap | 1 | 921 | float | 0.000e+00 |  |  |
| matbench_expt_gap | 2 | 921 | float | 0.000e+00 |  |  |
| matbench_expt_gap | 3 | 921 | float | 0.000e+00 |  |  |
| matbench_expt_gap | 4 | 920 | float | 0.000e+00 |  |  |
| matbench_expt_is_metal | 0 | 985 | bool | 5.551e-17 | 0.469965450992 |  |
| matbench_expt_is_metal | 1 | 984 | bool | 0.000e+00 | 0.500074361728 |  |
| matbench_expt_is_metal | 2 | 984 | bool | 0.000e+00 | 0.487812938941 |  |
| matbench_expt_is_metal | 3 | 984 | bool | 0.000e+00 | 0.507167644386 |  |
| matbench_expt_is_metal | 4 | 984 | bool | 0.000e+00 | 0.49693877551 |  |
| matbench_glass | 0 | 1136 | bool | 0.000e+00 | 0.521244581041 |  |
| matbench_glass | 1 | 1136 | bool | 0.000e+00 | 0.521747400218 |  |
| matbench_glass | 2 | 1136 | bool | 1.110e-16 | 0.484759117599 |  |
| matbench_glass | 3 | 1136 | bool | 0.000e+00 | 0.479860867862 |  |
| matbench_glass | 4 | 1136 | bool | 0.000e+00 | 0.495058436251 |  |
| matbench_jdft2d | 0 | 128 | float | 0.000e+00 |  |  |
| matbench_jdft2d | 1 | 127 | float | 0.000e+00 |  |  |
| matbench_jdft2d | 2 | 127 | float | 0.000e+00 |  |  |
| matbench_jdft2d | 3 | 127 | float | 0.000e+00 |  |  |
| matbench_jdft2d | 4 | 127 | float | 0.000e+00 |  |  |
| matbench_log_gvrh | 0 | 2198 | float | 0.000e+00 |  |  |
| matbench_log_gvrh | 1 | 2198 | float | 0.000e+00 |  |  |
| matbench_log_gvrh | 2 | 2197 | float | 0.000e+00 |  |  |
| matbench_log_gvrh | 3 | 2197 | float | 0.000e+00 |  |  |
| matbench_log_gvrh | 4 | 2197 | float | 0.000e+00 |  |  |
| matbench_log_kvrh | 0 | 2198 | float | 0.000e+00 |  |  |
| matbench_log_kvrh | 1 | 2198 | float | 0.000e+00 |  |  |
| matbench_log_kvrh | 2 | 2197 | float | 0.000e+00 |  |  |
| matbench_log_kvrh | 3 | 2197 | float | 0.000e+00 |  |  |
| matbench_log_kvrh | 4 | 2197 | float | 0.000e+00 |  |  |
| matbench_mp_e_form | 0 | 26551 | float | 3.553e-15 |  |  |
| matbench_mp_e_form | 1 | 26551 | float | 8.882e-16 |  |  |
| matbench_mp_e_form | 2 | 26550 | float | 0.000e+00 |  |  |
| matbench_mp_e_form | 3 | 26550 | float | 1.776e-15 |  |  |
| matbench_mp_e_form | 4 | 26550 | float | 2.220e-16 |  |  |
| matbench_mp_gap | 0 | 21223 | float | 1.776e-15 |  |  |
| matbench_mp_gap | 1 | 21223 | float | 3.553e-15 |  |  |
| matbench_mp_gap | 2 | 21223 | float | 0.000e+00 |  |  |
| matbench_mp_gap | 3 | 21222 | float | 0.000e+00 |  |  |
| matbench_mp_gap | 4 | 21222 | float | 2.220e-16 |  |  |
| matbench_mp_is_metal | 0 | 21223 | bool | 0.000e+00 | 0.506886095257 |  |
| matbench_mp_is_metal | 1 | 21223 | bool | 0.000e+00 | 0.494419221071 |  |
| matbench_mp_is_metal | 2 | 21223 | bool | 5.551e-17 | 0.498590270053 |  |
| matbench_mp_is_metal | 3 | 21222 | bool | 5.551e-17 | 0.50323734241 |  |
| matbench_mp_is_metal | 4 | 21222 | bool | 5.551e-17 | 0.502950061688 |  |
| matbench_perovskites | 0 | 3786 | float | 0.000e+00 |  |  |
| matbench_perovskites | 1 | 3786 | float | 0.000e+00 |  |  |
| matbench_perovskites | 2 | 3786 | float | 0.000e+00 |  |  |
| matbench_perovskites | 3 | 3785 | float | 0.000e+00 |  |  |
| matbench_perovskites | 4 | 3785 | float | 0.000e+00 |  |  |
| matbench_phonons | 0 | 253 | float | 0.000e+00 |  |  |
| matbench_phonons | 1 | 253 | float | 0.000e+00 |  |  |
| matbench_phonons | 2 | 253 | float | 0.000e+00 |  |  |
| matbench_phonons | 3 | 253 | float | 0.000e+00 |  |  |
| matbench_phonons | 4 | 253 | float | 0.000e+00 |  |  |
| matbench_steels | 0 | 63 | float | 0.000e+00 |  |  |
| matbench_steels | 1 | 63 | float | 0.000e+00 |  |  |
| matbench_steels | 2 | 62 | float | 0.000e+00 |  |  |
| matbench_steels | 3 | 62 | float | 0.000e+00 |  |  |
| matbench_steels | 4 | 62 | float | 0.000e+00 |  |  |

## Recomputed fold aggregates

### matbench_dielectric

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| mae | 0.80881997604 | 0.921817134881 | 0.702564297978 | 0.0717835125652 |
| rmse | 1.97276439959 | 3.10548965166 | 1.06773480736 | 0.726270709807 |
| mape | 0.319714785196 | 0.326616109687 | 0.314152052154 | 0.00453389033877 |
| max_error | 35.3994799869 | 59.6652611154 | 14.9500627337 | 17.9221496905 |

### matbench_expt_gap

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| mae | 1.14352696092 | 1.19221192656 | 1.09646800468 | 0.0310111790489 |
| rmse | 1.44375982344 | 1.52680793386 | 1.3396579641 | 0.07074457681 |
| mape | 0.951601279953 | 1.24184930189 | 0.780170403994 | 0.169159721419 |
| max_error | 8.93004949746 | 10.7354493619 | 7.01188433342 | 1.23283288667 |

### matbench_expt_is_metal

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| accuracy | 0.492384136024 | 0.507113821138 | 0.470050761421 | 0.0127716285884 |
| balanced_accuracy | 0.492391834312 | 0.507167644386 | 0.469965450992 | 0.0128213058361 |
| f1 | 0.491344921998 | 0.51256281407 | 0.453974895397 | 0.0207164926849 |
| rocauc | 0.492391834312 | 0.507167644386 | 0.469965450992 | 0.0128213058361 |

### matbench_glass

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| accuracy | 0.590669014085 | 0.612676056338 | 0.573063380282 | 0.0164685624418 |
| balanced_accuracy | 0.500534080594 | 0.521747400218 | 0.479860867862 | 0.0178053004541 |
| f1 | 0.712669719722 | 0.730392156863 | 0.700061842919 | 0.0125196238713 |
| rocauc | 0.500534080594 | 0.521747400218 | 0.479860867862 | 0.0178053004541 |

### matbench_jdft2d

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| mae | 67.2850873958 | 83.1220028779 | 53.1447467433 | 10.1832326615 |
| rmse | 126.844613359 | 192.236461159 | 74.1059643166 | 45.2193370998 |
| mape | 7.8079477369 | 35.3098249284 | 0.79210307142 | 13.7515312089 |
| max_error | 827.476377735 | 1491.79929416 | 468.041237726 | 385.901595872 |

### matbench_log_gvrh

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| mae | 0.293147728528 | 0.296893245401 | 0.287489096428 | 0.00309088260967 |
| rmse | 0.371590544033 | 0.374890372437 | 0.364594619641 | 0.00379960401816 |
| mape | 0.233303472103 | 0.236753399418 | 0.225144441871 | 0.00422138007666 |
| max_error | 1.55363851107 | 1.55523707332 | 1.55239936687 | 0.00102394167409 |

### matbench_log_kvrh

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| mae | 0.289693942024 | 0.295295712664 | 0.283276966769 | 0.00429747595087 |
| rmse | 0.369280680266 | 0.377400150458 | 0.363406251279 | 0.00589772165866 |
| mape | 0.187715572834 | 0.19264256072 | 0.182488864206 | 0.00348128655996 |
| max_error | 1.88044586043 | 1.88222304717 | 1.87899627074 | 0.0010767375786 |

### matbench_mp_e_form

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| mae | 1.00592689696 | 1.01107559823 | 1.00239527876 | 0.00298062807204 |
| rmse | 1.16313008776 | 1.16750266496 | 1.15966709918 | 0.00322549492437 |
| mape | 9.9487032688 | 11.6408738141 | 7.28677669784 | 1.71343664278 |
| max_error | 3.89700288851 | 3.90963195498 | 3.87819929834 | 0.0109045417018 |

### matbench_mp_gap

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| mae | 1.32715612132 | 1.33479749605 | 1.31988057023 | 0.00596803481226 |
| rmse | 1.59893509043 | 1.61182033281 | 1.58633655116 | 0.0108240191848 |
| mape | 15.5847966914 | 19.3774275113 | 12.1281805816 | 2.70223814416 |
| max_error | 7.75845333957 | 8.50918423154 | 7.10789517022 | 0.49632018836 |

### matbench_mp_is_metal

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| accuracy | 0.509918708023 | 0.515808321161 | 0.503227630401 | 0.00438899647352 |
| balanced_accuracy | 0.501216598096 | 0.506886095257 | 0.494419221071 | 0.0042972883326 |
| f1 | 0.435332826842 | 0.440548780488 | 0.42766407904 | 0.00433704294907 |
| rocauc | 0.501216598096 | 0.506886095257 | 0.494419221071 | 0.0042972883326 |

### matbench_perovskites

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| mae | 0.565998636192 | 0.574237337498 | 0.561199645022 | 0.00476994826584 |
| rmse | 0.742436343233 | 0.761797387026 | 0.734215871229 | 0.0102276667648 |
| mape | 0.758264985415 | 0.804586721598 | 0.705803135105 | 0.0333563178526 |
| max_error | 3.47706803685 | 3.68732796196 | 3.31226918505 | 0.126433463808 |

### matbench_phonons

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| mae | 323.98222624 | 348.257637178 | 299.120899653 | 17.7268997573 |
| rmse | 492.15330732 | 545.477181807 | 439.316559745 | 44.5175589932 |
| mape | 0.892570224044 | 1.02675700404 | 0.79769445702 | 0.0809879835419 |
| max_error | 2760.79467567 | 3062.34498517 | 1970.08835251 | 417.15805845 |

### matbench_steels

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| mae | 229.744529653 | 241.459074393 | 219.377031937 | 9.69580568939 |
| rmse | 301.221148667 | 343.934626844 | 287.68027737 | 21.4550756918 |
| mape | 0.158816036383 | 0.164724706551 | 0.155028132877 | 0.00335870996462 |
| max_error | 1032.32451791 | 1088.0568 | 941.064257028 | 59.3578666672 |



## 4g. Layer A all-submission score scan

# Matbench v0.1 all-submission score scan

- Submissions checked: 28
- Submission/task records checked: 180
- Folds checked: 900
- Max absolute stored-vs-recomputed score delta: 1.217e+01
- Failing folds at tolerance 1e-12: 5
- Classification folds checked: 135
- Classification folds with stored `rocauc == balanced_accuracy`: 135

## Per-submission summary

| Submission | Tasks | Folds | Max score delta | Failing folds |
|---|---:|---:|---:|---:|
| matbench_v0.1_Auto-sklearn | 1 | 5 | 0.000e+00 | 0 |
| matbench_v0.1_Ax_10_90_CrabNet_v1.2.7 | 1 | 5 | 0.000e+00 | 0 |
| matbench_v0.1_Ax_CrabNet_v1.2.1 | 1 | 5 | 0.000e+00 | 0 |
| matbench_v0.1_Ax_SAASBO_CrabNet_v1.2.7 | 1 | 5 | 0.000e+00 | 0 |
| matbench_v0.1_CrabNet | 10 | 50 | 8.882e-16 | 0 |
| matbench_v0.1_CrabNet_v1.2.1 | 1 | 5 | 0.000e+00 | 0 |
| matbench_v0.1_DeeperGATGNN | 8 | 40 | 8.882e-16 | 0 |
| matbench_v0.1_DimeNetPP_kgcnn_v2.1.0 | 9 | 45 | 1.776e-15 | 0 |
| matbench_v0.1_Finder_v1.2_composition | 8 | 40 | 8.882e-16 | 0 |
| matbench_v0.1_Finder_v1.2_structure | 8 | 40 | 1.776e-15 | 0 |
| matbench_v0.1_GN-OA | 1 | 5 | 1.217e+01 | 5 |
| matbench_v0.1_MegNet_kgcnn_v2.1.0 | 9 | 45 | 1.776e-15 | 0 |
| matbench_v0.1_RFLR | 1 | 5 | 0.000e+00 | 0 |
| matbench_v0.1_SchNet_kgcnn_v2.1.0 | 9 | 45 | 8.882e-16 | 0 |
| matbench_v0.1_TPOT | 1 | 5 | 0.000e+00 | 0 |
| matbench_v0.1_alignn | 9 | 45 | 1.776e-15 | 0 |
| matbench_v0.1_automatminer_expressv2020 | 13 | 65 | 4.441e-16 | 0 |
| matbench_v0.1_cgcnnv2019 | 9 | 45 | 8.882e-16 | 0 |
| matbench_v0.1_coGN | 9 | 45 | 8.882e-16 | 0 |
| matbench_v0.1_coNGN | 9 | 45 | 8.882e-16 | 0 |
| matbench_v0.1_darwin | 4 | 20 | 1.110e-16 | 0 |
| matbench_v0.1_dummy | 13 | 65 | 3.553e-15 | 0 |
| matbench_v0.1_gptchem | 4 | 20 | 1.110e-16 | 0 |
| matbench_v0.1_lattice_xgboost | 1 | 5 | 1.776e-15 | 0 |
| matbench_v0.1_matformer | 1 | 5 | 1.110e-16 | 0 |
| matbench_v0.1_modnet_v0.1.10 | 13 | 65 | 1.776e-15 | 0 |
| matbench_v0.1_modnet_v0.1.12 | 13 | 65 | 1.776e-15 | 0 |
| matbench_v0.1_rf | 13 | 65 | 1.776e-15 | 0 |

## Task coverage

| Task | Submission records |
|---|---:|
| matbench_dielectric | 16 |
| matbench_expt_gap | 12 |
| matbench_expt_is_metal | 7 |
| matbench_glass | 7 |
| matbench_jdft2d | 16 |
| matbench_log_gvrh | 16 |
| matbench_log_kvrh | 16 |
| matbench_mp_e_form | 18 |
| matbench_mp_gap | 16 |
| matbench_mp_is_metal | 13 |
| matbench_perovskites | 16 |
| matbench_phonons | 16 |
| matbench_steels | 11 |

## Largest score deltas

| Submission | Task | Fold | n | Prediction type | Worst metric | Max delta | Stored rocauc | Stored bal. acc. | Probability rocauc |
|---|---|---|---:|---|---|---:|---:|---:|---:|
| matbench_v0.1_GN-OA | matbench_mp_e_form | 0 | 26551 | float | mape | 1.217e+01 |  |  |  |
| matbench_v0.1_GN-OA | matbench_mp_e_form | 4 | 26550 | float | mape | 1.199e+01 |  |  |  |
| matbench_v0.1_GN-OA | matbench_mp_e_form | 3 | 26550 | float | mape | 1.165e+01 |  |  |  |
| matbench_v0.1_GN-OA | matbench_mp_e_form | 2 | 26550 | float | mape | 9.114e+00 |  |  |  |
| matbench_v0.1_GN-OA | matbench_mp_e_form | 1 | 26551 | float | mape | 7.809e+00 |  |  |  |
| matbench_v0.1_dummy | matbench_mp_e_form | 0 | 26551 | float | mape | 3.553e-15 |  |  |  |
| matbench_v0.1_dummy | matbench_mp_gap | 1 | 21223 | float | mape | 3.553e-15 |  |  |  |
| matbench_v0.1_alignn | matbench_mp_gap | 2 | 21223 | float | mape | 1.776e-15 |  |  |  |
| matbench_v0.1_DimeNetPP_kgcnn_v2.1.0 | matbench_mp_gap | 3 | 21222 | float | mape | 1.776e-15 |  |  |  |
| matbench_v0.1_dummy | matbench_mp_e_form | 3 | 26550 | float | mape | 1.776e-15 |  |  |  |
| matbench_v0.1_dummy | matbench_mp_gap | 0 | 21223 | float | mape | 1.776e-15 |  |  |  |
| matbench_v0.1_Finder_v1.2_structure | matbench_mp_gap | 3 | 21222 | float | mape | 1.776e-15 |  |  |  |
| matbench_v0.1_lattice_xgboost | matbench_mp_e_form | 0 | 26551 | float | mape | 1.776e-15 |  |  |  |
| matbench_v0.1_lattice_xgboost | matbench_mp_e_form | 4 | 26550 | float | mape | 1.776e-15 |  |  |  |
| matbench_v0.1_MegNet_kgcnn_v2.1.0 | matbench_mp_gap | 3 | 21222 | float | mape | 1.776e-15 |  |  |  |
| matbench_v0.1_modnet_v0.1.10 | matbench_mp_gap | 3 | 21222 | float | mape | 1.776e-15 |  |  |  |
| matbench_v0.1_modnet_v0.1.12 | matbench_mp_gap | 3 | 21222 | float | mape | 1.776e-15 |  |  |  |
| matbench_v0.1_rf | matbench_mp_gap | 0 | 21223 | float | mape | 1.776e-15 |  |  |  |
| matbench_v0.1_rf | matbench_mp_gap | 3 | 21222 | float | mape | 1.776e-15 |  |  |  |
| matbench_v0.1_rf | matbench_mp_gap | 4 | 21222 | float | mape | 1.776e-15 |  |  |  |

## Failures

| Submission | Task | Fold | Problem |
|---|---|---|---|
| matbench_v0.1_GN-OA | matbench_mp_e_form | fold_0 | delta 1.217e+01 |
| matbench_v0.1_GN-OA | matbench_mp_e_form | fold_1 | delta 7.809e+00 |
| matbench_v0.1_GN-OA | matbench_mp_e_form | fold_2 | delta 9.114e+00 |
| matbench_v0.1_GN-OA | matbench_mp_e_form | fold_3 | delta 1.165e+01 |
| matbench_v0.1_GN-OA | matbench_mp_e_form | fold_4 | delta 1.199e+01 |



## 4h. Layer A GN-OA MAPE exception probe

# Matbench v0.1 GN-OA MAPE exception probe

The all-submission score scan found one score-recompute exception:
`matbench_v0.1_GN-OA` on `matbench_mp_e_form`. This probe checks whether the
exception affects all regression metrics or only MAPE.

## Result

MAE, RMSE, and max error match the stored fold scores exactly or to floating-point
precision. The mismatch is isolated to MAPE.

| Fold | Stored MAPE | Recomputed Matbench MAPE | Delta | Other regression metrics |
|---:|---:|---:|---:|---|
| 0 | 12.5887409438 | 0.420116236715 | 12.1686247071 | match |
| 1 | 7.94659210396 | 0.137819988807 | 7.80877211515 | match |
| 2 | 9.26331433818 | 0.149750183903 | 9.11356415428 | match |
| 3 | 11.8881843898 | 0.236287007689 | 11.6518973821 | match |
| 4 | 12.1946455981 | 0.201616727224 | 11.9930288708 | match |

## Formula checks

The Matbench v0.1 MAPE path masks target values with `abs(y_true) > 1e-5`. Using
that formula gives the recomputed values above.

A simple unmasked MAPE is not the stored formula either: it becomes infinite on
all five folds because the `matbench_mp_e_form` test targets contain exact zeros.

Threshold sweeps over small denominators also did not reproduce the stored values.
This points to a submission-specific stored-MAPE inconsistency rather than an ID
alignment problem or a general scoring-path issue.

## Interpretation

The published GN-OA predictions appear aligned with the official validation IDs:
MAE, RMSE, and max error all match. The exception should be treated narrowly as a
stored MAPE inconsistency for `matbench_v0.1_GN-OA` / `matbench_mp_e_form`.



## 5. Classification prediction scan

# Matbench v0.1 classification prediction-type scan

- Submission/task records scanned: 27
- All-bool records: 16
- All-float records: 11
- Mixed-type records: 0
- Records where stored ROC-AUC differs from balanced accuracy: 0

| Submission | Task | Kind | n | bool | float | min float | max float | max abs rocauc-bal_acc |
|---|---|---|---:|---:|---:|---:|---:|---:|
| matbench_v0.1_alignn | matbench_mp_is_metal | all_bool | 106113 | 106113 | 0 |  |  | 1.110e-16 |
| matbench_v0.1_automatminer_expressv2020 | matbench_expt_is_metal | all_bool | 4921 | 4921 | 0 |  |  | 1.110e-16 |
| matbench_v0.1_automatminer_expressv2020 | matbench_glass | all_bool | 5680 | 5680 | 0 |  |  | 1.110e-16 |
| matbench_v0.1_automatminer_expressv2020 | matbench_mp_is_metal | all_bool | 106113 | 106113 | 0 |  |  | 1.110e-16 |
| matbench_v0.1_cgcnnv2019 | matbench_mp_is_metal | all_bool | 106113 | 106113 | 0 |  |  | 1.110e-16 |
| matbench_v0.1_coGN | matbench_mp_is_metal | all_float | 106113 | 0 | 106113 | 0 | 1 | 1.110e-16 |
| matbench_v0.1_coNGN | matbench_mp_is_metal | all_float | 106113 | 0 | 106113 | 0 | 1 | 1.110e-16 |
| matbench_v0.1_darwin | matbench_expt_is_metal | all_bool | 4921 | 4921 | 0 |  |  | 1.110e-16 |
| matbench_v0.1_darwin | matbench_glass | all_bool | 5680 | 5680 | 0 |  |  | 1.110e-16 |
| matbench_v0.1_DimeNetPP_kgcnn_v2.1.0 | matbench_mp_is_metal | all_float | 106113 | 0 | 106113 | 1.00267382286e-180 | 1 | 0.000e+00 |
| matbench_v0.1_dummy | matbench_expt_is_metal | all_bool | 4921 | 4921 | 0 |  |  | 1.110e-16 |
| matbench_v0.1_dummy | matbench_glass | all_bool | 5680 | 5680 | 0 |  |  | 5.551e-17 |
| matbench_v0.1_dummy | matbench_mp_is_metal | all_bool | 106113 | 106113 | 0 |  |  | 5.551e-17 |
| matbench_v0.1_gptchem | matbench_expt_is_metal | all_bool | 4921 | 4921 | 0 |  |  | 1.110e-16 |
| matbench_v0.1_gptchem | matbench_glass | all_bool | 5680 | 5680 | 0 |  |  | 1.110e-16 |
| matbench_v0.1_matformer | matbench_mp_is_metal | all_bool | 106113 | 106113 | 0 |  |  | 1.110e-16 |
| matbench_v0.1_MegNet_kgcnn_v2.1.0 | matbench_mp_is_metal | all_float | 106113 | 0 | 106113 | 0 | 1 | 1.110e-16 |
| matbench_v0.1_modnet_v0.1.10 | matbench_expt_is_metal | all_float | 4921 | 0 | 4921 | 0.0120466127992 | 0.992314636707 | 1.110e-16 |
| matbench_v0.1_modnet_v0.1.10 | matbench_glass | all_float | 5680 | 0 | 5680 | 0.0574636124074 | 0.979165077209 | 1.110e-16 |
| matbench_v0.1_modnet_v0.1.10 | matbench_mp_is_metal | all_float | 106113 | 0 | 106113 | 4.26786733953e-31 | 0.999985873699 | 1.110e-16 |
| matbench_v0.1_modnet_v0.1.12 | matbench_expt_is_metal | all_float | 4921 | 0 | 4921 | 0.0120466127992 | 0.992314636707 | 1.110e-16 |
| matbench_v0.1_modnet_v0.1.12 | matbench_glass | all_float | 5680 | 0 | 5680 | 2.40353672066e-17 | 1 | 1.110e-16 |
| matbench_v0.1_modnet_v0.1.12 | matbench_mp_is_metal | all_float | 106113 | 0 | 106113 | 0 | 1 | 1.110e-16 |
| matbench_v0.1_rf | matbench_expt_is_metal | all_bool | 4921 | 4921 | 0 |  |  | 1.110e-16 |
| matbench_v0.1_rf | matbench_glass | all_bool | 5680 | 5680 | 0 |  |  | 1.110e-16 |
| matbench_v0.1_rf | matbench_mp_is_metal | all_bool | 106113 | 106113 | 0 |  |  | 1.110e-16 |
| matbench_v0.1_SchNet_kgcnn_v2.1.0 | matbench_mp_is_metal | all_float | 106113 | 0 | 106113 | 0 | 1 | 2.220e-16 |



## 5b. Classification leaderboard metric scan

# Matbench v0.1 classification leaderboard metric scan

- Classification leaderboard tables scanned: 3
- Displayed algorithm rows scanned: 27
- Rows where displayed mean rocauc differs from mean balanced_accuracy: 0

| Task | Algorithm | mean rocauc | mean balanced_accuracy | displayed delta |
|---|---|---:|---:|---:|
| matbench_expt_is_metal | Darwin | 0.9598 | 0.9598 | 0.0000 |
| matbench_expt_is_metal | AMMExpress v2020 | 0.9209 | 0.9209 | 0.0000 |
| matbench_expt_is_metal | RF-SCM/Magpie | 0.9167 | 0.9167 | 0.0000 |
| matbench_expt_is_metal | MODNet (v0.1.12) | 0.9161 | 0.9161 | 0.0000 |
| matbench_expt_is_metal | MODNet (v0.1.10) | 0.9161 | 0.9161 | 0.0000 |
| matbench_expt_is_metal | gptchem | 0.8965 | 0.8965 | 0.0000 |
| matbench_expt_is_metal | Dummy | 0.4924 | 0.4924 | 0.0000 |
| matbench_glass | MODNet (v0.1.12) | 0.9603 | 0.9603 | 0.0000 |
| matbench_glass | AMMExpress v2020 | 0.8607 | 0.8607 | 0.0000 |
| matbench_glass | RF-SCM/Magpie | 0.8587 | 0.8587 | 0.0000 |
| matbench_glass | MODNet (v0.1.10) | 0.8107 | 0.8107 | 0.0000 |
| matbench_glass | gptchem | 0.7762 | 0.7762 | 0.0000 |
| matbench_glass | Darwin | 0.7668 | 0.7668 | 0.0000 |
| matbench_glass | Dummy | 0.5005 | 0.5005 | 0.0000 |
| matbench_mp_is_metal | CGCNN v2019 | 0.9520 | 0.9520 | 0.0000 |
| matbench_mp_is_metal | ALIGNN | 0.9128 | 0.9128 | 0.0000 |
| matbench_mp_is_metal | coGN | 0.9124 | 0.9124 | 0.0000 |
| matbench_mp_is_metal | AMMExpress v2020 | 0.9093 | 0.9093 | 0.0000 |
| matbench_mp_is_metal | coNGN | 0.9089 | 0.9089 | 0.0000 |
| matbench_mp_is_metal | MODNet (v0.1.12) | 0.9038 | 0.9038 | 0.0000 |
| matbench_mp_is_metal | DimeNet++ (kgcnn v2.1.0) | 0.9032 | 0.9032 | 0.0000 |
| matbench_mp_is_metal | MegNet (kgcnn v2.1.0) | 0.9021 | 0.9021 | 0.0000 |
| matbench_mp_is_metal | RF-SCM/Magpie | 0.8992 | 0.8992 | 0.0000 |
| matbench_mp_is_metal | SchNet (kgcnn v2.1.0) | 0.8907 | 0.8907 | 0.0000 |
| matbench_mp_is_metal | Matformer | 0.8117 | 0.8117 | 0.0000 |
| matbench_mp_is_metal | MODNet (v0.1.10) | 0.7805 | 0.7805 | 0.0000 |
| matbench_mp_is_metal | Dummy | 0.5012 | 0.5012 | 0.0000 |



## 5c. Classification ROC-AUC probe

# Matbench v0.1 classification ROC-AUC probe

Status: completed for public classification submission artifacts available in the
pinned upstream clone.

## Finding

All checked classification fold scores reproduce the values stored in
`results.json.gz`, but the stored `rocauc` field behaves as thresholded-label AUC
for submissions that store float predictions.

The code path explains the behavior. In `matbench.data_ops.score_array`,
classification metrics are ordered as:

```python
CLF_METRICS = ["accuracy", "balanced_accuracy", "f1", "rocauc"]
```

For non-ROC classification metrics, the local `pred_array` variable is reassigned
from float predictions to boolean labels at threshold 0.5. Because `accuracy` is
evaluated before `rocauc`, the later `rocauc` call receives the already-thresholded
labels rather than the original probability scores.

## Artifact scan

`scripts/matbench_classification_scan.py` inspected every local
`benchmarks/matbench_v0.1_*/results.json.gz` classification task:

| submission/task records | all bool | all float | mixed | records with stored ROC-AUC != balanced accuracy |
|---:|---:|---:|---:|---:|
| 27 | 16 | 11 | 0 | 0 |

The 11 all-float records include MODNet, coGN/coNGN, kgcnn SchNet/DimeNet/MegNet,
and are all stored with `rocauc` numerically equal to balanced accuracy within
rounding.

Report: `classification_prediction_scan.md`.

## Leaderboard display scan

`scripts/matbench_leaderboard_metric_scan.py` inspected the three generated
classification per-task leaderboard markdown tables. Each table uses `mean rocauc`
as the first displayed metric column, and all displayed rows have `mean rocauc`
equal to `mean balanced_accuracy`.

| classification leaderboard tables | displayed algorithm rows | rows with displayed mean rocauc != mean balanced_accuracy |
|---:|---:|---:|
| 3 | 27 | 0 |

Report: `classification_leaderboard_metric_scan.md`.

## Probability-AUC spot check

For two small MODNet classification tasks, the script reproduced stored fold scores
to numerical precision while also computing ROC-AUC from the raw float predictions.

| submission | task | stored rocauc mean | probability rocauc mean | mean gap |
|---|---|---:|---:|---:|
| `matbench_v0.1_modnet_v0.1.10` | `matbench_expt_is_metal` | 0.916052 | 0.972546 | 0.056495 |
| `matbench_v0.1_modnet_v0.1.10` | `matbench_glass` | 0.810676 | 0.932948 | 0.122272 |
| `matbench_v0.1_modnet_v0.1.12` | `matbench_expt_is_metal` | 0.916052 | 0.972546 | 0.056495 |
| `matbench_v0.1_modnet_v0.1.12` | `matbench_glass` | 0.960311 | 0.989876 | 0.029565 |

Reports:

- `layer_a_modnet_0_1_10_probability_auc_probe.md`
- `layer_a_modnet_0_1_12_probability_auc_probe.md`

## Interpretation

This does not break the reproducibility of the published artifacts: the stored
scores are internally consistent with the Matbench v0.1 code path and reproduce
exactly. It is an interpretation issue for classification metrics: a field named
`rocauc` can represent AUC of thresholded labels rather than AUC of submitted
probability scores.

The classification per-task leaderboards display `mean rocauc` as the main metric
column, so this should become either an upstream issue or a clearly scoped report
note.



## 5d. MODNet v0.1.10 probability-AUC probe

# Matbench v0.1 score recomputation

- Results artifact: `vendor/matbench/benchmarks/matbench_v0.1_modnet_v0.1.10/results.json.gz`
- Fold scores checked: 10
- Max absolute stored-vs-recomputed score delta: 1.110e-16

## Fold checks

| Task | Fold | n | Prediction type | Max score delta | Stored rocauc | Probability rocauc |
|---|---:|---:|---|---:|---:|---:|
| matbench_expt_is_metal | 0 | 985 | float | 1.110e-16 | 0.926853401717 | 0.976227973977 |
| matbench_expt_is_metal | 1 | 984 | float | 1.110e-16 | 0.913562753036 | 0.971321160043 |
| matbench_expt_is_metal | 2 | 984 | float | 1.110e-16 | 0.917677435347 | 0.974634388168 |
| matbench_expt_is_metal | 3 | 984 | float | 1.110e-16 | 0.917660910518 | 0.975113608196 |
| matbench_expt_is_metal | 4 | 984 | float | 1.110e-16 | 0.904503015781 | 0.96543418987 |
| matbench_glass | 0 | 1136 | float | 1.110e-16 | 0.826222302573 | 0.945985544419 |
| matbench_glass | 1 | 1136 | float | 0.000e+00 | 0.778326421924 | 0.922528182356 |
| matbench_glass | 2 | 1136 | float | 0.000e+00 | 0.806290324403 | 0.919718421261 |
| matbench_glass | 3 | 1136 | float | 0.000e+00 | 0.840239093344 | 0.935586415219 |
| matbench_glass | 4 | 1136 | float | 0.000e+00 | 0.802303552126 | 0.940923454726 |

## Recomputed fold aggregates

### matbench_expt_is_metal

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| accuracy | 0.91607176757 | 0.926903553299 | 0.904471544715 | 0.0072540465199 |
| balanced_accuracy | 0.91605150328 | 0.926853401717 | 0.904503015781 | 0.00723154613987 |
| f1 | 0.915321800781 | 0.925465838509 | 0.904858299595 | 0.00676906894697 |
| rocauc | 0.91605150328 | 0.926853401717 | 0.904503015781 | 0.00723154613987 |

### matbench_glass

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| accuracy | 0.867605633803 | 0.885563380282 | 0.853873239437 | 0.01187042805 |
| balanced_accuracy | 0.810676338874 | 0.840239093344 | 0.778326421924 | 0.0212202320756 |
| f1 | 0.910366876186 | 0.921686746988 | 0.901629450815 | 0.00751972277715 |
| rocauc | 0.810676338874 | 0.840239093344 | 0.778326421924 | 0.0212202320756 |



## 5e. MODNet v0.1.12 probability-AUC probe

# Matbench v0.1 score recomputation

- Results artifact: `vendor/matbench/benchmarks/matbench_v0.1_modnet_v0.1.12/results.json.gz`
- Fold scores checked: 10
- Max absolute stored-vs-recomputed score delta: 1.110e-16

## Fold checks

| Task | Fold | n | Prediction type | Max score delta | Stored rocauc | Probability rocauc |
|---|---:|---:|---|---:|---:|---:|
| matbench_expt_is_metal | 0 | 985 | float | 1.110e-16 | 0.926853401717 | 0.976227973977 |
| matbench_expt_is_metal | 1 | 984 | float | 1.110e-16 | 0.913562753036 | 0.971321160043 |
| matbench_expt_is_metal | 2 | 984 | float | 1.110e-16 | 0.917677435347 | 0.974634388168 |
| matbench_expt_is_metal | 3 | 984 | float | 1.110e-16 | 0.917660910518 | 0.975113608196 |
| matbench_expt_is_metal | 4 | 984 | float | 1.110e-16 | 0.904503015781 | 0.96543418987 |
| matbench_glass | 0 | 1136 | float | 0.000e+00 | 0.974327973695 | 0.995194027939 |
| matbench_glass | 1 | 1136 | float | 1.110e-16 | 0.961830939763 | 0.992173346441 |
| matbench_glass | 2 | 1136 | float | 0.000e+00 | 0.953893176348 | 0.986570773212 |
| matbench_glass | 3 | 1136 | float | 1.110e-16 | 0.95445437528 | 0.987841945289 |
| matbench_glass | 4 | 1136 | float | 0.000e+00 | 0.957049449535 | 0.987600893399 |

## Recomputed fold aggregates

### matbench_expt_is_metal

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| accuracy | 0.91607176757 | 0.926903553299 | 0.904471544715 | 0.0072540465199 |
| balanced_accuracy | 0.91605150328 | 0.926853401717 | 0.904503015781 | 0.00723154613987 |
| f1 | 0.915321800781 | 0.925465838509 | 0.904858299595 | 0.00676906894697 |
| rocauc | 0.91605150328 | 0.926853401717 | 0.904503015781 | 0.00723154613987 |

### matbench_glass

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| accuracy | 0.969190140845 | 0.978873239437 | 0.962147887324 | 0.00591821701196 |
| balanced_accuracy | 0.960311182924 | 0.974327973695 | 0.953893176348 | 0.00754866866747 |
| f1 | 0.978380170771 | 0.985130111524 | 0.973341599504 | 0.00417043559708 |
| rocauc | 0.960311182924 | 0.974327973695 | 0.953893176348 | 0.00754866866747 |



## 6. Source artifact inventory

# Matbench v0.1 source artifact inventory

- Submission directories scanned: 28
- Direct `run.py` files: 11
- Notebook sources: 14
- Pickle/joblib model artifacts: 1

## Disposition counts

| Disposition | Count |
|---|---:|
| artifact-only or unclear source path | 1 |
| best bounded replay candidate | 1 |
| dependency-conflicting AutoML runner | 1 |
| external/heavy MODNet path | 2 |
| heavy neural dependency path | 12 |
| notebook-only source | 9 |
| source runner present; inspect manually | 2 |

## Submission inventory

| Submission | Algorithm | Tasks | Source artifacts | Model artifacts | Signals | Disposition |
|---|---|---:|---|---|---|---|
| matbench_v0.1_alignn | ALIGNN | 9 | run.py | config_example.json |  | heavy neural dependency path |
| matbench_v0.1_Auto-sklearn | AutoML-Mat | 1 | environment.yml, notebook.ipynb |  | seed, fit, predict, external_repo | dependency-conflicting AutoML runner |
| matbench_v0.1_automatminer_expressv2020 | AMMExpress v2020 | 13 | notebook.ipynb |  | fit, predict, external_repo | notebook-only source |
| matbench_v0.1_Ax_10_90_CrabNet_v1.2.7 | Ax(10/90)+CrabNet v1.2.7 | 1 | gpei_submitit.py, notebook.ipynb |  | pickle, external_repo | notebook-only source |
| matbench_v0.1_Ax_CrabNet_v1.2.1 | Ax+CrabNet v1.2.1 | 1 | notebook.ipynb |  | seed, predict, external_repo | notebook-only source |
| matbench_v0.1_Ax_SAASBO_CrabNet_v1.2.7 | Ax/SAASBO CrabNet v1.2.7 | 1 | notebook.ipynb, saas_submitit.py |  | pickle, external_repo | notebook-only source |
| matbench_v0.1_cgcnnv2019 | CGCNN v2019 | 9 | run.py |  |  | source runner present; inspect manually |
| matbench_v0.1_coGN | coGN | 9 | preprocessing.py, run.py |  | fit, predict | heavy neural dependency path |
| matbench_v0.1_coNGN | coNGN | 9 | preprocess_crystal.py, processing.py, run.py |  | fit, predict | heavy neural dependency path |
| matbench_v0.1_CrabNet | CrabNet | 10 | notebook.ipynb |  | seed | notebook-only source |
| matbench_v0.1_CrabNet_v1.2.1 | CrabNet v1.2.1 | 1 | notebook.ipynb |  | predict, external_repo | notebook-only source |
| matbench_v0.1_darwin | Darwin | 4 | preprocessing.py, run.py |  | external_repo | heavy neural dependency path |
| matbench_v0.1_DeeperGATGNN | DeeperGATGNN | 8 | config.yml, deep_gatgnn.py, main.py, training.py |  | seed, predict | heavy neural dependency path |
| matbench_v0.1_DimeNetPP_kgcnn_v2.1.0 | DimeNet++ (kgcnn v2.1.0) | 9 | run.py |  | fit, predict | heavy neural dependency path |
| matbench_v0.1_dummy | Dummy | 13 | notebook.ipynb |  | fit, predict | notebook-only source |
| matbench_v0.1_Finder_v1.2_composition | Finder_v1.2 composition-only version | 8 | matbench_test.py |  | seed, external_repo | heavy neural dependency path |
| matbench_v0.1_Finder_v1.2_structure | Finder_v1.2 structure-based version | 8 | matbench_test.py |  | seed, external_repo | heavy neural dependency path |
| matbench_v0.1_GN-OA | GN-OA v1 | 1 | GN_OA.ipynb |  |  | heavy neural dependency path |
| matbench_v0.1_gptchem | gptchem | 4 | run_experiments_classification.py, run_experiments_regression.py |  | fit, predict, pickle, external_repo | artifact-only or unclear source path |
| matbench_v0.1_lattice_xgboost | Lattice-XGBoost | 1 | notebook.ipynb |  | predict, external_repo | notebook-only source |
| matbench_v0.1_matformer | Matformer | 1 | config.py, data.py, train.py, train_matbench.py, train_on_folder.py | config_example.json | seed, fit, pickle | heavy neural dependency path |
| matbench_v0.1_MegNet_kgcnn_v2.1.0 | MegNet (kgcnn v2.1.0) | 9 | run.py |  | fit, predict | heavy neural dependency path |
| matbench_v0.1_modnet_v0.1.10 | MODNet (v0.1.10) | 13 | benchmarks.ipynb, run.py |  | predict, pickle, external_repo | external/heavy MODNet path |
| matbench_v0.1_modnet_v0.1.12 | MODNet (v0.1.12) | 13 | benchmarks.ipynb, run.py |  | predict, pickle, external_repo | external/heavy MODNet path |
| matbench_v0.1_rf | RF-SCM/Magpie | 13 | run.py |  | fit, predict | source runner present; inspect manually |
| matbench_v0.1_RFLR | RF-Regex Steels | 1 | Matbench_Steels_RFLR.ipynb |  | seed, fit, predict | notebook-only source |
| matbench_v0.1_SchNet_kgcnn_v2.1.0 | SchNet (kgcnn v2.1.0) | 9 | run.py |  | fit, predict | heavy neural dependency path |
| matbench_v0.1_TPOT | TPOT-Mat | 1 | Matbench_steel_TPOT.ipynb, utils.py | tpot_best_pipeline.pkl | fit, predict, pickle | best bounded replay candidate |

## Interpretation

`matbench_v0.1_TPOT` stands out as the best bounded Layer B target because it has one small task, a notebook, a submitted helper, and a pickled pipeline artifact. Many other submissions are either notebook-only without saved fold-level models, full-run AutoML paths, or neural/external repositories with heavier dependencies.



## 6b. Layer B candidate triage

# Matbench v0.1 Layer B candidate triage

This ranks public Matbench v0.1 submission artifacts for bounded source replays. The score is a triage heuristic, not a claim about scientific quality.

- Submissions checked: 28
- High-priority candidates: 0
- Medium-priority candidates: 1
- Low-priority candidates: 24
- Already replayed: 3
- Positive-control candidates: 0

## Decision

`matbench_v0.1_RFLR` was selected as the best next nontrivial bounded CPU replay target after TPOT-Mat. It has one small `matbench_steels` task, simple scikit-learn/numpy/matbench requirements, notebook source, and seed/fit/predict signals. The follow-up replay is prediction-identical in `layer_b_rflr_steels_replay.md`.

`matbench_v0.1_dummy` was also replayed on the low-cost composition subset as a positive control: regression folds are exact and stratified classification folds are non-identical without a persisted RNG state. `matbench_v0.1_lattice_xgboost` is a plausible later one-task baseline, but it targets the large `matbench_mp_e_form` task and is notebook-only.

## Next remaining candidates

| Rank | Submission | Tasks | Score | Priority | Evidence | Recommendation |
|---:|---|---|---:|---|---|---|

## Full ranking

| Submission | Algorithm | Tasks | Source | Saved models | Score | Priority | Recommendation |
|---|---|---:|---|---|---:|---|---|
| matbench_v0.1_TPOT | TPOT-Mat | 1 | Matbench_steel_TPOT.ipynb, utils.py | tpot_best_pipeline.pkl | 93 | already replayed | Already used for the first bounded Layer B replay; runnable but not prediction-identical. |
| matbench_v0.1_RFLR | RF-Regex Steels | 1 | Matbench_Steels_RFLR.ipynb |  | 78 | already replayed | Already replayed after triage; prediction-identical in `layer_b_rflr_steels_replay.md`. |
| matbench_v0.1_Auto-sklearn | AutoML-Mat | 1 | environment.yml, notebook.ipynb |  | 46 | medium | Defer for now; Auto-sklearn environment conflicts make this a poor next smoke. |
| matbench_v0.1_lattice_xgboost | Lattice-XGBoost | 1 | notebook.ipynb |  | 28 | low | Bounded one-task baseline, but large MP e_form data and notebook-only source. |
| matbench_v0.1_gptchem | gptchem | 4 | run_experiments_classification.py, run_experiments_regression.py |  | 21 | low | Defer for now; source path depends on external repository or service state. |
| matbench_v0.1_Ax_10_90_CrabNet_v1.2.7 | Ax(10/90)+CrabNet v1.2.7 | 1 | gpei_submitit.py, notebook.ipynb, utils/extraordinary.py, utils/fractional.py, +6 more |  | 16 | low | Defer for now; dependency stack is heavier than needed for the next bounded pass. |
| matbench_v0.1_Ax_CrabNet_v1.2.1 | Ax+CrabNet v1.2.1 | 1 | notebook.ipynb |  | 16 | low | Defer for now; dependency stack is heavier than needed for the next bounded pass. |
| matbench_v0.1_Ax_SAASBO_CrabNet_v1.2.7 | Ax/SAASBO CrabNet v1.2.7 | 1 | notebook.ipynb, saas_submitit.py, utils/matbench.py, utils/metrics.py, +3 more |  | 16 | low | Defer for now; dependency stack is heavier than needed for the next bounded pass. |
| matbench_v0.1_darwin | Darwin | 4 | preprocessing.py, run.py |  | 8 | low | Defer for now; dependency stack is heavier than needed for the next bounded pass. |
| matbench_v0.1_rf | RF-SCM/Magpie | 13 | run.py |  | 7 | low | Useful reference runner, but all 13 tasks and unseeded RF make exact replay unlikely. |
| matbench_v0.1_CrabNet_v1.2.1 | CrabNet v1.2.1 | 1 | notebook.ipynb |  | 6 | low | Defer for now; dependency stack is heavier than needed for the next bounded pass. |
| matbench_v0.1_alignn | ALIGNN | 9 | run.py |  | 0 | low | Defer for now; dependency stack is heavier than needed for the next bounded pass. |
| matbench_v0.1_automatminer_expressv2020 | AMMExpress v2020 | 13 | notebook.ipynb |  | 0 | low | Defer for now; source path depends on external repository or service state. |
| matbench_v0.1_cgcnnv2019 | CGCNN v2019 | 9 | run.py |  | 0 | low | Defer for now; source path depends on external repository or service state. |
| matbench_v0.1_coGN | coGN | 9 | preprocessing.py, run.py |  | 0 | low | Defer for now; dependency stack is heavier than needed for the next bounded pass. |
| matbench_v0.1_coNGN | coNGN | 9 | preprocess_crystal.py, processing.py, run.py |  | 0 | low | Defer for now; dependency stack is heavier than needed for the next bounded pass. |
| matbench_v0.1_CrabNet | CrabNet | 10 | notebook.ipynb |  | 0 | low | Defer for now; dependency stack is heavier than needed for the next bounded pass. |
| matbench_v0.1_DeeperGATGNN | DeeperGATGNN | 8 | config.yml, deep_gatgnn.py, main.py, training.py |  | 0 | low | Defer for now; dependency stack is heavier than needed for the next bounded pass. |
| matbench_v0.1_DimeNetPP_kgcnn_v2.1.0 | DimeNet++ (kgcnn v2.1.0) | 9 | run.py |  | 0 | low | Defer for now; dependency stack is heavier than needed for the next bounded pass. |
| matbench_v0.1_dummy | Dummy | 13 | notebook.ipynb |  | 0 | already replayed | Already replayed on the low-cost composition subset; regression folds are exact and stratified classification folds are non-identical without a persisted RNG state. |
| matbench_v0.1_Finder_v1.2_composition | Finder_v1.2 composition-only version | 8 | matbench_test.py |  | 0 | low | Defer for now; dependency stack is heavier than needed for the next bounded pass. |
| matbench_v0.1_Finder_v1.2_structure | Finder_v1.2 structure-based version | 8 | matbench_test.py |  | 0 | low | Defer for now; dependency stack is heavier than needed for the next bounded pass. |
| matbench_v0.1_GN-OA | GN-OA v1 | 1 | GN_OA.ipynb |  | 0 | low | Defer for now; dependency stack is heavier than needed for the next bounded pass. |
| matbench_v0.1_matformer | Matformer | 1 | config.py, data.py, train.py, train_matbench.py, +1 more |  | 0 | low | Defer for now; dependency stack is heavier than needed for the next bounded pass. |
| matbench_v0.1_MegNet_kgcnn_v2.1.0 | MegNet (kgcnn v2.1.0) | 9 | run.py |  | 0 | low | Defer for now; dependency stack is heavier than needed for the next bounded pass. |
| matbench_v0.1_modnet_v0.1.10 | MODNet (v0.1.10) | 13 | benchmarks.ipynb, run.py |  | 0 | low | Defer for now; dependency stack is heavier than needed for the next bounded pass. |
| matbench_v0.1_modnet_v0.1.12 | MODNet (v0.1.12) | 13 | benchmarks.ipynb, run.py |  | 0 | low | Defer for now; dependency stack is heavier than needed for the next bounded pass. |
| matbench_v0.1_SchNet_kgcnn_v2.1.0 | SchNet (kgcnn v2.1.0) | 9 | run.py |  | 0 | low | Defer for now; dependency stack is heavier than needed for the next bounded pass. |

## Scoring notes

The heuristic rewards one-task scope, low-cost tasks, direct source runners, notebooks, saved model artifacts, seed signals, fit/predict signals, and simple CPU dependencies. It penalizes large MP tasks, heavy neural stacks, external repository/service paths, many-task submissions, and missing source.



## 7. Layer B TPOT steels source replay

# Matbench v0.1 TPOT steels source replay

- Submission: `matbench_v0.1_TPOT` / `TPOT-Mat`
- Task: `matbench_steels`
- Source artifacts used: `Matbench_steel_TPOT.ipynb`, `utils.py`, `tpot_best_pipeline.pkl`, `results.json.gz`
- Python environment: `env/matbench-tpot`
- Audit random seed: `0`
- Folds replayed: 5
- Max absolute prediction delta vs submitted artifact: 1.629e+02
- Max absolute score delta vs submitted artifact: 2.477e+01

## Method

The replay mirrors the notebook path: load the pickled TPOT pipeline, load Matbench's steels folds, convert composition strings with the submitted `LoadExisting.cleaning` helper, refit the pipeline on each training fold, predict the held-out fold, then compare with the committed `results.json.gz` predictions and stored scores. The submitted notebook does not set a random seed; this audit sets one so the replay report is stable.

## Fold comparison

| Fold | Train n | Test n | Max prediction delta | Mean prediction delta | Submitted MAE | Replay MAE | MAE delta |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 249 | 63 | 162.894287109 | 17.8011435857 | 105.636302161 | 100.433370536 | 5.20293162512 |
| 1 | 249 | 63 | 76.1984863281 | 17.4563530816 | 66.3153579954 | 66.5803722563 | 0.265014260913 |
| 2 | 250 | 62 | 95.1945800781 | 17.3075896232 | 78.2786392704 | 78.4412038495 | 0.162564579133 |
| 3 | 250 | 62 | 122.348510742 | 20.5586784117 | 77.9676911385 | 75.5824372322 | 2.38525390625 |
| 4 | 250 | 62 | 59.8782958984 | 16.3402532762 | 71.5360627205 | 74.4317926222 | 2.89572990171 |



## 7b. Layer B RFLR steels source replay

# Matbench v0.1 RFLR steels source replay

- Submission: `matbench_v0.1_RFLR` / `RF-Regex Steels`
- Task: `matbench_steels`
- Source artifacts used: `Matbench_Steels_RFLR.ipynb`, `results.json.gz`
- Python environment: `env/matbench-tpot`
- scikit-learn version: `1.2.2`
- Model: `RandomForestRegressor(n_estimators=30, random_state=1)`
- Folds replayed: 5
- Max absolute prediction delta vs submitted artifact: 0.000e+00
- Max absolute score delta vs submitted artifact: 0.000e+00

## Method

The replay mirrors the submitted notebook: convert each steel composition string into 13 fixed element-fraction columns with the notebook regex, fit a 30-tree scikit-learn random forest with `random_state=1` on each official training fold, predict the held-out fold, then compare with the committed `results.json.gz` predictions and stored scores.

## Fold comparison

| Fold | Train n | Test n | Max prediction delta | Mean prediction delta | Submitted MAE | Replay MAE | MAE delta | Max score delta |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 249 | 63 | 0 | 0 | 97.5403703704 | 97.5403703704 | 0 | 0 |
| 1 | 249 | 63 | 0 | 0 | 86.2788888889 | 86.2788888889 | 0 | 0 |
| 2 | 250 | 62 | 0 | 0 | 79.5098924731 | 79.5098924731 | 0 | 0 |
| 3 | 250 | 62 | 0 | 0 | 94.5817204301 | 94.5817204301 | 0 | 0 |
| 4 | 250 | 62 | 0 | 0 | 95.0371505376 | 95.0371505376 | 0 | 0 |

## Interpretation

The source replay is prediction-identical to the submitted artifact.

## Version note

A logged control run in env/jarvis with scikit-learn 1.9.0 was runnable but non-identical (max prediction delta 108.587, max score delta 22.307). The prediction-identical replay above uses scikit-learn 1.2.2.



## 7c. Layer B Dummy composition source replay

# Matbench v0.1 Dummy source replay

- Submission: `matbench_v0.1_dummy` / `Dummy`
- Tasks replayed: 4
- Folds replayed: 20
- Python environment: `env/matbench-tpot`
- scikit-learn version: `1.2.2`
- Audit NumPy seed: `0`
- Exact prediction+score folds: 10 / 20
- Regression exact folds: 10 / 10
- Classification exact folds: 0 / 10
- Max prediction delta / mismatch rate: 5.020e-01
- Max score delta: 4.487e-02

## Method

The replay mirrors the submitted notebook logic on a bounded low-cost task subset: `DummyRegressor(strategy="mean")` for regression and `DummyClassifier(strategy="stratified")` for classification. The notebook does not record a random seed for the stratified classifier, so this audit sets a NumPy seed only to make the replay deterministic.

## Fold comparison

| Task | Fold | Type | Test n | Prediction delta / mismatch rate | Primary stored | Primary replay | Primary delta | Max score delta |
|---|---:|---|---:|---:|---:|---:|---:|---:|
| matbench_expt_gap | 0 | regression | 921 | 0 | 1.09646800468 | 1.09646800468 | 0 | 0 |
| matbench_expt_gap | 1 | regression | 921 | 0 | 1.19221192656 | 1.19221192656 | 0 | 0 |
| matbench_expt_gap | 2 | regression | 921 | 0 | 1.15268817052 | 1.15268817052 | 0 | 0 |
| matbench_expt_gap | 3 | regression | 921 | 0 | 1.1445202552 | 1.1445202552 | 0 | 0 |
| matbench_expt_gap | 4 | regression | 920 | 0 | 1.13174644762 | 1.13174644762 | 0 | 0 |
| matbench_expt_is_metal | 0 | classification | 985 | 0.489340101523 | 0.469965450992 | 0.502477798758 | 0.0325123477659 | 0.0377263494158 |
| matbench_expt_is_metal | 1 | classification | 984 | 0.502032520325 | 0.500074361728 | 0.514302239114 | 0.0142278773858 | 0.0142278773858 |
| matbench_expt_is_metal | 2 | classification | 984 | 0.485772357724 | 0.487812938941 | 0.491861521937 | 0.00404858299595 | 0.00406504065041 |
| matbench_expt_is_metal | 3 | classification | 984 | 0.475609756098 | 0.507167644386 | 0.521222011072 | 0.0140543666859 | 0.0142276422764 |
| matbench_expt_is_metal | 4 | classification | 984 | 0.5 | 0.49693877551 | 0.488742460547 | 0.00819631496323 | 0.016708086854 |
| matbench_glass | 0 | classification | 1136 | 0.397887323944 | 0.521244581041 | 0.496355973379 | 0.0248886076617 | 0.0264084507042 |
| matbench_glass | 1 | classification | 1136 | 0.426936619718 | 0.521747400218 | 0.486115034482 | 0.035632365736 | 0.035632365736 |
| matbench_glass | 2 | classification | 1136 | 0.406690140845 | 0.484759117599 | 0.515048794176 | 0.0302896765762 | 0.0302896765762 |
| matbench_glass | 3 | classification | 1136 | 0.414612676056 | 0.479860867862 | 0.524728534141 | 0.0448676662787 | 0.0448676662787 |
| matbench_glass | 4 | classification | 1136 | 0.399647887324 | 0.495058436251 | 0.500237285454 | 0.00517884920321 | 0.00517884920321 |
| matbench_steels | 0 | regression | 63 | 0 | 241.459074393 | 241.459074393 | 0 | 0 |
| matbench_steels | 1 | regression | 63 | 0 | 219.377031937 | 219.377031937 | 0 | 0 |
| matbench_steels | 2 | regression | 62 | 0 | 225.793225806 | 225.793225806 | 0 | 0 |
| matbench_steels | 3 | regression | 62 | 0 | 241.203522581 | 241.203522581 | 0 | 0 |
| matbench_steels | 4 | regression | 62 | 0 | 220.889793548 | 220.889793548 | 0 | 0 |

## Interpretation

The mean-regression dummy source path is prediction-identical for the checked regression folds. The stratified classification dummy source path is runnable but not prediction-identical under the audit seed, which is expected because the submitted notebook did not persist the RNG state or a classifier `random_state`.



## 7d. Layer C leaderboard resolution map

# Matbench v0.1 leaderboard resolution map

This uses stored fold scores from public `results.json.gz` artifacts. For each task, submissions are ranked by the primary leaderboard metric (`mae` for regression, stored `rocauc` for classification), then adjacent mean gaps are compared with a fold-level standard-error proxy from the five paired fold-score differences.

Classification caveat: the stored `rocauc` values in these artifacts behave as thresholded-label AUC / balanced accuracy for the checked records, as documented in the classification probe.

- Submission-task rows ranked: 180
- Tasks ranked: 13
- Adjacent pairs: 167
- Exact adjacent ties: 6
- Adjacent gaps <= 1 fold-SE proxy: 68
- Adjacent gaps <= 2 fold-SE proxy: 87
- Regression adjacent pairs: 143
- Classification adjacent pairs: 24

## Per-task resolution

| Task | Type | Metric | Entries | Adjacent pairs | Exact ties | <=1 SE | <=2 SE | Min gap | Median gap | Min gap / SE |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|
| matbench_dielectric | regression | mae | 16 | 15 | 0 | 11 | 11 | 0.000709045 | 0.00491146 | 0.0433745 |
| matbench_expt_gap | regression | mae | 12 | 11 | 0 | 5 | 7 | 0.000750008 | 0.0125305 | 0.0659425 |
| matbench_expt_is_metal | classification | rocauc | 7 | 6 | 1 | 2 | 3 | 0 | 0.0118908 | 0 |
| matbench_glass | classification | rocauc | 7 | 6 | 0 | 1 | 2 | 0.00197173 | 0.0412622 | 0.161961 |
| matbench_jdft2d | regression | mae | 16 | 15 | 0 | 11 | 14 | 0.14923 | 1.34496 | 0.0721843 |
| matbench_log_gvrh | regression | mae | 16 | 15 | 1 | 5 | 6 | 0 | 0.00188593 | 0 |
| matbench_log_kvrh | regression | mae | 16 | 15 | 1 | 4 | 6 | 0 | 0.00202217 | 0 |
| matbench_mp_e_form | regression | mae | 18 | 17 | 1 | 4 | 4 | 0 | 0.00225949 | 0 |
| matbench_mp_gap | regression | mae | 16 | 15 | 1 | 3 | 5 | 0 | 0.0134738 | 0 |
| matbench_mp_is_metal | classification | rocauc | 13 | 12 | 0 | 6 | 6 | 0.000383175 | 0.0040911 | 0.110668 |
| matbench_perovskites | regression | mae | 16 | 15 | 1 | 3 | 4 | 0 | 0.00301299 | 0 |
| matbench_phonons | regression | mae | 16 | 15 | 0 | 8 | 11 | 0.126783 | 1.59285 | 0.111603 |
| matbench_steels | regression | mae | 11 | 10 | 0 | 5 | 8 | 1.279 | 5.54138 | 0.210305 |

## Closest adjacent pairs by fold-SE proxy

| Task | Rank | Better | Worse | Metric | Better mean | Worse mean | Gap | Fold-SE proxy | Gap / SE |
|---|---:|---|---|---|---:|---:|---:|---:|---:|
| matbench_expt_is_metal | 4 | matbench_v0.1_modnet_v0.1.10 | matbench_v0.1_modnet_v0.1.12 | rocauc | 0.916052 | 0.916052 | 0 | 0 | 0 |
| matbench_log_gvrh | 4 | matbench_v0.1_modnet_v0.1.10 | matbench_v0.1_modnet_v0.1.12 | mae | 0.0731162 | 0.0731162 | 0 | 0 | 0 |
| matbench_log_kvrh | 3 | matbench_v0.1_modnet_v0.1.10 | matbench_v0.1_modnet_v0.1.12 | mae | 0.05477 | 0.05477 | 0 | 0 | 0 |
| matbench_mp_e_form | 11 | matbench_v0.1_modnet_v0.1.10 | matbench_v0.1_modnet_v0.1.12 | mae | 0.0447692 | 0.0447692 | 0 | 0 | 0 |
| matbench_mp_gap | 8 | matbench_v0.1_modnet_v0.1.10 | matbench_v0.1_modnet_v0.1.12 | mae | 0.219872 | 0.219872 | 0 | 0 | 0 |
| matbench_perovskites | 10 | matbench_v0.1_modnet_v0.1.10 | matbench_v0.1_modnet_v0.1.12 | mae | 0.0907542 | 0.0907542 | 0 | 0 | 0 |
| matbench_dielectric | 4 | matbench_v0.1_coNGN | matbench_v0.1_automatminer_expressv2020 | mae | 0.314157 | 0.315029 | 0.00087203 | 0.0201047 | 0.0433745 |
| matbench_dielectric | 11 | matbench_v0.1_MegNet_kgcnn_v2.1.0 | matbench_v0.1_DimeNetPP_kgcnn_v2.1.0 | mae | 0.339066 | 0.340007 | 0.000941329 | 0.0155406 | 0.0605722 |
| matbench_expt_gap | 4 | matbench_v0.1_CrabNet | matbench_v0.1_modnet_v0.1.10 | mae | 0.346265 | 0.347015 | 0.000750008 | 0.0113737 | 0.0659425 |
| matbench_jdft2d | 8 | matbench_v0.1_DeeperGATGNN | matbench_v0.1_CrabNet | mae | 45.4611 | 45.6104 | 0.14923 | 2.06735 | 0.0721843 |
| matbench_mp_is_metal | 6 | matbench_v0.1_modnet_v0.1.12 | matbench_v0.1_DimeNetPP_kgcnn_v2.1.0 | rocauc | 0.903809 | 0.903168 | 0.000641083 | 0.00579286 | 0.110668 |
| matbench_phonons | 1 | matbench_v0.1_MegNet_kgcnn_v2.1.0 | matbench_v0.1_coNGN | mae | 28.7606 | 28.8874 | 0.126783 | 1.13602 | 0.111603 |
| matbench_dielectric | 6 | matbench_v0.1_Finder_v1.2_structure | matbench_v0.1_Finder_v1.2_composition | mae | 0.319656 | 0.320366 | 0.000709045 | 0.00628733 | 0.112774 |
| matbench_jdft2d | 12 | matbench_v0.1_DimeNetPP_kgcnn_v2.1.0 | matbench_v0.1_cgcnnv2019 | mae | 49.0243 | 49.244 | 0.219754 | 1.93619 | 0.113498 |
| matbench_mp_gap | 2 | matbench_v0.1_DeeperGATGNN | matbench_v0.1_coNGN | mae | 0.16937 | 0.169684 | 0.000314041 | 0.00269319 | 0.116606 |
| matbench_perovskites | 2 | matbench_v0.1_alignn | matbench_v0.1_DeeperGATGNN | mae | 0.0287655 | 0.0288114 | 4.58128e-05 | 0.000388605 | 0.11789 |
| matbench_glass | 2 | matbench_v0.1_automatminer_expressv2020 | matbench_v0.1_rf | rocauc | 0.860672 | 0.858701 | 0.00197173 | 0.0121741 | 0.161961 |
| matbench_expt_gap | 2 | matbench_v0.1_Ax_SAASBO_CrabNet_v1.2.7 | matbench_v0.1_modnet_v0.1.12 | mae | 0.330975 | 0.332674 | 0.00169891 | 0.00985325 | 0.172421 |
| matbench_mp_e_form | 8 | matbench_v0.1_cgcnnv2019 | matbench_v0.1_DeeperGATGNN | mae | 0.0337208 | 0.0339587 | 0.000237907 | 0.00131737 | 0.180593 |
| matbench_dielectric | 7 | matbench_v0.1_Finder_v1.2_composition | matbench_v0.1_CrabNet | mae | 0.320366 | 0.323352 | 0.00298632 | 0.0157631 | 0.18945 |
| matbench_mp_gap | 7 | matbench_v0.1_Finder_v1.2_structure | matbench_v0.1_modnet_v0.1.10 | mae | 0.219283 | 0.219872 | 0.000589556 | 0.00294238 | 0.200367 |
| matbench_dielectric | 12 | matbench_v0.1_DimeNetPP_kgcnn_v2.1.0 | matbench_v0.1_alignn | mae | 0.340007 | 0.344918 | 0.00491146 | 0.0236748 | 0.207455 |
| matbench_steels | 5 | matbench_v0.1_modnet_v0.1.10 | matbench_v0.1_automatminer_expressv2020 | mae | 96.2139 | 97.4929 | 1.279 | 6.08162 | 0.210305 |
| matbench_log_gvrh | 8 | matbench_v0.1_MegNet_kgcnn_v2.1.0 | matbench_v0.1_automatminer_expressv2020 | mae | 0.0871107 | 0.08741 | 0.000299287 | 0.00131458 | 0.227668 |
| matbench_expt_is_metal | 3 | matbench_v0.1_rf | matbench_v0.1_modnet_v0.1.10 | rocauc | 0.916659 | 0.916052 | 0.000607287 | 0.00255684 | 0.237515 |

## Smallest raw adjacent gaps

| Task | Rank | Better | Worse | Metric | Gap | Gap / SE |
|---|---:|---|---|---|---:|---:|
| matbench_expt_is_metal | 4 | matbench_v0.1_modnet_v0.1.10 | matbench_v0.1_modnet_v0.1.12 | rocauc | 0 | 0 |
| matbench_log_gvrh | 4 | matbench_v0.1_modnet_v0.1.10 | matbench_v0.1_modnet_v0.1.12 | mae | 0 | 0 |
| matbench_log_kvrh | 3 | matbench_v0.1_modnet_v0.1.10 | matbench_v0.1_modnet_v0.1.12 | mae | 0 | 0 |
| matbench_mp_e_form | 11 | matbench_v0.1_modnet_v0.1.10 | matbench_v0.1_modnet_v0.1.12 | mae | 0 | 0 |
| matbench_mp_gap | 8 | matbench_v0.1_modnet_v0.1.10 | matbench_v0.1_modnet_v0.1.12 | mae | 0 | 0 |
| matbench_perovskites | 10 | matbench_v0.1_modnet_v0.1.10 | matbench_v0.1_modnet_v0.1.12 | mae | 0 | 0 |
| matbench_perovskites | 2 | matbench_v0.1_alignn | matbench_v0.1_DeeperGATGNN | mae | 4.58128e-05 | 0.11789 |
| matbench_perovskites | 3 | matbench_v0.1_DeeperGATGNN | matbench_v0.1_coNGN | mae | 0.000172379 | 0.416664 |
| matbench_mp_e_form | 8 | matbench_v0.1_cgcnnv2019 | matbench_v0.1_DeeperGATGNN | mae | 0.000237907 | 0.180593 |
| matbench_mp_e_form | 3 | matbench_v0.1_alignn | matbench_v0.1_SchNet_kgcnn_v2.1.0 | mae | 0.000287615 | 0.909748 |
| matbench_log_gvrh | 8 | matbench_v0.1_MegNet_kgcnn_v2.1.0 | matbench_v0.1_automatminer_expressv2020 | mae | 0.000299287 | 0.227668 |
| matbench_mp_gap | 2 | matbench_v0.1_DeeperGATGNN | matbench_v0.1_coNGN | mae | 0.000314041 | 0.116606 |
| matbench_mp_e_form | 9 | matbench_v0.1_DeeperGATGNN | matbench_v0.1_Finder_v1.2_structure | mae | 0.000360029 | 0.265289 |
| matbench_mp_is_metal | 4 | matbench_v0.1_automatminer_expressv2020 | matbench_v0.1_coNGN | rocauc | 0.000383175 | 0.347879 |
| matbench_log_gvrh | 6 | matbench_v0.1_DimeNetPP_kgcnn_v2.1.0 | matbench_v0.1_SchNet_kgcnn_v2.1.0 | mae | 0.000394917 | 0.53175 |
| matbench_mp_is_metal | 2 | matbench_v0.1_alignn | matbench_v0.1_coGN | rocauc | 0.000395411 | 0.546968 |
| matbench_mp_e_form | 6 | matbench_v0.1_GN-OA | matbench_v0.1_MegNet_kgcnn_v2.1.0 | mae | 0.000431652 | 3.40465 |
| matbench_log_kvrh | 5 | matbench_v0.1_alignn | matbench_v0.1_DimeNetPP_kgcnn_v2.1.0 | mae | 0.000446188 | 0.905221 |
| matbench_log_kvrh | 10 | matbench_v0.1_Finder_v1.2_structure | matbench_v0.1_DeeperGATGNN | mae | 0.000535312 | 0.761792 |
| matbench_mp_gap | 7 | matbench_v0.1_Finder_v1.2_structure | matbench_v0.1_modnet_v0.1.10 | mae | 0.000589556 | 0.200367 |
| matbench_expt_is_metal | 3 | matbench_v0.1_rf | matbench_v0.1_modnet_v0.1.10 | rocauc | 0.000607287 | 0.237515 |
| matbench_log_kvrh | 13 | matbench_v0.1_CrabNet | matbench_v0.1_Finder_v1.2_composition | mae | 0.00061045 | 0.593142 |
| matbench_mp_is_metal | 6 | matbench_v0.1_modnet_v0.1.12 | matbench_v0.1_DimeNetPP_kgcnn_v2.1.0 | rocauc | 0.000641083 | 0.110668 |
| matbench_dielectric | 6 | matbench_v0.1_Finder_v1.2_structure | matbench_v0.1_Finder_v1.2_composition | mae | 0.000709045 | 0.112774 |
| matbench_log_gvrh | 10 | matbench_v0.1_cgcnnv2019 | matbench_v0.1_DeeperGATGNN | mae | 0.000716145 | 0.643009 |

## Interpretation

This is a leaderboard-resolution screen, not a formal significance test. It shows where adjacent point estimates are narrow relative to fold-to-fold metric variation. Exact ties and gaps below one fold-SE proxy should be treated as unresolved without a stronger paired uncertainty analysis.



## 7e. Layer C close-pair fold bootstrap

# Matbench v0.1 fold-bootstrap adjacent-pair screen

This is a follow-up to `layer_c_leaderboard_resolution.md`. It takes the closest adjacent leaderboard pairs by gap/fold-SE proxy, then bootstraps the five paired fold-score differences. Positive differences mean the higher-ranked submission remains better under the task's primary metric.

This is a lightweight fold-level uncertainty screen, not a formal statistical test. It has only five folds per pair, and classification uses stored `rocauc`, which behaves as thresholded-label AUC / balanced accuracy for the checked records.

- Adjacent pairs checked: 25
- Bootstrap draws per pair: 20000
- RNG seed: 0
- 95% bootstrap CIs including zero: 25
- P(bootstrapped gap <= 0) >= 0.05: 25
- Exact adjacent ties in checked set: 6

## Pair results

| Task | Rank | Better | Worse | Metric | Gap | Gap / SE | CI low | CI high | P(gap <= 0) | CI includes 0 |
|---|---:|---|---|---|---:|---:|---:|---:|---:|---|
| matbench_expt_is_metal | 4 | matbench_v0.1_modnet_v0.1.10 | matbench_v0.1_modnet_v0.1.12 | rocauc | 0 | 0 | 0 | 0 | 1 | yes |
| matbench_log_gvrh | 4 | matbench_v0.1_modnet_v0.1.10 | matbench_v0.1_modnet_v0.1.12 | mae | 0 | 0 | 0 | 0 | 1 | yes |
| matbench_log_kvrh | 3 | matbench_v0.1_modnet_v0.1.10 | matbench_v0.1_modnet_v0.1.12 | mae | 0 | 0 | 0 | 0 | 1 | yes |
| matbench_mp_e_form | 11 | matbench_v0.1_modnet_v0.1.10 | matbench_v0.1_modnet_v0.1.12 | mae | 0 | 0 | 0 | 0 | 1 | yes |
| matbench_mp_gap | 8 | matbench_v0.1_modnet_v0.1.10 | matbench_v0.1_modnet_v0.1.12 | mae | 0 | 0 | 0 | 0 | 1 | yes |
| matbench_perovskites | 10 | matbench_v0.1_modnet_v0.1.10 | matbench_v0.1_modnet_v0.1.12 | mae | 0 | 0 | 0 | 0 | 1 | yes |
| matbench_dielectric | 4 | matbench_v0.1_coNGN | matbench_v0.1_automatminer_expressv2020 | mae | 0.00087203 | 0.0433745 | -0.0386628 | 0.0310366 | 0.4255 | yes |
| matbench_dielectric | 11 | matbench_v0.1_MegNet_kgcnn_v2.1.0 | matbench_v0.1_DimeNetPP_kgcnn_v2.1.0 | mae | 0.000941329 | 0.0605722 | -0.0256149 | 0.0274976 | 0.4681 | yes |
| matbench_expt_gap | 4 | matbench_v0.1_CrabNet | matbench_v0.1_modnet_v0.1.10 | mae | 0.000750008 | 0.0659425 | -0.0183764 | 0.0211091 | 0.4725 | yes |
| matbench_jdft2d | 8 | matbench_v0.1_DeeperGATGNN | matbench_v0.1_CrabNet | mae | 0.14923 | 0.0721843 | -3.96875 | 3.24105 | 0.45805 | yes |
| matbench_mp_is_metal | 6 | matbench_v0.1_modnet_v0.1.12 | matbench_v0.1_DimeNetPP_kgcnn_v2.1.0 | rocauc | 0.000641083 | 0.110668 | -0.0103745 | 0.00988183 | 0.42745 | yes |
| matbench_phonons | 1 | matbench_v0.1_MegNet_kgcnn_v2.1.0 | matbench_v0.1_coNGN | mae | 0.126783 | 0.111603 | -2.15202 | 1.43937 | 0.3151 | yes |
| matbench_dielectric | 6 | matbench_v0.1_Finder_v1.2_structure | matbench_v0.1_Finder_v1.2_composition | mae | 0.000709045 | 0.112774 | -0.0108184 | 0.0107964 | 0.4384 | yes |
| matbench_jdft2d | 12 | matbench_v0.1_DimeNetPP_kgcnn_v2.1.0 | matbench_v0.1_cgcnnv2019 | mae | 0.219754 | 0.113498 | -2.65548 | 4.00417 | 0.48355 | yes |
| matbench_mp_gap | 2 | matbench_v0.1_DeeperGATGNN | matbench_v0.1_coNGN | mae | 0.000314041 | 0.116606 | -0.00410629 | 0.0054197 | 0.4557 | yes |
| matbench_perovskites | 2 | matbench_v0.1_alignn | matbench_v0.1_DeeperGATGNN | mae | 4.58128e-05 | 0.11789 | -0.000680917 | 0.000624587 | 0.427 | yes |
| matbench_glass | 2 | matbench_v0.1_automatminer_expressv2020 | matbench_v0.1_rf | rocauc | 0.00197173 | 0.161961 | -0.0212167 | 0.0204627 | 0.39925 | yes |
| matbench_expt_gap | 2 | matbench_v0.1_Ax_SAASBO_CrabNet_v1.2.7 | matbench_v0.1_modnet_v0.1.12 | mae | 0.00169891 | 0.172421 | -0.0122981 | 0.0209692 | 0.47005 | yes |
| matbench_mp_e_form | 8 | matbench_v0.1_cgcnnv2019 | matbench_v0.1_DeeperGATGNN | mae | 0.000237907 | 0.180593 | -0.00200926 | 0.0027376 | 0.41045 | yes |
| matbench_dielectric | 7 | matbench_v0.1_Finder_v1.2_composition | matbench_v0.1_CrabNet | mae | 0.00298632 | 0.18945 | -0.0284995 | 0.0257243 | 0.3892 | yes |
| matbench_mp_gap | 7 | matbench_v0.1_Finder_v1.2_structure | matbench_v0.1_modnet_v0.1.10 | mae | 0.000589556 | 0.200367 | -0.00371107 | 0.00643074 | 0.4289 | yes |
| matbench_dielectric | 12 | matbench_v0.1_DimeNetPP_kgcnn_v2.1.0 | matbench_v0.1_alignn | mae | 0.00491146 | 0.207455 | -0.0403924 | 0.0368495 | 0.39215 | yes |
| matbench_steels | 5 | matbench_v0.1_modnet_v0.1.10 | matbench_v0.1_automatminer_expressv2020 | mae | 1.279 | 0.210305 | -9.01348 | 12.1864 | 0.42925 | yes |
| matbench_log_gvrh | 8 | matbench_v0.1_MegNet_kgcnn_v2.1.0 | matbench_v0.1_automatminer_expressv2020 | mae | 0.000299287 | 0.227668 | -0.00190315 | 0.00267186 | 0.4104 | yes |
| matbench_expt_is_metal | 3 | matbench_v0.1_rf | matbench_v0.1_modnet_v0.1.10 | rocauc | 0.000607287 | 0.237515 | -0.00430554 | 0.00468892 | 0.37515 | yes |

## Interpretation

For these closest adjacent pairs, a CI crossing zero means the five-fold score pattern does not stably separate the two neighboring submissions under this coarse fold-bootstrap screen. Exact ties are deterministic ties in the stored fold scores.



## 8. Classification ROC-AUC upstream issue draft

# Matbench upstream issue draft - classification ROC-AUC scoring

Status: ready to post/share; use `reports/paper-003_rocauc_issue_body.md` for the
clean GitHub issue body.

Target repo: https://github.com/materialsproject/matbench

Suggested title:

> Classification `rocauc` appears to be computed after float predictions are thresholded

## Draft body

Hi Matbench maintainers,

I am running an independent reproducibility audit of Matbench v0.1 leaderboard
artifacts. First, the positive result: the stored fold scores I checked are
internally reproducible from the released `results.json.gz` files, official split
IDs, and Matminer targets.

While checking classification submissions, I found a ROC-AUC scoring behavior that
looks worth confirming or documenting for submissions that record float
predictions.

### Observation

In the current scoring code, classification metrics are ordered as:

```python
CLF_METRICS = ["accuracy", "balanced_accuracy", "f1", "rocauc"]
```

My read of `matbench.data_ops.score_array` is that non-ROC classification metrics
can convert float predictions to thresholded labels by reassigning the local
`pred_array` variable. Because `accuracy` is evaluated before `rocauc`, a later
`rocauc` call appears to receive the already-thresholded labels rather than the
original float scores.

That would make the stored `rocauc` field behave as thresholded-label AUC, which is
numerically the same as balanced accuracy for binary labels.

### Evidence from public artifacts

Using the public Matbench v0.1 submission artifacts in a pinned clone
(`936176db18ca4cd7b38cbd957c017a5bac770c6b`):

- I scanned 27 classification submission-task records.
- 16 store hard bool predictions.
- 11 store float predictions.
- In all 27 records, stored `rocauc` equals stored balanced accuracy within
  numerical precision.
- The generated classification per-task leaderboards display `mean rocauc` as the
  first metric column; all 27 displayed rows have `mean rocauc == mean balanced_accuracy`.

For two small MODNet classification tasks, I reproduced the stored fold scores and
also computed ROC-AUC from the raw float predictions:

| submission | task | stored rocauc mean | raw-probability rocauc mean | mean gap |
|---|---|---:|---:|---:|
| `matbench_v0.1_modnet_v0.1.10` | `matbench_expt_is_metal` | 0.916052 | 0.972546 | 0.056495 |
| `matbench_v0.1_modnet_v0.1.10` | `matbench_glass` | 0.810676 | 0.932948 | 0.122272 |
| `matbench_v0.1_modnet_v0.1.12` | `matbench_expt_is_metal` | 0.916052 | 0.972546 | 0.056495 |
| `matbench_v0.1_modnet_v0.1.12` | `matbench_glass` | 0.960311 | 0.989876 | 0.029565 |

### Minimal code-level cause

If this read is correct, the key point is that the local prediction variable is
reused across metrics. A minimal forward-looking code fix would be to keep a copy
of the original prediction array for ROC-AUC, or compute ROC-AUC from a separate
unthresholded variable when the submitted values are floats.

Conceptually:

```python
raw_pred_array = pred_array
...
if metric == "rocauc" and isinstance(raw_pred_array[0], float):
    computed[metric] = roc_auc_score(homogenized_true_array, raw_pred_array)
```

### Suggested handling

I see three possible paths:

1. Confirm that this is the intended historical behavior and document that
   Matbench v0.1 classification `rocauc` is thresholded-label AUC for affected
   float-prediction submissions.
2. Fix the scoring code for future submissions and add a release note that historic
   Matbench v0.1 classification `rocauc` values were computed from thresholded
   labels when float predictions were submitted.
3. If a different code path explains the stored values, point me to it and I will
   update the audit notes.

I have not opened a PR because the right handling of historical leaderboard values
is a maintainer policy decision.

Thanks for maintaining the benchmark. The rest of the checked fold-score artifacts
were reproducible exactly, so this issue is specifically about interpretation of
the classification `rocauc` field.

## Local evidence files

- `papers/matbench/classification_auc_probe.md`
- `papers/matbench/classification_prediction_scan.md`
- `papers/matbench/classification_leaderboard_metric_scan.md`
- `papers/matbench/layer_a_modnet_0_1_10_probability_auc_probe.md`
- `papers/matbench/layer_a_modnet_0_1_12_probability_auc_probe.md`
- `scripts/matbench_score.py`
- `scripts/matbench_classification_scan.py`
- `scripts/matbench_leaderboard_metric_scan.py`

## Posting notes

- If posting, link the public ReproLab commit containing the scripts/reports.
- Keep the issue scoped to classification `rocauc`; do not bundle unrelated
  Matbench v0.1 audit notes.
- Post this classification issue before the narrower GN-OA MAPE issue.



## 8b. GN-OA MAPE upstream issue draft

# Matbench upstream issue draft - GN-OA MAPE exception

Status: ready as a follow-up; use `reports/paper-003_gn_oa_mape_issue_body.md`
for the clean GitHub issue body.

Target repo: https://github.com/materialsproject/matbench

Suggested title:

> `matbench_v0.1_GN-OA` stored MAPE for `matbench_mp_e_form` appears inconsistent with Matbench MAPE

## Draft body

Hi Matbench maintainers,

I am running an independent reproducibility audit of Matbench v0.1 leaderboard
artifacts. The broad result is positive: scanning the public `results.json.gz`
artifacts across 28 submissions, 180 submission-task records, and 900 folds, I
found that 179/180 submission-task records reproduce their stored fold scores to
numerical precision with the Matbench v0.1 scoring path.

The only score-recompute exception I found is narrow: `matbench_v0.1_GN-OA` on
`matbench_mp_e_form`, and only for MAPE. The same predictions and official split
IDs reproduce MAE, RMSE, and max error exactly or to floating-point precision, so
this does not look like a prediction-ID alignment problem.

### Observation

Using the Matbench v0.1 MAPE path, which masks targets with
`abs(y_true) > 1e-5`, the stored and recomputed values differ on all five folds:

| Fold | Stored MAPE | Recomputed Matbench MAPE | Delta | Other regression metrics |
|---:|---:|---:|---:|---|
| 0 | 12.5887409438 | 0.420116236715 | 12.1686247071 | match |
| 1 | 7.94659210396 | 0.137819988807 | 7.80877211515 | match |
| 2 | 9.26331433818 | 0.149750183903 | 9.11356415428 | match |
| 3 | 11.8881843898 | 0.236287007689 | 11.6518973821 | match |
| 4 | 12.1946455981 | 0.201616727224 | 11.9930288708 | match |

### Checks that did not explain the stored values

- Recomputing MAE, RMSE, and max error from the same fold predictions matches the
  stored values, which supports the official validation IDs being aligned.
- A simple unmasked MAPE is not the stored formula either. It is infinite on all
  five folds because the `matbench_mp_e_form` test targets contain exact zeros.
- Sweeping small denominator thresholds did not reproduce the stored MAPE values.

### Suggested handling

Could you confirm whether the stored GN-OA MAPE values for `matbench_mp_e_form`
were computed with a submission-specific formula, or whether this is a historical
stored-score inconsistency that should be corrected or annotated?

I have not opened a PR because the right treatment of historical leaderboard
artifacts is a maintainer policy decision. The issue is intentionally scoped to
this one submission/task/metric exception.

Thanks for maintaining the benchmark.

## Local evidence files

- `papers/matbench/layer_a_all_submission_score_scan.md`
- `papers/matbench/layer_a_gn_oa_mape_probe.md`
- `scripts/matbench_all_results_score_scan.py`
- `scripts/matbench_score.py`

## Posting notes

- If posting, link the public ReproLab commit containing the scripts/reports.
- Keep this issue separate from the classification `rocauc` draft unless the user
  explicitly asks to combine them.
- Post after the classification `rocauc` issue, not before it.



## 9. Run log (tail)

### 2026-07-03 13:45 UTC — paper003 Layer C resolution whitespace check

```
$ git diff --check
```

- exit code: **0**  | duration: 0.0s  | raw log: `logs/cmd-20260703-134545-808119.log`

output tail:
```
warning: in the working copy of 'README.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'papers/matbench/metadata.yaml', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'papers/matbench/summary.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'reports/paper-003-external_release_packet.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'scripts/make_matbench_report.py', LF will be replaced by CRLF the next time Git touches it
```

### 2026-07-03 13:45 UTC — paper003 final reassemble report after Layer C resolution checks

```
$ .venv\Scripts\python.exe scripts\make_matbench_report.py
```

- exit code: **0**  | duration: 0.1s  | raw log: `logs/cmd-20260703-134552-212321.log`

output tail:
```
wrote C:\Users\07013\Desktop\0702fable\reprolab\reports\paper-003-matbench-audit.md
```

### 2026-07-03 13:47 UTC — paper003 Matbench Layer C fold bootstrap close pairs

```
$ .venv\Scripts\python.exe scripts\matbench_leaderboard_fold_bootstrap.py --report papers\matbench\layer_c_fold_bootstrap.md --pairs 25 --draws 20000 --seed 0
```

- exit code: **0**  | duration: 4.8s  | raw log: `logs/cmd-20260703-134728-845023.log`

output tail:
```
{
  "ci_includes_zero": 25,
  "draws": 20000,
  "exact_adjacent_ties": 6,
  "p_gap_lte_zero_gte_0_05": 25,
  "pairs_checked": 25,
  "report": "papers\\matbench\\layer_c_fold_bootstrap.md",
  "resolution_report": "C:\\Users\\07013\\Desktop\\0702fable\\reprolab\\papers\\matbench\\layer_c_leaderboard_resolution.md"
}
```

### 2026-07-03 13:48 UTC — paper003 reassemble report with Layer C fold bootstrap

```
$ .venv\Scripts\python.exe scripts\make_matbench_report.py
```

- exit code: **0**  | duration: 0.1s  | raw log: `logs/cmd-20260703-134816-683582.log`

output tail:
```
wrote C:\Users\07013\Desktop\0702fable\reprolab\reports\paper-003-matbench-audit.md
```

### 2026-07-03 13:48 UTC — paper003 verify Layer C fold bootstrap docs

```
$ .venv\Scripts\python.exe -c from pathlib import Path; import py_compile, sys, yaml; py_compile.compile('scripts/matbench_leaderboard_fold_bootstrap.py', doraise=True); py_compile.compile('scripts/matbench_leaderboard_resolution.py', doraise=True); py_compile.compile('scripts/make_matbench_report.py', doraise=True); meta=yaml.safe_load(Path('papers/matbench/metadata.yaml').read_text(encoding='utf-8')); boot=Path('papers/matbench/layer_c_fold_bootstrap.md').read_text(encoding='utf-8'); summary=Path('papers/matbench/summary.md').read_text(encoding='utf-8'); assembled=Path('reports/paper-003-matbench-audit.md').read_text(encoding='utf-8'); packet=Path('reports/paper-003-external_release_packet.md').read_text(encoding='utf-8'); readme=Path('README.md').read_text(encoding='utf-8'); checks=[meta['layer_c_fold_bootstrap']['adjacent_pairs_checked']==25, meta['layer_c_fold_bootstrap']['bootstrap_ci_95_including_zero']==25, '95% bootstrap CIs including zero: 25' in boot, 'Layer C close-pair fold bootstrap' in assembled, 'layer_c_fold_bootstrap.md' in summary, 'Layer C fold bootstrap' in packet, 'layer_c_fold_bootstrap.md' in readme]; print({'checks': checks}); sys.exit(0 if all(checks) else 1)
```

- exit code: **0**  | duration: 0.1s  | raw log: `logs/cmd-20260703-134824-676175.log`

output tail:
```
{'checks': [True, True, True, True, True, True, True]}
```

### 2026-07-03 13:48 UTC — paper003 Layer C fold bootstrap whitespace check

```
$ git diff --check
```

- exit code: **0**  | duration: 0.1s  | raw log: `logs/cmd-20260703-134834-723661.log`

output tail:
```
warning: in the working copy of 'README.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'papers/matbench/metadata.yaml', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'papers/matbench/summary.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'reports/paper-003-external_release_packet.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'scripts/make_matbench_report.py', LF will be replaced by CRLF the next time Git touches it
```

### 2026-07-03 13:48 UTC — paper003 final reassemble report after Layer C fold bootstrap checks

```
$ .venv\Scripts\python.exe scripts\make_matbench_report.py
```

- exit code: **0**  | duration: 0.1s  | raw log: `logs/cmd-20260703-134841-449596.log`

output tail:
```
wrote C:\Users\07013\Desktop\0702fable\reprolab\reports\paper-003-matbench-audit.md
```

### 2026-07-03 13:50 UTC — paper003 reassemble report after wording sync

```
$ .venv\Scripts\python.exe scripts\make_matbench_report.py
```

- exit code: **0**  | duration: 0.1s  | raw log: `logs/cmd-20260703-135012-123917.log`

output tail:
```
wrote C:\Users\07013\Desktop\0702fable\reprolab\reports\paper-003-matbench-audit.md
```

### 2026-07-03 13:50 UTC — paper003 verify wording sync

```
$ .venv\Scripts\python.exe -c from pathlib import Path; import sys; summary=Path('papers/matbench/summary.md').read_text(encoding='utf-8'); packet=Path('reports/paper-003-external_release_packet.md').read_text(encoding='utf-8'); readme=Path('README.md').read_text(encoding='utf-8'); assembled=Path('reports/paper-003-matbench-audit.md').read_text(encoding='utf-8'); checks=['both were then replayed' in summary, 'Three bounded source replays now run' in packet, 'both follow-up replays are now recorded' in readme, 'both were then replayed' in assembled]; print({'checks': checks}); sys.exit(0 if all(checks) else 1)
```

- exit code: **0**  | duration: 0.1s  | raw log: `logs/cmd-20260703-135019-251623.log`

output tail:
```
{'checks': [True, True, True, True]}
```

### 2026-07-03 13:50 UTC — paper003 wording sync whitespace check

```
$ git diff --check
```

- exit code: **0**  | duration: 0.0s  | raw log: `logs/cmd-20260703-135026-241118.log`

output tail:
```
warning: in the working copy of 'README.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'papers/matbench/summary.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'reports/paper-003-external_release_packet.md', LF will be replaced by CRLF the next time Git touches it
```

### 2026-07-03 13:50 UTC — paper003 final reassemble report after wording sync

```
$ .venv\Scripts\python.exe scripts\make_matbench_report.py
```

- exit code: **0**  | duration: 0.1s  | raw log: `logs/cmd-20260703-135031-722587.log`

output tail:
```
wrote C:\Users\07013\Desktop\0702fable\reprolab\reports\paper-003-matbench-audit.md
```

