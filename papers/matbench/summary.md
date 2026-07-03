# Summary - Matbench v0.1 Paper-003 Candidate

Status: candidate selected; Layer A seed passed.

## Result

The first audit slice recomputed stored Matbench v0.1 fold scores from public
prediction artifacts rather than rerunning a model. For the RF-SCM/Magpie baseline
(`matbench_v0.1_rf`), `scripts/matbench_score.py` checked two tasks:

| task | type | folds | max score delta |
|---|---|---:|---:|
| `matbench_steels` | regression | 5 | 0 |
| `matbench_expt_is_metal` | classification | 5 | 1.110e-16 |

Across all 10 checked folds, the max absolute stored-vs-recomputed score delta is
`1.1102230246251565e-16`.

Report: `layer_a_score_recompute.md`.

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

- Plan: `reproduction_plan.md`
- Candidate screen: `candidate_screen.md`
- Metadata: `metadata.yaml`
- Layer A seed report: `layer_a_score_recompute.md`
- Classification AUC probe: `classification_auc_probe.md`
- Classification prediction scan: `classification_prediction_scan.md`
- Classification leaderboard metric scan: `classification_leaderboard_metric_scan.md`
- Upstream issue draft: `../../reports/paper-003_upstream_issue_draft.md`
- Script: `../../scripts/matbench_score.py`
- Classification scan script: `../../scripts/matbench_classification_scan.py`
- Leaderboard metric scan script: `../../scripts/matbench_leaderboard_metric_scan.py`
- Run log: `run_log.md`
