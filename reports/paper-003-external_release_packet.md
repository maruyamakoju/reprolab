# External Release Packet - Paper-003 Matbench v0.1 Audit

Date: 2026-07-03
Repo: https://github.com/maruyamakoju/reprolab
Audit target: https://github.com/materialsproject/matbench at commit
`936176db18ca4cd7b38cbd957c017a5bac770c6b`

This packet is the short handoff for maintainers, reviewers, or collaborators who
need the Matbench result without reading the full assembled report first.

## Bottom line

The checked Matbench v0.1 prediction artifacts are internally reproducible, but
the classification `rocauc` field appears to be computed after float predictions
are thresholded to labels. Three bounded source replays now run: TPOT-Mat is
executable but non-identical, RFLR is prediction-identical under scikit-learn
1.2.2, and Dummy regression folds are exact while stratified classification folds
are not because RNG state was not persisted.

- **Layer A:** RF-SCM/Magpie `matbench_v0.1_rf` fold scores reproduce exactly
  across all 13 Matbench v0.1 tasks. Scope: 65 folds, max stored-vs-recomputed
  score delta `1.776e-15`. The Dummy baseline also reproduces across all 13 tasks:
  another 65 folds, max delta `3.553e-15`.
- **All-submission scan:** all 28 local Matbench v0.1 submission artifacts were
  scanned: 180 submission-task records and 900 folds. 179/180 records match stored
  scores to numerical precision. The only exception is `matbench_v0.1_GN-OA` on
  `matbench_mp_e_form`, where MAPE differs on all five folds while MAE, RMSE, and
  max error match exactly. A simple unmasked MAPE is not the stored formula either;
  it is infinite because the target contains exact zeros.
- **Classification metric probe:** 27 classification submission-task records were
  scanned. 11 store float predictions and 16 store booleans; in all 27 records,
  stored `rocauc` equals balanced accuracy within numerical precision. For MODNet
  probability outputs, raw-probability ROC-AUC is higher by 0.030-0.122 mean AUC
  depending on task/version.
- **Leaderboard display check:** all three classification per-task leaderboard
  tables put `mean rocauc` first, and all 27 displayed rows have `mean rocauc`
  equal to mean balanced accuracy.
- **Layer B:** three bounded source paths run. TPOT-Mat runs from the submitted
  notebook artifacts but is not prediction-identical. RFLR mirrors the submitted
  regex featurizer plus `RandomForestRegressor(n_estimators=30, random_state=1)`
  and is prediction-identical under scikit-learn 1.2.2. Dummy is exact for
  checked regression folds and non-identical for stratified classification folds
  because no RNG state was persisted.
- **Source inventory:** 28 submission directories scanned; 11 have direct
  `run.py` files, 14 have notebooks, and only one has a pickle/joblib model
  artifact. This supports treating TPOT-Mat as the bounded Layer B candidate.
- **Layer B candidate triage:** after TPOT-Mat, RFLR was selected as the
  nontrivial bounded CPU replay target and Dummy as the positive-control target;
  both follow-up replays are now recorded.
- **Layer C resolution:** 180 submission-task rows produce 167 adjacent
  leaderboard pairs. 68 adjacent gaps are no larger than one fold-SE proxy, 87
  are no larger than two, and 6 are exact ties.
- **Layer C fold bootstrap:** the 25 closest adjacent pairs all have 95%
  fold-bootstrap CIs including zero; 6 of those are exact stored-score ties.

## Key numbers

| Check | Scope | Result |
|---|---:|---|
| RF all-task score recomputation | 13 tasks, 65 folds | max delta `1.776e-15` |
| Dummy all-task score recomputation | 13 tasks, 65 folds | max delta `3.553e-15` |
| All-submission score scan | 28 submissions, 900 folds | 5 MAPE-only failing folds |
| Classification records scanned | 27 submission-task records | 16 bool, 11 float, 0 mixed |
| Stored `rocauc` differing from balanced accuracy | 27 records | 0 |
| Classification leaderboard rows checked | 27 displayed rows | all `mean rocauc == mean balanced_accuracy` |
| MODNet probability-AUC gap | 4 submission/task probes | mean gap 0.029565-0.122272 |
| Source artifact inventory | 28 submission directories | 1 pickle/joblib model artifact |
| Layer B candidate triage | 28 submissions | selected `matbench_v0.1_RFLR`, now replayed exactly |
| TPOT source replay | 5 steels folds | runnable, non-identical predictions |
| RFLR source replay | 5 steels folds | max prediction delta `0.0`, max score delta `0.0` |
| Dummy source replay | 4 composition tasks, 20 folds | 10/10 regression folds exact, 0/10 classification folds exact |
| Layer C resolution map | 167 adjacent pairs | 68 <= 1 fold-SE proxy, 87 <= 2 |
| Layer C fold bootstrap | 25 closest adjacent pairs | 25/25 CIs include zero |

## Evidence map

