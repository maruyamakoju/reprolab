# Matbench v0.1 score recomputation

- Results artifact: `vendor/matbench/benchmarks/matbench_v0.1_rf/results.json.gz`
- Fold scores checked: 20
- Max absolute stored-vs-recomputed score delta: 1.110e-16

## Fold checks

| Task | Fold | n | Prediction type | Max score delta | Stored rocauc | Probability rocauc |
|---|---:|---:|---|---:|---:|---:|
| matbench_expt_gap | 0 | 921 | float | 0.000e+00 |  |  |
| matbench_expt_gap | 1 | 921 | float | 0.000e+00 |  |  |
| matbench_expt_gap | 2 | 921 | float | 0.000e+00 |  |  |
| matbench_expt_gap | 3 | 921 | float | 0.000e+00 |  |  |
| matbench_expt_gap | 4 | 920 | float | 0.000e+00 |  |  |
| matbench_expt_is_metal | 0 | 985 | bool | 0.000e+00 | 0.924829110219 |  |
| matbench_expt_is_metal | 1 | 984 | bool | 0.000e+00 | 0.916632239941 |  |
| matbench_expt_is_metal | 2 | 984 | bool | 1.110e-16 | 0.909481120383 |  |
| matbench_expt_is_metal | 3 | 984 | bool | 1.110e-16 | 0.922746426506 |  |
| matbench_expt_is_metal | 4 | 984 | bool | 1.110e-16 | 0.909605056598 |  |
| matbench_glass | 0 | 1136 | bool | 0.000e+00 | 0.886006937775 |  |
| matbench_glass | 1 | 1136 | bool | 0.000e+00 | 0.840239093344 |  |
| matbench_glass | 2 | 1136 | bool | 1.110e-16 | 0.849521474334 |  |
| matbench_glass | 3 | 1136 | bool | 1.110e-16 | 0.852619367766 |  |
| matbench_glass | 4 | 1136 | bool | 0.000e+00 | 0.865116401698 |  |
| matbench_steels | 0 | 63 | float | 0.000e+00 |  |  |
| matbench_steels | 1 | 63 | float | 0.000e+00 |  |  |
| matbench_steels | 2 | 62 | float | 0.000e+00 |  |  |
| matbench_steels | 3 | 62 | float | 0.000e+00 |  |  |
| matbench_steels | 4 | 62 | float | 0.000e+00 |  |  |

## Recomputed fold aggregates

### matbench_expt_gap

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| mae | 0.446054992487 | 0.481156868621 | 0.434542420557 | 0.0176552424643 |
| rmse | 0.824300735345 | 0.943523224093 | 0.781867354239 | 0.0601326123053 |
| mape | 0.369492377556 | 0.43851001849 | 0.304356979438 | 0.0470475962382 |
| max_error | 6.046496 | 9.5428 | 4.71216 | 1.76997564717 |

### matbench_expt_is_metal

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| accuracy | 0.916681936363 | 0.924873096447 | 0.909552845528 | 0.00641463134 |
| balanced_accuracy | 0.916658790729 | 0.924829110219 | 0.909481120383 | 0.00640450234832 |
| f1 | 0.915855162513 | 0.923553719008 | 0.907580477674 | 0.00628063358071 |
| rocauc | 0.916658790729 | 0.924829110219 | 0.909481120383 | 0.00640450234832 |

### matbench_glass

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| accuracy | 0.895422535211 | 0.919894366197 | 0.884683098592 | 0.0130969823334 |
| balanced_accuracy | 0.858700654983 | 0.886006937775 | 0.840239093344 | 0.0158041991609 |
| f1 | 0.927798088561 | 0.944881889764 | 0.919975565058 | 0.00908698827732 |
| rocauc | 0.858700654983 | 0.886006937775 | 0.840239093344 | 0.0158041991609 |

### matbench_steels

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| mae | 103.512486062 | 114.63311746 | 85.6694031746 | 11.0367786926 |
| rmse | 149.383944441 | 196.358570629 | 113.154922817 | 27.4893431478 |
| mape | 0.0744721297401 | 0.0807437889227 | 0.0653807405884 | 0.0056047478171 |
| max_error | 594.98156 | 1121.1276 | 362.663 | 278.700159881 |
