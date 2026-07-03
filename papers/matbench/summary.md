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
accuracy. The next useful audit question is whether other submissions store
probabilities and, if so, whether the Matbench v0.1 scoring order materially affects
the recorded ROC-AUC.

## Artifacts

- Plan: `reproduction_plan.md`
- Candidate screen: `candidate_screen.md`
- Metadata: `metadata.yaml`
- Layer A seed report: `layer_a_score_recompute.md`
- Script: `../../scripts/matbench_score.py`
- Run log: `run_log.md`
