# Matbench v0.1 TPOT steels source replay

- Submission: `matbench_v0.1_TPOT` / `TPOT-Mat`
- Task: `matbench_steels`
- Source artifacts used: `Matbench_steel_TPOT.ipynb`, `utils.py`, `tpot_best_pipeline.pkl`, `results.json.gz`
- Python environment: `env/matbench-tpot`
- Audit random seed: `0`
- Folds replayed: 5
- Max absolute prediction delta vs submitted artifact: 1.629e+02
- Max absolute score delta vs submitted artifact: 2.477e+01

## Method

The replay mirrors the notebook path: load the pickled TPOT pipeline, load Matbench's steels folds, convert composition strings with the submitted `LoadExisting.cleaning` helper, refit the pipeline on each training fold, predict the held-out fold, then compare with the committed `results.json.gz` predictions and stored scores. The submitted notebook does not set a random seed; this audit sets one so the replay report is stable.

## Fold comparison

| Fold | Train n | Test n | Max prediction delta | Mean prediction delta | Submitted MAE | Replay MAE | MAE delta |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 249 | 63 | 162.894287109 | 17.8011435857 | 105.636302161 | 100.433370536 | 5.20293162512 |
| 1 | 249 | 63 | 76.1984863281 | 17.4563530816 | 66.3153579954 | 66.5803722563 | 0.265014260913 |
| 2 | 250 | 62 | 95.1945800781 | 17.3075896232 | 78.2786392704 | 78.4412038495 | 0.162564579133 |
| 3 | 250 | 62 | 122.348510742 | 20.5586784117 | 77.9676911385 | 75.5824372322 | 2.38525390625 |
| 4 | 250 | 62 | 59.8782958984 | 16.3402532762 | 71.5360627205 | 74.4317926222 | 2.89572990171 |
