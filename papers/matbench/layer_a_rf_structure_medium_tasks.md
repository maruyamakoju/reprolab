# Matbench v0.1 score recomputation

- Results artifact: `vendor/matbench/benchmarks/matbench_v0.1_rf/results.json.gz`
- Fold scores checked: 15
- Max absolute stored-vs-recomputed score delta: 0.000e+00

## Fold checks

| Task | Fold | n | Prediction type | Max score delta | Stored rocauc | Probability rocauc |
|---|---:|---:|---|---:|---:|---:|
| matbench_dielectric | 0 | 953 | float | 0.000e+00 |  |  |
| matbench_dielectric | 1 | 953 | float | 0.000e+00 |  |  |
| matbench_dielectric | 2 | 953 | float | 0.000e+00 |  |  |
| matbench_dielectric | 3 | 953 | float | 0.000e+00 |  |  |
| matbench_dielectric | 4 | 952 | float | 0.000e+00 |  |  |
| matbench_log_gvrh | 0 | 2198 | float | 0.000e+00 |  |  |
| matbench_log_gvrh | 1 | 2198 | float | 0.000e+00 |  |  |
| matbench_log_gvrh | 2 | 2197 | float | 0.000e+00 |  |  |
| matbench_log_gvrh | 3 | 2197 | float | 0.000e+00 |  |  |
| matbench_log_gvrh | 4 | 2197 | float | 0.000e+00 |  |  |
| matbench_log_kvrh | 0 | 2198 | float | 0.000e+00 |  |  |
| matbench_log_kvrh | 1 | 2198 | float | 0.000e+00 |  |  |
| matbench_log_kvrh | 2 | 2197 | float | 0.000e+00 |  |  |
| matbench_log_kvrh | 3 | 2197 | float | 0.000e+00 |  |  |
| matbench_log_kvrh | 4 | 2197 | float | 0.000e+00 |  |  |

## Recomputed fold aggregates

### matbench_dielectric

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| mae | 0.419578159259 | 0.52198700518 | 0.304162451401 | 0.0750037451263 |
| rmse | 1.85382481618 | 2.98323049778 | 0.785044337763 | 0.770049375991 |
| mape | 0.139968218264 | 0.188632999374 | 0.10574510663 | 0.0288667979365 |
| max_error | 34.8805599225 | 59.1201445981 | 14.5978573183 | 16.9979726853 |

### matbench_log_gvrh

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| mae | 0.103998778594 | 0.106730986524 | 0.102382766772 | 0.00158833792656 |
| rmse | 0.154040121902 | 0.160123342295 | 0.149548591245 | 0.00365247845886 |
| mape | 0.0807614737326 | 0.0832065562181 | 0.0776724866644 | 0.0018807671835 |
| max_error | 1.15770278575 | 1.69423726872 | 0.904052794872 | 0.284521613255 |

### matbench_log_kvrh

| Metric | mean | max | min | std |
|---|---:|---:|---:|---:|
| mae | 0.0819825484217 | 0.0862696399472 | 0.0783141445137 | 0.00271972565089 |
| rmse | 0.145360912566 | 0.150255516099 | 0.138320059166 | 0.00462831988118 |
| mape | 0.054592530708 | 0.0607661711246 | 0.050921152629 | 0.00348070098442 |
| max_error | 1.37315631231 | 1.76416363754 | 1.11891531674 | 0.231105610567 |