- Full assembled report: `reports/paper-003-matbench-audit.md`
- Summary: `papers/matbench/summary.md`
- Reproduction plan: `papers/matbench/reproduction_plan.md`
- Metadata: `papers/matbench/metadata.yaml`
- Layer A reports:
  - `papers/matbench/layer_a_score_recompute.md`
  - `papers/matbench/layer_a_rf_composition_tasks.md`
  - `papers/matbench/layer_a_rf_structure_small_tasks.md`
  - `papers/matbench/layer_a_rf_structure_medium_tasks.md`
  - `papers/matbench/layer_a_rf_all_tasks.md`
  - `papers/matbench/layer_a_dummy_all_tasks.md`
  - `papers/matbench/layer_a_all_submission_score_scan.md`
  - `papers/matbench/layer_a_gn_oa_mape_probe.md`
- Classification reports:
  - `papers/matbench/classification_prediction_scan.md`
  - `papers/matbench/classification_leaderboard_metric_scan.md`
  - `papers/matbench/classification_auc_probe.md`
  - `papers/matbench/layer_a_modnet_0_1_10_probability_auc_probe.md`
  - `papers/matbench/layer_a_modnet_0_1_12_probability_auc_probe.md`
- Source artifact inventory: `papers/matbench/source_artifact_inventory.md`
- Layer B candidate triage: `papers/matbench/layer_b_candidate_triage.md`
- Layer B replay: `papers/matbench/layer_b_tpot_steels_replay.md`
- Layer B RFLR replay: `papers/matbench/layer_b_rflr_steels_replay.md`
- Layer B Dummy replay: `papers/matbench/layer_b_dummy_composition_replay.md`
- Layer C resolution map: `papers/matbench/layer_c_leaderboard_resolution.md`
- Layer C fold bootstrap: `papers/matbench/layer_c_fold_bootstrap.md`
- Classification ROC-AUC issue draft: `reports/paper-003_upstream_issue_draft.md`
- GN-OA MAPE issue draft: `reports/paper-003_gn_oa_mape_issue_draft.md`
- Command log: `papers/matbench/run_log.md`
- Core scripts:
  - `scripts/matbench_score.py`
  - `scripts/matbench_all_results_score_scan.py`
  - `scripts/matbench_classification_scan.py`
  - `scripts/matbench_leaderboard_metric_scan.py`
  - `scripts/matbench_submission_inventory.py`
  - `scripts/matbench_layer_b_candidate_triage.py`
  - `scripts/matbench_tpot_replay.py`
  - `scripts/matbench_rflr_replay.py`
  - `scripts/matbench_dummy_replay.py`
  - `scripts/matbench_leaderboard_resolution.py`
  - `scripts/matbench_leaderboard_fold_bootstrap.py`
  - `scripts/make_matbench_report.py`

## Claims to avoid

- Do not claim Matbench's stored scores are irreproducible. The checked stored
  scores reproduce exactly under the Matbench v0.1 scoring path.
- Do not claim the classification leaderboard rows are numerically wrong relative
  to stored artifacts. The issue is metric semantics: the field named `rocauc`
  behaves like thresholded-label AUC / balanced accuracy for the checked records.
- Do not claim a full model-regeneration audit. The TPOT replay is a bounded
  source-execution smoke for one small task.
- Do not claim the TPOT replay proves the submitted TPOT predictions are invalid.
  The public notebook refits stochastic estimators without a seed, so exact
  regeneration is not expected from the artifact alone.

## Suggested short wording

> I ran a ReproLab audit on Matbench v0.1. The positive result is that the checked
> local submission artifacts are almost entirely score-reproducible: 179/180
> submission-task records across 900 folds match to numerical precision. The only
> exception is a GN-OA formation-energy MAPE-only mismatch; MAE, RMSE, and max
> error match.
> The main finding is in classification scoring:
> across 27 classification submission-task records, stored `rocauc` always equals
> balanced accuracy, and for MODNet probability outputs the raw-probability ROC-AUC
> is higher by up to 0.122 mean AUC. I also ran two bounded source replays on
> `matbench_steels`: TPOT-Mat is executable but non-identical, while RFLR is
> prediction-identical under scikit-learn 1.2.2. A Dummy positive-control replay
> is exact for checked regression folds and non-identical for stratified
> classification folds because the notebook did not persist RNG state. Layer C
> then finds that 68/167 adjacent leaderboard gaps are within one fold-SE proxy,
> and the 25 closest adjacent pairs all have fold-bootstrap CIs including zero.

## Next useful moves

1. Classification `rocauc` audit evidence has been added to existing Matbench
   issue #137:
   https://github.com/materialsproject/matbench/issues/137#issuecomment-4882357351
   No duplicate issue was opened; #137 already captures the code-level concern.
2. Share the GN-OA MAPE issue separately as a follow-up, since it is a narrow
   stored-score exception rather than the classification metric behavior.
3. If maintainers confirm intended behavior, update wording/docs so classification
   leaderboards do not imply probability ROC-AUC when labels were used.
4. If deeper Layer B is needed, choose submissions with fixed seeds or saved
   fold-level model artifacts before attempting larger structure tasks.
   `matbench_v0.1_lattice_xgboost` is a possible later one-task baseline, but it
   targets the large `matbench_mp_e_form` task.
