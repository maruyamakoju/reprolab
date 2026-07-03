# ReproLab Paper-003 - Matbench v0.1 Audit

_Generated: 2026-07-03 08:00 UTC_

> Auto-assembled from tracked artifacts by `scripts/make_matbench_report.py`.

## 0. Executive summary

# Summary - Matbench v0.1 Paper-003 Candidate

Status: candidate selected; Layer A RF composition-task check passed; bounded Layer B TPOT source replay completed.

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

## Layer B source replay

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
- Classification AUC probe: `classification_auc_probe.md`
- Classification prediction scan: `classification_prediction_scan.md`
- Classification leaderboard metric scan: `classification_leaderboard_metric_scan.md`
- Layer B TPOT steels replay: `layer_b_tpot_steels_replay.md`
- Upstream issue draft: `../../reports/paper-003_upstream_issue_draft.md`
- Script: `../../scripts/matbench_score.py`
- Layer B replay script: `../../scripts/matbench_tpot_replay.py`
- Classification scan script: `../../scripts/matbench_classification_scan.py`
- Leaderboard metric scan script: `../../scripts/matbench_leaderboard_metric_scan.py`
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



## 6. Layer B TPOT steels source replay

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



## 7. Upstream issue draft

# Matbench upstream issue draft - classification ROC-AUC scoring

Status: draft only; not posted.

Target repo: https://github.com/materialsproject/matbench

Suggested title:

> Classification `rocauc` appears to be computed after float predictions are thresholded

## Draft body

Hi Matbench maintainers,

I am running an independent reproducibility audit of Matbench v0.1 leaderboard
artifacts. First, the positive result: the stored fold scores I checked are
internally reproducible from the released `results.json.gz` files, official split
IDs, and Matminer targets.

While checking classification submissions, I found what looks like an unintended
ROC-AUC scoring behavior for submissions that record float predictions.

### Observation

In the current scoring code, classification metrics are ordered as:

```python
CLF_METRICS = ["accuracy", "balanced_accuracy", "f1", "rocauc"]
```

In `matbench.data_ops.score_array`, non-ROC classification metrics convert float
predictions to thresholded labels by reassigning the local `pred_array` variable.
Because `accuracy` is evaluated before `rocauc`, a later `rocauc` call receives the
already-thresholded labels rather than the original float scores.

That means the stored `rocauc` field can behave as thresholded-label AUC, which is
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

The key point is that the local prediction variable is reused across metrics. A
minimal fix would be to keep a copy of the original prediction array for ROC-AUC,
or compute ROC-AUC from a separate unthresholded variable when the submitted values
are floats.

Conceptually:

```python
raw_pred_array = pred_array
...
if metric == "rocauc" and isinstance(raw_pred_array[0], float):
    computed[metric] = roc_auc_score(homogenized_true_array, raw_pred_array)
```

### Suggested handling

I see two possible paths:

1. Fix the scoring code for future submissions and add a release note that historic
   Matbench v0.1 classification `rocauc` values were computed from thresholded
   labels when float predictions were submitted.
2. If the thresholded behavior is intended for Matbench v0.1 historical stability,
   document that `rocauc` in those artifacts is thresholded-label AUC rather than
   probability-score ROC-AUC.

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

## Guardrails

- Do not post until the user explicitly asks.
- If posting, link the public ReproLab commit containing the scripts/reports.
- Keep the issue scoped to classification `rocauc`; do not bundle unrelated
  Matbench v0.1 audit notes.



