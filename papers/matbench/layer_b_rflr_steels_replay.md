# Matbench v0.1 RFLR steels source replay

- Submission: `matbench_v0.1_RFLR` / `RF-Regex Steels`
- Task: `matbench_steels`
- Source artifacts used: `Matbench_Steels_RFLR.ipynb`, `results.json.gz`
- Python environment: `env/matbench-tpot`
- scikit-learn version: `1.2.2`
- Model: `RandomForestRegressor(n_estimators=30, random_state=1)`
- Folds replayed: 5
- Max absolute prediction delta vs submitted artifact: 0.000e+00
- Max absolute score delta vs submitted artifact: 0.000e+00

## Method

The replay mirrors the submitted notebook: convert each steel composition string into 13 fixed element-fraction columns with the notebook regex, fit a 30-tree scikit-learn random forest with `random_state=1` on each official training fold, predict the held-out fold, then compare with the committed `results.json.gz` predictions and stored scores.

## Fold comparison

| Fold | Train n | Test n | Max prediction delta | Mean prediction delta | Submitted MAE | Replay MAE | MAE delta | Max score delta |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 249 | 63 | 0 | 0 | 97.5403703704 | 97.5403703704 | 0 | 0 |
| 1 | 249 | 63 | 0 | 0 | 86.2788888889 | 86.2788888889 | 0 | 0 |
| 2 | 250 | 62 | 0 | 0 | 79.5098924731 | 79.5098924731 | 0 | 0 |
| 3 | 250 | 62 | 0 | 0 | 94.5817204301 | 94.5817204301 | 0 | 0 |
| 4 | 250 | 62 | 0 | 0 | 95.0371505376 | 95.0371505376 | 0 | 0 |

## Interpretation

The source replay is prediction-identical to the submitted artifact.

## Version note

A logged control run in env/jarvis with scikit-learn 1.9.0 was runnable but non-identical (max prediction delta 108.587, max score delta 22.307). The prediction-identical replay above uses scikit-learn 1.2.2.
