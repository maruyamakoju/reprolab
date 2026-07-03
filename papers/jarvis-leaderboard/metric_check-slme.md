# Metric Check - JARVIS-Leaderboard Layer A

Target: `AI-SinglePropertyPrediction-slme-dft_3d-test-mae`
Vendor repo: `vendor/jarvis_leaderboard`
Ground-truth split sizes: {'train': 7250, 'val': 906, 'test': 906}

The score is recomputed from the public submission CSV zip and benchmark JSON zip artifacts. This mirrors the upstream `rebuild.py::get_metric_value` path for `mae` but uses a small stdlib-only implementation.
Models scored: 13

| model | team | official MAE | reproduced MAE | rows | id check | pass |
|---|---|---:|---:|---:|---|---|
| kgcnn_coNGN | kgcnn | 4.4428 | 4.44277482 | 906 | exact | yes |
| kgcnn_coGN | kgcnn | 4.4507 | 4.45069549 | 906 | exact | yes |
| cgcnn_model | CGCNN | 5.6603 | 5.66033686 | 906 | exact | yes |
| kgcnn_schnet | kgcnn | 5.3222 | 5.32216693 | 906 | exact | yes |
| matminer_lgbm | Matminer | 5.4242 | 5.42422043 | 906 | exact | yes |
| kgcnn_megnet | kgcnn | 5.0614 | 5.06136079 | 906 | exact | yes |
| kgcnn_dimenetPP | kgcnn | 5.6403 | 5.64029506 | 906 | exact | yes |
| cfid_chem | JARVIS | 6.5321 | 6.53214181 | 906 | exact | yes |
| cfid | JARVIS | 6.2607 | 6.26070041 | 906 | exact | yes |
| alignn_model | ALIGNN | 4.5207 | 4.52067485 | 906 | exact | yes |
| matminer_rf | UofT | 5.1235 | 5.12345466 | 906 | exact | yes |
| matminer_xgboost | UofT | 4.9255 | 4.92548902 | 906 | exact | yes |
| kgcnn_cgcnn | kgcnn | 5.0139 | 5.01394452 | 906 | exact | yes |

## Closest adjacent scores

The official page reports point estimates only; this table flags adjacent MAE gaps that may deserve uncertainty or sensitivity checks later.

| pair | official MAE gap | reproduced MAE gap |
|---|---:|---:|
| kgcnn_coNGN to kgcnn_coGN | 0.0079 | 0.00792067 |
| kgcnn_dimenetPP to cgcnn_model | 0.0200 | 0.02004180 |
| kgcnn_cgcnn to kgcnn_megnet | 0.0475 | 0.04741627 |
| kgcnn_megnet to matminer_rf | 0.0621 | 0.06209388 |
| kgcnn_coGN to alignn_model | 0.0700 | 0.06997936 |

## Scope

- Layer A only: metric recomputation from already-published artifacts.
- No model training or model execution yet.
- The target was chosen because the official page exposes CSV predictions, JSON ground truth, run scripts, and metadata.

## Next

Next, decide whether to broaden across more JARVIS tasks or attempt one Layer B model-execution smoke for a tractable baseline.
