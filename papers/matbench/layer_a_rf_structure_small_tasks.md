# Matbench v0.1 score recomputation

- Results artifact: `vendor/matbench/benchmarks/matbench_v0.1_rf/results.json.gz`
- Fold scores checked: 10
- Max absolute stored-vs-recomputed score delta: 0.000e+00

## Fold checks

| Task | Fold | n | Prediction type | Max score delta | Stored rocauc | Probability rocauc |
|---|---:|---:|---|---:|---:|---:|
| matbench_jdft2d | 0 | 128 | float | 0.000e+00 |  |  |
| matbench_jdft2d | 1 | 127 | float | 0.000e+00 |  |  |
| matbench_jdft2d | 2 | 127 | float | 0.000e+00 |  |  |
| matbench_jdft2d | 3 | 127 | float | 0.000e+00 |  |  |
| matbench_jdft2d | 4 | 127 | float | 0.000e+00 |  |  |
| matbench_phonons | 0 | 253 | float | 0.000e+00 |  |  |
| matbench_phonons | 1 | 253 | float | 0.000e+00 |  |  |
| matbench_phonons | 2 | 253 | float | 0.000e+00 |  |  |
| matbench_phonons | 3 | 253 | float | 0.000e+00 |  |  |
| matbench_phonons | 4 | 253 | float | 0.000e+00 |  |  |

## Recomputed fold aggregates

### matbench_jdft2d

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| mae | 50.04399974 | 66.2421301222 | 42.7472945267 | 8.62712887611 |
| rmse | 112.265975486 | 159.638986052 | 72.7391490957 | 36.7066225573 |
| mape | 5.23911546788 | 23.7624894676 | 0.43823538542 | 9.26294774418 |
| max_error | 718.045733692 | 1538.60726856 | 295.743678511 | 453.647322018 |

### matbench_phonons

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| mae | 67.6126142422 | 82.3862649649 | 58.6036107598 | 8.9899908374 |
| rmse | 146.276431864 | 172.801458959 | 122.15658115 | 21.4751689658 |
| mape | 0.118485135116 | 0.134769893668 | 0.104049045388 | 0.00979558791325 |
| max_error | 1270.68885897 | 2024.7301119 | 861.90049904 | 402.730658047 |
