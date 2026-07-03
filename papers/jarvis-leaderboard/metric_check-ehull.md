# Metric Check - JARVIS-Leaderboard Layer A

Target: `AI-SinglePropertyPrediction-ehull-dft_3d-test-mae`
Vendor repo: `vendor/jarvis_leaderboard`
Ground-truth split sizes: {'train': 44290, 'val': 5537, 'test': 5537}

The score is recomputed from the public submission CSV zip and benchmark JSON zip artifacts. This mirrors the upstream `rebuild.py::get_metric_value` path for MAE but uses a small stdlib-only implementation.
Models scored: 11

| model | team | official MAE | reproduced MAE | rows | id check | pass |
|---|---|---:|---:|---:|---|---|
| kgcnn_coNGN | kgcnn | 0.0485 | 0.04854471 | 5537 | exact | yes |
| kgcnn_coGN | kgcnn | 0.0466 | 0.04663351 | 5537 | exact | yes |
| cgcnn_model | CGCNN | 0.173 | 0.17303957 | 5537 | exact | yes |
| potnet | DIVE@TAMU | 0.0522 | 0.05216660 | 5537 | exact | yes |
| kgcnn_schnet | kgcnn | 0.1014 | 0.10137342 | 5537 | exact | yes |
| kgcnn_megnet | kgcnn | 0.0569 | 0.05692482 | 5537 | exact | yes |
| kgcnn_dimenetPP | kgcnn | 0.3685 | 0.36845777 | 5537 | exact | yes |
| alignn_model | ALIGNN | 0.0763 | 0.07625421 | 5537 | exact | yes |
| matminer_rf | UofT | 0.112 | 0.11201492 | 5537 | exact | yes |
| matminer_xgboost | UofT | 0.0601 | 0.06010375 | 5537 | exact | yes |
| kgcnn_cgcnn | kgcnn | 0.059 | 0.05903185 | 5537 | exact | yes |

## Closest adjacent scores

The official page reports point estimates only; this table flags adjacent MAE gaps that may deserve uncertainty or sensitivity checks later.

| pair | official MAE gap | reproduced MAE gap |
|---|---:|---:|
| kgcnn_cgcnn to matminer_xgboost | 0.0011 | 0.00107191 |
| kgcnn_coGN to kgcnn_coNGN | 0.0019 | 0.00191120 |
| kgcnn_megnet to kgcnn_cgcnn | 0.0021 | 0.00210703 |
| kgcnn_coNGN to potnet | 0.0037 | 0.00362190 |
| potnet to kgcnn_megnet | 0.0047 | 0.00475822 |

## Scope

- Layer A only: metric recomputation from already-published artifacts.
- No model training or model execution yet.
- The target was chosen because the official page exposes CSV predictions, JSON ground truth, run scripts, and metadata.

## Next

Next, decide whether to broaden across more JARVIS tasks or attempt one Layer B model-execution smoke for a tractable baseline.
