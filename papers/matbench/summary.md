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
28 submissions for the next bounded source replay. It identifies
`matbench_v0.1_RFLR` as the best next nontrivial CPU target: one
`matbench_steels` task, simple scikit-learn/numpy/matbench requirements, notebook
source, and seed/fit/predict signals. `matbench_v0.1_dummy` is the best
positive-control candidate if an exact low-novelty source replay is needed.

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
