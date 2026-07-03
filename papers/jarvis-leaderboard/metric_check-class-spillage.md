# Metric Check - JARVIS-Leaderboard Layer A

Target: `AI-SinglePropertyClass-spillage-dft_3d-test-acc`
Vendor repo: `vendor/jarvis_leaderboard`
Ground-truth split sizes: {'train': 9101, 'val': 1137, 'test': 1137}

The score is recomputed from the public submission CSV zip and benchmark JSON zip artifacts. This mirrors the upstream `rebuild.py::get_metric_value` path for `acc` but uses a small stdlib-only implementation.
Models scored: 3

| model | team | official ACC | reproduced ACC | rows | id check | pass |
|---|---|---:|---:|---:|---|---|
| alignn_model | ALIGNN | 0.8135 | 0.81354442 | 1137 | exact | yes |
| matminer_rf | UofT | 0.8311 | 0.83113456 | 1137 | exact | yes |
| matminer_xgboost | UofT | 0.8364 | 0.83641161 | 1137 | exact | yes |

## Closest adjacent scores

The official page reports point estimates only; this table flags adjacent ACC gaps that may deserve uncertainty or sensitivity checks later.

| pair | official ACC gap | reproduced ACC gap |
|---|---:|---:|
| matminer_rf to matminer_xgboost | 0.0053 | 0.00527704 |
| alignn_model to matminer_rf | 0.0176 | 0.01759015 |

## Scope

- Layer A only: metric recomputation from already-published artifacts.
- No model training or model execution yet.
- The target was chosen because the official page exposes CSV predictions, JSON ground truth, run scripts, and metadata.

## Next

Next, decide whether to broaden across more JARVIS tasks or attempt one Layer B model-execution smoke for a tractable baseline.
