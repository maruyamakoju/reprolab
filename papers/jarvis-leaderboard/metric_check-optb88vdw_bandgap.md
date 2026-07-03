# Metric Check - JARVIS-Leaderboard Layer A

Target: `AI-SinglePropertyPrediction-optb88vdw_bandgap-dft_3d-test-mae`
Vendor repo: `vendor/jarvis_leaderboard`
Ground-truth split sizes: {'train': 44569, 'val': 5572, 'test': 5572}

The score is recomputed from the public submission CSV zip and benchmark JSON zip artifacts. This mirrors the upstream `rebuild.py::get_metric_value` path for MAE but uses a small stdlib-only implementation.
Models scored: 14

| model | team | official MAE | reproduced MAE | rows | id check | pass |
|---|---|---:|---:|---:|---|---|
| kgcnn_coNGN | kgcnn | 0.1267 | 0.12669279 | 5572 | exact | yes |
| kgcnn_coGN | kgcnn | 0.1219 | 0.12188751 | 5572 | exact | yes |
| cgcnn_model | CGCNN | 0.1908 | 0.19082040 | 5572 | exact | yes |
| potnet | DIVE@TAMU | 0.1246 | 0.12463427 | 5572 | exact | yes |
| kgcnn_schnet | kgcnn | 0.698 | 0.69798998 | 5572 | exact | yes |
| matminer_lgbm | Matminer | 0.2021 | 0.20208063 | 5572 | exact | yes |
| kgcnn_megnet | kgcnn | 0.146 | 0.14604425 | 5572 | exact | yes |
| kgcnn_dimenetPP | kgcnn | 0.2247 | 0.22467448 | 5572 | exact | yes |
| cfid_chem | JARVIS | 0.4057 | 0.40568531 | 5572 | exact | yes |
| cfid | JARVIS | 0.299 | 0.29904368 | 5572 | exact | yes |
| alignn_model | ALIGNN | 0.1423 | 0.14232787 | 5572 | exact | yes |
| matminer_rf | UofT | 0.1895 | 0.18945517 | 5572 | exact | yes |
| matminer_xgboost | UofT | 0.1873 | 0.18732505 | 5572 | exact | yes |
| kgcnn_cgcnn | kgcnn | 0.1857 | 0.18574149 | 5572 | exact | yes |

## Closest adjacent scores

The official page reports point estimates only; this table flags adjacent MAE gaps that may deserve uncertainty or sensitivity checks later.

| pair | official MAE gap | reproduced MAE gap |
|---|---:|---:|
| matminer_rf to cgcnn_model | 0.0013 | 0.00136523 |
| kgcnn_cgcnn to matminer_xgboost | 0.0016 | 0.00158357 |
| potnet to kgcnn_coNGN | 0.0021 | 0.00205851 |
| matminer_xgboost to matminer_rf | 0.0022 | 0.00213012 |
| kgcnn_coGN to potnet | 0.0027 | 0.00274677 |

## Scope

- Layer A only: metric recomputation from already-published artifacts.
- No model training or model execution yet.
- The target was chosen because the official page exposes CSV predictions, JSON ground truth, run scripts, and metadata.

## Next

Next, decide whether to broaden across more JARVIS tasks or attempt one Layer B model-execution smoke for a tractable baseline.
