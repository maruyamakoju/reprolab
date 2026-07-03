# Matbench v0.1 GN-OA MAPE exception probe

The all-submission score scan found one score-recompute exception:
`matbench_v0.1_GN-OA` on `matbench_mp_e_form`. This probe checks whether the
exception affects all regression metrics or only MAPE.

## Result

MAE, RMSE, and max error match the stored fold scores exactly or to floating-point
precision. The mismatch is isolated to MAPE.

| Fold | Stored MAPE | Recomputed Matbench MAPE | Delta | Other regression metrics |
|---:|---:|---:|---:|---|
| 0 | 12.5887409438 | 0.420116236715 | 12.1686247071 | match |
| 1 | 7.94659210396 | 0.137819988807 | 7.80877211515 | match |
| 2 | 9.26331433818 | 0.149750183903 | 9.11356415428 | match |
| 3 | 11.8881843898 | 0.236287007689 | 11.6518973821 | match |
| 4 | 12.1946455981 | 0.201616727224 | 11.9930288708 | match |

## Formula checks

The Matbench v0.1 MAPE path masks target values with `abs(y_true) > 1e-5`. Using
that formula gives the recomputed values above.

A simple unmasked MAPE is not the stored formula either: it becomes infinite on
all five folds because the `matbench_mp_e_form` test targets contain exact zeros.

Threshold sweeps over small denominators also did not reproduce the stored values.
This points to a submission-specific stored-MAPE inconsistency rather than an ID
alignment problem or a general scoring-path issue.

## Interpretation

The published GN-OA predictions appear aligned with the official validation IDs:
MAE, RMSE, and max error all match. The exception should be treated narrowly as a
stored MAPE inconsistency for `matbench_v0.1_GN-OA` / `matbench_mp_e_form`.