## 8. Run log (tail)

  warnings.warn(
```

### 2026-07-03 07:54 UTC — paper003 compile seeded TPOT replay script

```
$ .venv\Scripts\python.exe -m py_compile scripts\matbench_tpot_replay.py
```

- exit code: **0**  | duration: 0.1s  | raw log: `logs/cmd-20260703-075455-609148.log`

output tail:
```

```

### 2026-07-03 07:55 UTC — paper003 replay TPOT steels all folds seeded

```
$ env\matbench-tpot\Scripts\python.exe scripts\matbench_tpot_replay.py --report papers\matbench\layer_b_tpot_steels_replay.md --seed 0
```

- exit code: **0**  | duration: 1.9s  | raw log: `logs/cmd-20260703-075500-370249.log`

output tail:
```
If you wish to scale the data, use Pipeline with a StandardScaler in a preprocessing stage. To reproduce the previous behavior:

from sklearn.pipeline import make_pipeline

model = make_pipeline(StandardScaler(with_mean=False), LassoLarsCV())

If you wish to pass a sample_weight parameter, you need to pass it as a fit parameter to each step of the pipeline as follows:

kwargs = {s[0] + '__sample_weight': sample_weight for s in model.steps}
model.fit(X, y, **kwargs)

Set parameter alpha to: original_alpha * np.sqrt(n_samples).
  warnings.warn(
C:\Users\07013\Desktop\0702fable\reprolab\env\matbench-tpot\Lib\site-packages\sklearn\svm\_base.py:1244: ConvergenceWarning: Liblinear failed to converge, increase the number of iterations.
  warnings.warn(
```

### 2026-07-03 07:57 UTC — paper003 verify TPOT replay docs

```
$ .venv\Scripts\python.exe -c from pathlib import Path; import py_compile, sys, yaml; py_compile.compile('scripts/matbench_tpot_replay.py', doraise=True); meta=yaml.safe_load(Path('papers/matbench/metadata.yaml').read_text(encoding='utf-8')); summary=Path('papers/matbench/summary.md').read_text(encoding='utf-8'); plan=Path('papers/matbench/reproduction_plan.md').read_text(encoding='utf-8'); readme=Path('README.md').read_text(encoding='utf-8'); report=Path('papers/matbench/layer_b_tpot_steels_replay.md').read_text(encoding='utf-8'); checks=[meta['layer_b_tpot_steels']['folds_replayed']==5, abs(meta['layer_b_tpot_steels']['replay_mae_mean']-79.09383529924)<1e-9, 'Layer B source replay' in summary, 'matbench_tpot_replay.py' in plan, 'seed-0 replay mean MAE 79.094' in readme, 'Audit random seed:
```

- exit code: **1**  | duration: 0.1s  | raw log: `logs/cmd-20260703-075724-036491.log`

output tail:
```
  File "<string>", line 1
    from pathlib import Path; import py_compile, sys, yaml; py_compile.compile('scripts/matbench_tpot_replay.py', doraise=True); meta=yaml.safe_load(Path('papers/matbench/metadata.yaml').read_text(encoding='utf-8')); summary=Path('papers/matbench/summary.md').read_text(encoding='utf-8'); plan=Path('papers/matbench/reproduction_plan.md').read_text(encoding='utf-8'); readme=Path('README.md').read_text(encoding='utf-8'); report=Path('papers/matbench/layer_b_tpot_steels_replay.md').read_text(encoding='utf-8'); checks=[meta['layer_b_tpot_steels']['folds_replayed']==5, abs(meta['layer_b_tpot_steels']['replay_mae_mean']-79.09383529924)<1e-9, 'Layer B source replay' in summary, 'matbench_tpot_replay.py' in plan, 'seed-0 replay mean MAE 79.094' in readme, 'Audit random seed:
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     ^
SyntaxError: unterminated string literal (detected at line 1)
```

### 2026-07-03 07:57 UTC — paper003 verify TPOT replay docs rerun

```
$ .venv\Scripts\python.exe -c from pathlib import Path; import py_compile, sys, yaml; py_compile.compile('scripts/matbench_tpot_replay.py', doraise=True); meta=yaml.safe_load(Path('papers/matbench/metadata.yaml').read_text(encoding='utf-8')); summary=Path('papers/matbench/summary.md').read_text(encoding='utf-8'); plan=Path('papers/matbench/reproduction_plan.md').read_text(encoding='utf-8'); readme=Path('README.md').read_text(encoding='utf-8'); report=Path('papers/matbench/layer_b_tpot_steels_replay.md').read_text(encoding='utf-8'); checks=[meta['layer_b_tpot_steels']['folds_replayed']==5, abs(meta['layer_b_tpot_steels']['replay_mae_mean']-79.09383529924)<1e-9, 'Layer B source replay' in summary, 'matbench_tpot_replay.py' in plan, 'seed-0 replay mean MAE 79.094' in readme, 'Audit random seed' in report]; print({'checks': checks}); sys.exit(0 if all(checks) else 1)
```

- exit code: **0**  | duration: 0.1s  | raw log: `logs/cmd-20260703-075739-651817.log`

output tail:
```
{'checks': [True, True, True, True, True, True]}
```

### 2026-07-03 07:57 UTC — paper003 TPOT replay git diff whitespace check

```
$ git diff --check
```

- exit code: **2**  | duration: 0.0s  | raw log: `logs/cmd-20260703-075744-886128.log`

output tail:
```
papers/matbench/run_log.md:1087: trailing whitespace.
+Set parameter alpha to: original_alpha * np.sqrt(n_samples).
papers/matbench/run_log.md:1127: trailing whitespace.
+Set parameter alpha to: original_alpha * np.sqrt(n_samples).
papers/matbench/run_log.md:1136: trailing whitespace.
+$ .venv\Scripts\python.exe -c from pathlib import Path; import py_compile, sys, yaml; py_compile.compile('scripts/matbench_tpot_replay.py', doraise=True); meta=yaml.safe_load(Path('papers/matbench/metadata.yaml').read_text(encoding='utf-8')); summary=Path('papers/matbench/summary.md').read_text(encoding='utf-8'); plan=Path('papers/matbench/reproduction_plan.md').read_text(encoding='utf-8'); readme=Path('README.md').read_text(encoding='utf-8'); report=Path('papers/matbench/layer_b_tpot_steels_replay.md').read_text(encoding='utf-8'); checks=[meta['layer_b_tpot_steels']['folds_replayed']==5, abs(meta['layer_b_tpot_steels']['replay_mae_mean']-79.09383529924)<1e-9, 'Layer B source replay' in summary, 'matbench_tpot_replay.py' in plan, 'seed-0 replay mean MAE 79.094' in readme, 'Audit random seed:
papers/matbench/run_log.md:1144: trailing whitespace.
+    from pathlib import Path; import py_compile, sys, yaml; py_compile.compile('scripts/matbench_tpot_replay.py', doraise=True); meta=yaml.safe_load(Path('papers/matbench/metadata.yaml').read_text(encoding='utf-8')); summary=Path('papers/matbench/summary.md').read_text(encoding='utf-8'); plan=Path('papers/matbench/reproduction_plan.md').read_text(encoding='utf-8'); readme=Path('README.md').read_text(encoding='utf-8'); report=Path('papers/matbench/layer_b_tpot_steels_replay.md').read_text(encoding='utf-8'); checks=[meta['layer_b_tpot_steels']['folds_replayed']==5, abs(meta['layer_b_tpot_steels']['replay_mae_mean']-79.09383529924)<1e-9, 'Layer B source replay' in summary, 'matbench_tpot_replay.py' in plan, 'seed-0 replay mean MAE 79.094' in readme, 'Audit random seed:
warning: in the working copy of 'README.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'papers/matbench/candidate_screen.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'papers/matbench/metadata.yaml', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'papers/matbench/reproduction_plan.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'papers/matbench/run_log.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'papers/matbench/summary.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'reports/one_page_summary.md', LF will be replaced by CRLF the next time Git touches it
```

### 2026-07-03 07:58 UTC — paper003 TPOT replay git diff whitespace check rerun

```
$ git diff --check
```

- exit code: **0**  | duration: 0.0s  | raw log: `logs/cmd-20260703-075808-299482.log`

output tail:
```
warning: in the working copy of 'README.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'papers/matbench/candidate_screen.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'papers/matbench/metadata.yaml', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'papers/matbench/reproduction_plan.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'papers/matbench/summary.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'reports/one_page_summary.md', LF will be replaced by CRLF the next time Git touches it
```

### 2026-07-03 07:58 UTC — paper003 verify TPOT replay docs final

```
$ .venv\Scripts\python.exe -c from pathlib import Path; import py_compile, sys, yaml; py_compile.compile('scripts/matbench_tpot_replay.py', doraise=True); meta=yaml.safe_load(Path('papers/matbench/metadata.yaml').read_text(encoding='utf-8')); summary=Path('papers/matbench/summary.md').read_text(encoding='utf-8'); plan=Path('papers/matbench/reproduction_plan.md').read_text(encoding='utf-8'); readme=Path('README.md').read_text(encoding='utf-8'); report=Path('papers/matbench/layer_b_tpot_steels_replay.md').read_text(encoding='utf-8'); checks=[meta['layer_b_tpot_steels']['folds_replayed']==5, abs(meta['layer_b_tpot_steels']['replay_mae_mean']-79.09383529924)<1e-9, 'Layer B source replay' in summary, 'env/matbench-tpot/Scripts/python.exe -m pip install' in plan, 'seed-0 replay mean MAE 79.094' in readme, 'Audit random seed' in report]; print({'checks': checks}); sys.exit(0 if all(checks) else 1)
```

- exit code: **0**  | duration: 0.1s  | raw log: `logs/cmd-20260703-075841-802043.log`

output tail:
```
{'checks': [True, True, True, True, True, True]}
```

### 2026-07-03 07:58 UTC — paper003 TPOT replay final whitespace check

```
$ git diff --check
```

- exit code: **0**  | duration: 0.1s  | raw log: `logs/cmd-20260703-075846-206235.log`

output tail:
```
warning: in the working copy of 'README.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'papers/matbench/candidate_screen.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'papers/matbench/metadata.yaml', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'papers/matbench/reproduction_plan.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'papers/matbench/summary.md', LF will be replaced by CRLF the next time Git touches it
warning: in the working copy of 'reports/one_page_summary.md', LF will be replaced by CRLF the next time Git touches it
```

### 2026-07-03 08:00 UTC — paper003 assemble Matbench audit report

```
$ .venv\Scripts\python.exe scripts\make_matbench_report.py
```

- exit code: **0**  | duration: 0.1s  | raw log: `logs/cmd-20260703-080015-463513.log`

output tail:
```
wrote C:\Users\07013\Desktop\0702fable\reprolab\reports\paper-003-matbench-audit.md
```

