# Metric Check - JARVIS-Leaderboard Layer A

Target: `AI-SinglePropertyClass-magmom_oszicar-dft_3d-test-acc`
Vendor repo: `vendor/jarvis_leaderboard`
Ground-truth split sizes: {'train': 41766, 'val': 5222, 'test': 5222}

The score is recomputed from the public submission CSV zip and benchmark JSON zip artifacts. This mirrors the upstream `rebuild.py::get_metric_value` path for `acc` but uses a small stdlib-only implementation.
Models scored: 3

| model | team | official ACC | reproduced ACC | rows | id check | pass |
|---|---|---:|---:|---:|---|---|
| alignn_model | ALIGNN | 0.945 | 0.94504021 | 5222 | exact | yes |
| matminer_rf | UofT | 0.9458 | 0.94580620 | 5222 | exact | yes |
| matminer_xgboost | UofT | 0.9489 | 0.94887016 | 5222 | exact | yes |

## Closest adjacent scores

The official page reports point estimates only; this table flags adjacent ACC gaps that may deserve uncertainty or sensitivity checks later.

| pair | official ACC gap | reproduced ACC gap |
|---|---:|---:|
| alignn_model to matminer_rf | 0.0008 | 0.00076599 |
| matminer_rf to matminer_xgboost | 0.0031 | 0.00306396 |

## Scope

- Layer A only: metric recomputation from already-published artifacts.
- No model training or model execution yet.
- The target was chosen because the official page exposes CSV predictions, JSON ground truth, run scripts, and metadata.

## Next

Next, decide whether to broaden across more JARVIS tasks or attempt one Layer B model-execution smoke for a tractable baseline.
