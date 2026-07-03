# Metric Check - JARVIS-Leaderboard Layer A

Target: `AI-SinglePropertyPrediction-formation_energy_peratom-dft_3d-test-mae`
Vendor repo: `vendor/jarvis_leaderboard`
Ground-truth split sizes: {'train': 44569, 'val': 5572, 'test': 5572}

The score is recomputed from the public submission CSV zip and benchmark JSON zip artifacts. This mirrors the upstream `rebuild.py::get_metric_value` path for `mae` but uses a small stdlib-only implementation.
Models scored: 15

| model | team | official MAE | reproduced MAE | rows | id check | pass |
|---|---|---:|---:|---:|---|---|
| kgcnn_coNGN | kgcnn | 0.0291 | 0.02909801 | 5572 | exact | yes |
| kgcnn_coGN | kgcnn | 0.0271 | 0.02711760 | 5572 | exact | yes |
| cgcnn_model | CGCNN | 0.0625 | 0.06250565 | 5572 | exact | yes |
| potnet | DIVE@TAMU | 0.0293 | 0.02926653 | 5572 | exact | yes |
| kgcnn_schnet | kgcnn | 0.0365 | 0.03649074 | 5572 | exact | yes |
| matminer_lgbm | Matminer | 0.1023 | 0.10231528 | 5572 | exact | yes |
| kgcnn_megnet | kgcnn | 0.0423 | 0.04229563 | 5572 | exact | yes |
| kgcnn_dimenetPP | kgcnn | 0.0528 | 0.05282269 | 5572 | exact | yes |
| cfid_chem | JARVIS | 0.2226 | 0.22264128 | 5572 | exact | yes |
| matformer_256 | DIVE@TAMU | 0.0322 | 0.03218742 | 5572 | exact | yes |
| cfid | JARVIS | 0.1419 | 0.14186013 | 5572 | exact | yes |
| alignn_model | ALIGNN | 0.0331 | 0.03311989 | 5572 | exact | yes |
| matminer_rf | UofT | 0.096 | 0.09595936 | 5572 | exact | yes |
| matminer_xgboost | UofT | 0.0734 | 0.07339676 | 5572 | exact | yes |
| kgcnn_cgcnn | kgcnn | 0.0551 | 0.05508731 | 5572 | exact | yes |

## Closest adjacent scores

The official page reports point estimates only; this table flags adjacent MAE gaps that may deserve uncertainty or sensitivity checks later.

| pair | official MAE gap | reproduced MAE gap |
|---|---:|---:|
| kgcnn_coNGN to potnet | 0.0002 | 0.00016852 |
| matformer_256 to alignn_model | 0.0009 | 0.00093247 |
| kgcnn_coGN to kgcnn_coNGN | 0.0020 | 0.00198041 |
| kgcnn_dimenetPP to kgcnn_cgcnn | 0.0023 | 0.00226462 |
| potnet to matformer_256 | 0.0029 | 0.00292089 |

## Scope

- Layer A only: metric recomputation from already-published artifacts.
- No model training or model execution yet.
- The target was chosen because the official page exposes CSV predictions, JSON ground truth, run scripts, and metadata.

## Next

Next, decide whether to broaden across more JARVIS tasks or attempt one Layer B model-execution smoke for a tractable baseline.
