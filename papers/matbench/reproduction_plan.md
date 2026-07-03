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
