# Matbench v0.1 score recomputation

- Results artifact: `vendor/matbench/benchmarks/matbench_v0.1_modnet_v0.1.10/results.json.gz`
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
| matbench_glass | 0 | 1136 | float | 1.110e-16 | 0.826222302573 | 0.945985544419 |
| matbench_glass | 1 | 1136 | float | 0.000e+00 | 0.778326421924 | 0.922528182356 |
| matbench_glass | 2 | 1136 | float | 0.000e+00 | 0.806290324403 | 0.919718421261 |
| matbench_glass | 3 | 1136 | float | 0.000e+00 | 0.840239093344 | 0.935586415219 |
| matbench_glass | 4 | 1136 | float | 0.000e+00 | 0.802303552126 | 0.940923454726 |

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
| accuracy | 0.867605633803 | 0.885563380282 | 0.853873239437 | 0.01187042805 |
| balanced_accuracy | 0.810676338874 | 0.840239093344 | 0.778326421924 | 0.0212202320756 |
| f1 | 0.910366876186 | 0.921686746988 | 0.901629450815 | 0.00751972277715 |
| rocauc | 0.810676338874 | 0.840239093344 | 0.778326421924 | 0.0212202320756 |
