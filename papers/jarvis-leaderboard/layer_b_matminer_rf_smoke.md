# Layer B Pre-smoke - JARVIS matminer_rf

Target: `AI-SinglePropertyPrediction-formation_energy_peratom-dft_3d-test-mae`

Status: passed. This is a bounded CPU execution-path smoke, not a full
leaderboard reproduction and not a claim to reproduce the official
`matminer_rf` MAE.

## Result

- Train rows: 32
- Test rows: 16
- Feature columns: 273
- All-NaN feature rows: 0
- Random forest trees: 100
- Subset MAE: 0.62991474
- Runtime seconds: 26.7
- Prediction CSV: `experiments\jarvis-leaderboard\matminer_rf_smoke\predictions.csv`

## Scope

- Uses the official benchmark train/test split, truncated deterministically
  to the first `--train-size` train ids and first `--test-size` test ids.
- Uses JARVIS `dft_3d` structures fetched by `jarvis-tools`.
- Uses the same broad Matminer feature family and RF hyperparameters as the
  public `matminer_rf` script, but does not run the full 55k-row test page.
- Intended to prove the Layer B execution path is viable in an isolated env.

## Sample ids

- First train id: `JVASP-21450`
- First test id: `JVASP-38636`
