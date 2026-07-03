# Matbench upstream issue draft - GN-OA MAPE exception

Status: draft only; not posted.

Target repo: https://github.com/materialsproject/matbench

Suggested title:

> `matbench_v0.1_GN-OA` stored MAPE for `matbench_mp_e_form` appears inconsistent with Matbench MAPE

## Draft body

Hi Matbench maintainers,

I am running an independent reproducibility audit of Matbench v0.1 leaderboard
artifacts. The broad result is positive: scanning the public `results.json.gz`
artifacts across 28 submissions, 180 submission-task records, and 900 folds, I
found that 179/180 submission-task records reproduce their stored fold scores to
numerical precision with the Matbench v0.1 scoring path.

The only score-recompute exception I found is narrow: `matbench_v0.1_GN-OA` on
`matbench_mp_e_form`, and only for MAPE. The same predictions and official split
IDs reproduce MAE, RMSE, and max error exactly or to floating-point precision, so
this does not look like a prediction-ID alignment problem.

### Observation

Using the Matbench v0.1 MAPE path, which masks targets with
`abs(y_true) > 1e-5`, the stored and recomputed values differ on all five folds:

| Fold | Stored MAPE | Recomputed Matbench MAPE | Delta | Other regression metrics |
|---:|---:|---:|---:|---|
| 0 | 12.5887409438 | 0.420116236715 | 12.1686247071 | match |
| 1 | 7.94659210396 | 0.137819988807 | 7.80877211515 | match |
| 2 | 9.26331433818 | 0.149750183903 | 9.11356415428 | match |
| 3 | 11.8881843898 | 0.236287007689 | 11.6518973821 | match |
| 4 | 12.1946455981 | 0.201616727224 | 11.9930288708 | match |

### Checks that did not explain the stored values

- Recomputing MAE, RMSE, and max error from the same fold predictions matches the
  stored values, which supports the official validation IDs being aligned.
- A simple unmasked MAPE is not the stored formula either. It is infinite on all
  five folds because the `matbench_mp_e_form` test targets contain exact zeros.
- Sweeping small denominator thresholds did not reproduce the stored MAPE values.

### Suggested handling

Could you confirm whether the stored GN-OA MAPE values for `matbench_mp_e_form`
were computed with a submission-specific formula, or whether this is a historical
stored-score inconsistency that should be corrected or annotated?

I have not opened a PR because the right treatment of historical leaderboard
artifacts is a maintainer policy decision. The issue is intentionally scoped to
this one submission/task/metric exception.

Thanks for maintaining the benchmark.

## Local evidence files

- `papers/matbench/layer_a_all_submission_score_scan.md`
- `papers/matbench/layer_a_gn_oa_mape_probe.md`
- `scripts/matbench_all_results_score_scan.py`
- `scripts/matbench_score.py`

## Guardrails

- Do not post until the user explicitly asks.
- If posting, link the public ReproLab commit containing the scripts/reports.
- Keep this issue separate from the classification `rocauc` draft unless the user
  explicitly asks to combine them.
