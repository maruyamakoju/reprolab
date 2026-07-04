I ran an independent ReproLab audit of the Matbench v0.1 leaderboard artifacts and
can add artifact-level evidence for this issue.

The short version: the code-level concern in this issue appears to show up in the
published v0.1 artifacts. The stored `rocauc` values I checked behave as
thresholded-label AUC / balanced accuracy rather than probability-score ROC-AUC.

Audit scope:

- 27 classification submission-task records scanned from public Matbench v0.1
  `results.json.gz` artifacts.
- 16 records store hard bool predictions.
- 11 records store float predictions.
- In all 27 records, stored `rocauc` equals stored balanced accuracy within
  numerical precision.
- The generated classification per-task leaderboard tables display `mean rocauc`
  as the first metric column, and all 27 displayed rows have
  `mean rocauc == mean balanced_accuracy`.

For two small MODNet classification tasks, I reproduced the stored fold scores and
also computed ROC-AUC from the raw float predictions:

| submission | task | stored rocauc mean | raw-probability rocauc mean | mean gap |
|---|---|---:|---:|---:|
| `matbench_v0.1_modnet_v0.1.10` | `matbench_expt_is_metal` | 0.916052 | 0.972546 | 0.056495 |
| `matbench_v0.1_modnet_v0.1.10` | `matbench_glass` | 0.810676 | 0.932948 | 0.122272 |
| `matbench_v0.1_modnet_v0.1.12` | `matbench_expt_is_metal` | 0.916052 | 0.972546 | 0.056495 |
| `matbench_v0.1_modnet_v0.1.12` | `matbench_glass` | 0.960311 | 0.989876 | 0.029565 |

So the historical artifacts are internally reproducible, but the field named
`rocauc` appears to be interpreted/displayed as the primary classification metric
even when it equals thresholded-label AUC. My read is that the main action is a
maintainer policy decision:

1. document that Matbench v0.1 classification `rocauc` is thresholded-label AUC for
   affected float-prediction submissions,
2. fix the scoring path for future submissions and note the historical behavior,
   or
3. point to a different code path if this audit is missing something.

Evidence:

- ReproLab repo: https://github.com/maruyamakoju/reprolab
- Full Matbench audit: https://github.com/maruyamakoju/reprolab/blob/master/reports/paper-003-matbench-audit.md
- External packet: https://github.com/maruyamakoju/reprolab/blob/master/reports/paper-003-external_release_packet.md
- Classification AUC probe: https://github.com/maruyamakoju/reprolab/blob/master/papers/matbench/classification_auc_probe.md
- Prediction scan: https://github.com/maruyamakoju/reprolab/blob/master/papers/matbench/classification_prediction_scan.md
- Leaderboard metric scan: https://github.com/maruyamakoju/reprolab/blob/master/papers/matbench/classification_leaderboard_metric_scan.md
