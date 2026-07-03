# Metric Check - JARVIS-Leaderboard Layer A

Target: `AI-Spectra-ph_dos-edos_pdos-test-multimae`
Vendor repo: `vendor/jarvis_leaderboard`
Ground-truth split sizes: {'train': 11395, 'val': 1424, 'test': 1424}

The score is recomputed from the public submission CSV zip and benchmark JSON zip artifacts. This mirrors the upstream `rebuild.py::get_metric_value` path for `multimae` but uses a small stdlib-only implementation.
Models scored: 1

| model | team | official MULTIMAE | reproduced MULTIMAE | rows | id check | pass |
|---|---|---:|---:|---:|---|---|
| alignn_model | ALIGNN | 0.05772635693310998 | 0.05772636 | 1424 | exact | yes |

## Scope

- Layer A only: metric recomputation from already-published artifacts.
- No model training or model execution yet.
- The target was chosen because the official page exposes CSV predictions, JSON ground truth, run scripts, and metadata.

## Next

Next, decide whether to broaden across more JARVIS tasks or attempt one Layer B model-execution smoke for a tractable baseline.
