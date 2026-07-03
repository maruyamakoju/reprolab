# Metric Check - JARVIS-Leaderboard Layer A

Target: `AI-SinglePropertyClass-n_powerfact-dft_3d-test-acc`
Vendor repo: `vendor/jarvis_leaderboard`
Ground-truth split sizes: {'train': 18568, 'val': 2321, 'test': 2321}

The score is recomputed from the public submission CSV zip and benchmark JSON zip artifacts. This mirrors the upstream `rebuild.py::get_metric_value` path for `acc` but uses a small stdlib-only implementation.
Models scored: 3

| model | team | official ACC | reproduced ACC | rows | id check | pass |
|---|---|---:|---:|---:|---|---|
| alignn_model | ALIGNN | 0.7897 | 0.78974580 | 2321 | exact | yes |
| matminer_rf | UofT | 0.8065 | 0.80654890 | 2321 | exact | yes |
| matminer_xgboost | UofT | 0.8186 | 0.81861267 | 2321 | exact | yes |

## Closest adjacent scores

The official page reports point estimates only; this table flags adjacent ACC gaps that may deserve uncertainty or sensitivity checks later.

| pair | official ACC gap | reproduced ACC gap |
|---|---:|---:|
| matminer_rf to matminer_xgboost | 0.0121 | 0.01206377 |
| alignn_model to matminer_rf | 0.0168 | 0.01680310 |

## Scope

- Layer A only: metric recomputation from already-published artifacts.
- No model training or model execution yet.
- The target was chosen because the official page exposes CSV predictions, JSON ground truth, run scripts, and metadata.

## Next

Next, decide whether to broaden across more JARVIS tasks or attempt one Layer B model-execution smoke for a tractable baseline.
