# Summary - JARVIS-Leaderboard Paper-002 Candidate

Status: Layer A metric recomputation has passed for 6 JARVIS-Leaderboard AI
single-property-prediction benchmarks.

## Result

The audit recomputed MAE directly from public benchmark JSON zips and contribution
CSV zips, mirroring the upstream `rebuild.py::get_metric_value` logic with a small
stdlib-only implementation (`scripts/jarvis_score.py`).

All 79 checked submissions match the official docs-page MAE within displayed
rounding, and every checked CSV id set exactly matches the corresponding JSON
`test` split.

| benchmark property | submissions | test rows | report |
|---|---:|---:|---|
| formation_energy_peratom | 15 | 5,572 | `metric_check.md` |
| ehull | 11 | 5,537 | `metric_check-ehull.md` |
| optb88vdw_bandgap | 14 | 5,572 | `metric_check-optb88vdw_bandgap.md` |
| optb88vdw_total_energy | 14 | 5,572 | `metric_check-optb88vdw_total_energy.md` |
| bulk_modulus_kv | 12 | 1,968 | `metric_check-bulk_modulus_kv.md` |
| slme | 13 | 906 | `metric_check-slme.md` |

## Interpretation

This is a positive Layer A result: for the sampled JARVIS pages, the reported
leaderboard MAE values are exactly recoverable from the public artifacts.

The closest adjacent score gaps are small on several pages, for example 0.0002 MAE
between `kgcnn_coNGN` and `potnet` on formation energy, and 0.0013 MAE between
`matminer_rf` and `cgcnn_model` on optB88vdW bandgap. The docs pages report point
estimates only, so uncertainty or split-sensitivity analysis is the natural Layer C
analogue if this becomes the main Paper-002 target.

## Next

The best next move is not more MAE recomputation on near-identical pages; it is
either a broader task-family sample (classification or spectra) or one tractable
Layer B model-execution smoke for a simple baseline.
