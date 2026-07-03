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

The next step is to check whether any public leaderboard view ranks classification
tasks by the stored `rocauc` field, and to decide whether this should become an
upstream issue or a report note.
