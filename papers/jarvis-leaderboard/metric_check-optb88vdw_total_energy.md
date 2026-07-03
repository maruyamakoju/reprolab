# Metric Check - JARVIS-Leaderboard Layer A

Target: `AI-SinglePropertyPrediction-optb88vdw_total_energy-dft_3d-test-mae`
Vendor repo: `vendor/jarvis_leaderboard`
Ground-truth split sizes: {'train': 44569, 'val': 5572, 'test': 5572}

The score is recomputed from the public submission CSV zip and benchmark JSON zip artifacts. This mirrors the upstream `rebuild.py::get_metric_value` path for `mae` but uses a small stdlib-only implementation.
Models scored: 14

| model | team | official MAE | reproduced MAE | rows | id check | pass |
|---|---|---:|---:|---:|---|---|
| kgcnn_coNGN | kgcnn | 0.0273 | 0.02732437 | 5572 | exact | yes |
| kgcnn_coGN | kgcnn | 0.0262 | 0.02620960 | 5572 | exact | yes |
| cgcnn_model | CGCNN | 0.0815 | 0.08154179 | 5572 | exact | yes |
| potnet | DIVE@TAMU | 0.0321 | 0.03213739 | 5572 | exact | yes |
| kgcnn_schnet | kgcnn | 0.0374 | 0.03737607 | 5572 | exact | yes |
| matminer_lgbm | Matminer | 0.1509 | 0.15091305 | 5572 | exact | yes |
| kgcnn_megnet | kgcnn | 0.0393 | 0.03928123 | 5572 | exact | yes |
| kgcnn_dimenetPP | kgcnn | 0.051 | 0.05096236 | 5572 | exact | yes |
| cfid_chem | JARVIS | 0.3526 | 0.35263653 | 5572 | exact | yes |
| cfid | JARVIS | 0.2436 | 0.24363629 | 5572 | exact | yes |
| alignn_model | ALIGNN | 0.0367 | 0.03668744 | 5572 | exact | yes |
| matminer_rf | UofT | 0.1544 | 0.15435009 | 5572 | exact | yes |
| matminer_xgboost | UofT | 0.0936 | 0.09359743 | 5572 | exact | yes |
| kgcnn_cgcnn | kgcnn | 0.0584 | 0.05844295 | 5572 | exact | yes |

## Closest adjacent scores

The official page reports point estimates only; this table flags adjacent MAE gaps that may deserve uncertainty or sensitivity checks later.

| pair | official MAE gap | reproduced MAE gap |
|---|---:|---:|
| alignn_model to kgcnn_schnet | 0.0007 | 0.00068863 |
| kgcnn_coGN to kgcnn_coNGN | 0.0011 | 0.00111477 |
| kgcnn_schnet to kgcnn_megnet | 0.0019 | 0.00190516 |
| matminer_lgbm to matminer_rf | 0.0035 | 0.00343703 |
| potnet to alignn_model | 0.0046 | 0.00455005 |

## Scope

- Layer A only: metric recomputation from already-published artifacts.
- No model training or model execution yet.
- The target was chosen because the official page exposes CSV predictions, JSON ground truth, run scripts, and metadata.

## Next

Next, decide whether to broaden across more JARVIS tasks or attempt one Layer B model-execution smoke for a tractable baseline.
