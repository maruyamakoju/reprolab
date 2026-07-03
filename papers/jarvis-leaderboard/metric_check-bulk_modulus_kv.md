# Metric Check - JARVIS-Leaderboard Layer A

Target: `AI-SinglePropertyPrediction-bulk_modulus_kv-dft_3d-test-mae`
Vendor repo: `vendor/jarvis_leaderboard`
Ground-truth split sizes: {'train': 15744, 'val': 1968, 'test': 1968}

The score is recomputed from the public submission CSV zip and benchmark JSON zip artifacts. This mirrors the upstream `rebuild.py::get_metric_value` path for `mae` but uses a small stdlib-only implementation.
Models scored: 12

| model | team | official MAE | reproduced MAE | rows | id check | pass |
|---|---|---:|---:|---:|---|---|
| kgcnn_coNGN | kgcnn | 8.7022 | 8.70219322 | 1968 | exact | yes |
| kgcnn_coGN | kgcnn | 8.992 | 8.99203924 | 1968 | exact | yes |
| kgcnn_schnet | kgcnn | 10.7105 | 10.71047255 | 1968 | exact | yes |
| matminer_lgbm | Matminer | 15.4752 | 15.47517687 | 1968 | exact | yes |
| kgcnn_megnet | kgcnn | 11.4287 | 11.42867602 | 1968 | exact | yes |
| kgcnn_dimenetPP | kgcnn | 13.3743 | 13.37431796 | 1968 | exact | yes |
| cfid_chem | JARVIS | 15.5726 | 15.57257995 | 1968 | exact | yes |
| cfid | JARVIS | 14.1999 | 14.19994925 | 1968 | exact | yes |
| alignn_model | ALIGNN | 10.3988 | 10.39883748 | 1968 | exact | yes |
| matminer_rf | UofT | 14.1108 | 14.11083439 | 1968 | exact | yes |
| matminer_xgboost | UofT | 12.7411 | 12.74114673 | 1968 | exact | yes |
| kgcnn_cgcnn | kgcnn | 11.0148 | 11.01483561 | 1968 | exact | yes |

## Closest adjacent scores

The official page reports point estimates only; this table flags adjacent MAE gaps that may deserve uncertainty or sensitivity checks later.

| pair | official MAE gap | reproduced MAE gap |
|---|---:|---:|
| matminer_rf to cfid | 0.0891 | 0.08911486 |
| matminer_lgbm to cfid_chem | 0.0974 | 0.09740308 |
| kgcnn_coNGN to kgcnn_coGN | 0.2898 | 0.28984601 |
| kgcnn_schnet to kgcnn_cgcnn | 0.3043 | 0.30436306 |
| alignn_model to kgcnn_schnet | 0.3117 | 0.31163507 |

## Scope

- Layer A only: metric recomputation from already-published artifacts.
- No model training or model execution yet.
- The target was chosen because the official page exposes CSV predictions, JSON ground truth, run scripts, and metadata.

## Next

Next, decide whether to broaden across more JARVIS tasks or attempt one Layer B model-execution smoke for a tractable baseline.
