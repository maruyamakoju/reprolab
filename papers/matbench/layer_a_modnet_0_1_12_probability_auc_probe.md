# Matbench v0.1 score recomputation

- Results artifact: `vendor/matbench/benchmarks/matbench_v0.1_modnet_v0.1.12/results.json.gz`
- Fold scores checked: 10
- Max absolute stored-vs-recomputed score delta: 1.110e-16

## Fold checks

| Task | Fold | n | Prediction type | Max score delta | Stored rocauc | Probability rocauc |
|---|---:|---:|---|---:|---:|---:|
| matbench_expt_is_metal | 0 | 985 | float | 1.110e-16 | 0.926853401717 | 0.976227973977 |
| matbench_expt_is_metal | 1 | 984 | float | 1.110e-16 | 0.913562753036 | 0.971321160043 |
| matbench_expt_is_metal | 2 | 984 | float | 1.110e-16 | 0.917677435347 | 0.974634388168 |
| matbench_expt_is_metal | 3 | 984 | float | 1.110e-16 | 0.917660910518 | 0.975113608196 |
| matbench_expt_is_metal | 4 | 984 | float | 1.110e-16 | 0.904503015781 | 0.96543418987 |
| matbench_glass | 0 | 1136 | float | 0.000e+00 | 0.974327973695 | 0.995194027939 |
| matbench_glass | 1 | 1136 | float | 1.110e-16 | 0.961830939763 | 0.992173346441 |
| matbench_glass | 2 | 1136 | float | 0.000e+00 | 0.953893176348 | 0.986570773212 |
| matbench_glass | 3 | 1136 | float | 1.110e-16 | 0.95445437528 | 0.987841945289 |
| matbench_glass | 4 | 1136 | float | 0.000e+00 | 0.957049449535 | 0.987600893399 |

## Recomputed fold aggregates

### matbench_expt_is_metal

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| accuracy | 0.91607176757 | 0.926903553299 | 0.904471544715 | 0.0072540465199 |
| balanced_accuracy | 0.91605150328 | 0.926853401717 | 0.904503015781 | 0.00723154613987 |
| f1 | 0.915321800781 | 0.925465838509 | 0.904858299595 | 0.00676906894697 |
| rocauc | 0.91605150328 | 0.926853401717 | 0.904503015781 | 0.00723154613987 |

### matbench_glass

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| accuracy | 0.969190140845 | 0.978873239437 | 0.962147887324 | 0.00591821701196 |
| balanced_accuracy | 0.960311182924 | 0.974327973695 | 0.953893176348 | 0.00754866866747 |
| f1 | 0.978380170771 | 0.985130111524 | 0.973341599504 | 0.00417043559708 |
| rocauc | 0.960311182924 | 0.974327973695 | 0.953893176348 | 0.00754866866747 |
