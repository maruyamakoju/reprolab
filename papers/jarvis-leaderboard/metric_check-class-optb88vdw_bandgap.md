# Metric Check - JARVIS-Leaderboard Layer A

Target: `AI-SinglePropertyClass-optb88vdw_bandgap-dft_3d-test-acc`
Vendor repo: `vendor/jarvis_leaderboard`
Ground-truth split sizes: {'train': 44569, 'val': 5572, 'test': 5572}

The score is recomputed from the public submission CSV zip and benchmark JSON zip artifacts. This mirrors the upstream `rebuild.py::get_metric_value` path for `acc` but uses a small stdlib-only implementation.
Models scored: 3

| model | team | official ACC | reproduced ACC | rows | id check | pass |
|---|---|---:|---:|---:|---|---|
| alignn_model | ALIGNN | 0.9327 | 0.93269921 | 5572 | exact | yes |
| matminer_rf | UofT | 0.9318 | 0.93180187 | 5572 | exact | yes |
| matminer_xgboost | UofT | 0.9361 | 0.93610912 | 5572 | exact | yes |

## Closest adjacent scores

The official page reports point estimates only; this table flags adjacent ACC gaps that may deserve uncertainty or sensitivity checks later.

| pair | official ACC gap | reproduced ACC gap |
|---|---:|---:|
| matminer_rf to alignn_model | 0.0009 | 0.00089734 |
| alignn_model to matminer_xgboost | 0.0034 | 0.00340991 |

## Scope

- Layer A only: metric recomputation from already-published artifacts.
- No model training or model execution yet.
- The target was chosen because the official page exposes CSV predictions, JSON ground truth, run scripts, and metadata.

## Next

Next, decide whether to broaden across more JARVIS tasks or attempt one Layer B model-execution smoke for a tractable baseline.
