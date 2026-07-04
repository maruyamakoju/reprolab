# Matbench upstream issue draft - classification ROC-AUC scoring

Status: posted as a comment on existing upstream issue #137:
https://github.com/materialsproject/matbench/issues/137#issuecomment-4882357351

This new-issue draft is kept as an archive. Existing upstream issue #137 already
covers the code-level `rocauc` concern, so the audit evidence was posted there
using `reports/paper-003_rocauc_issue_137_comment.md`.

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

- Do not open this as a new issue unless maintainers ask for a fresh one.
- Prefer commenting on existing issue #137 with the audit evidence.
- If posting, link the public ReproLab commit containing the scripts/reports.
- Keep the issue scoped to classification `rocauc`; do not bundle unrelated
  Matbench v0.1 audit notes.
- Post this classification issue before the narrower GN-OA MAPE issue.
