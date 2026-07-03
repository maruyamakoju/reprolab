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
are thresholded to labels. A bounded TPOT source replay also shows that at least
one public notebook path can run end-to-end, but does not regenerate its committed
predictions exactly because the notebook refits stochastic estimators without a
submitted random seed.

- **Layer A:** RF-SCM/Magpie `matbench_v0.1_rf` fold scores reproduce exactly
  across all 13 Matbench v0.1 tasks. Scope: 65 folds, max stored-vs-recomputed
  score delta `1.776e-15`.
- **Classification metric probe:** 27 classification submission-task records were
  scanned. 11 store float predictions and 16 store booleans; in all 27 records,
  stored `rocauc` equals balanced accuracy within numerical precision. For MODNet
  probability outputs, raw-probability ROC-AUC is higher by 0.030-0.122 mean AUC
  depending on task/version.
- **Leaderboard display check:** all three classification per-task leaderboard
  tables put `mean rocauc` first, and all 27 displayed rows have `mean rocauc`
  equal to mean balanced accuracy.
- **Layer B:** TPOT-Mat `matbench_steels` source replay runs from the submitted
  notebook artifacts in a pinned TPOT/sklearn environment. It is not
  prediction-identical: with audit seed 0, replay mean MAE is 79.094 vs submitted
  mean MAE 79.947.
- **Source inventory:** 28 submission directories scanned; 11 have direct
  `run.py` files, 14 have notebooks, and only one has a pickle/joblib model
  artifact. This supports treating TPOT-Mat as the bounded Layer B candidate.

## Key numbers

| Check | Scope | Result |
|---|---:|---|
| RF all-task score recomputation | 13 tasks, 65 folds | max delta `1.776e-15` |
| Classification records scanned | 27 submission-task records | 16 bool, 11 float, 0 mixed |
| Stored `rocauc` differing from balanced accuracy | 27 records | 0 |
| Classification leaderboard rows checked | 27 displayed rows | all `mean rocauc == mean balanced_accuracy` |
| MODNet probability-AUC gap | 4 submission/task probes | mean gap 0.029565-0.122272 |
| Source artifact inventory | 28 submission directories | 1 pickle/joblib model artifact |
| TPOT source replay | 5 steels folds | runnable, non-identical predictions |

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
- Classification reports:
  - `papers/matbench/classification_prediction_scan.md`
  - `papers/matbench/classification_leaderboard_metric_scan.md`
  - `papers/matbench/classification_auc_probe.md`
  - `papers/matbench/layer_a_modnet_0_1_10_probability_auc_probe.md`
  - `papers/matbench/layer_a_modnet_0_1_12_probability_auc_probe.md`
- Source artifact inventory: `papers/matbench/source_artifact_inventory.md`
- Layer B replay: `papers/matbench/layer_b_tpot_steels_replay.md`
- Upstream issue draft: `reports/paper-003_upstream_issue_draft.md`
- Command log: `papers/matbench/run_log.md`
- Core scripts:
  - `scripts/matbench_score.py`
  - `scripts/matbench_classification_scan.py`
  - `scripts/matbench_leaderboard_metric_scan.py`
  - `scripts/matbench_submission_inventory.py`
  - `scripts/matbench_tpot_replay.py`
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
> RF baseline prediction artifacts reproduce their stored fold scores exactly on
> all 13 tasks / 65 folds.
> The main finding is in classification scoring:
> across 27 classification submission-task records, stored `rocauc` always equals
> balanced accuracy, and for MODNet probability outputs the raw-probability ROC-AUC
> is higher by up to 0.122 mean AUC. I also ran a bounded TPOT-Mat source replay:
> the notebook path is executable, but it does not regenerate committed predictions
> exactly because it refits stochastic estimators without a submitted seed.

## Next useful moves

1. Share the classification `rocauc` issue draft with Matbench maintainers after
   user approval.
2. If maintainers confirm intended behavior, update wording/docs so classification
   leaderboards do not imply probability ROC-AUC when labels were used.
3. If deeper Layer B is needed, choose submissions with fixed seeds or saved
   fold-level model artifacts before attempting larger structure tasks.
