# Summary - JARVIS-Leaderboard Paper-002 Candidate

Status: Layer A metric recomputation has passed for 14 JARVIS-Leaderboard AI
benchmarks: 6 regression pages, 7 classification pages, and 1 spectra page.
Layer B has an execution-path probe, but no model-execution smoke yet.

## Result

The audit recomputed MAE directly from public benchmark JSON zips and contribution
CSV zips, mirroring the upstream `rebuild.py::get_metric_value` logic with a small
stdlib-only implementation (`scripts/jarvis_score.py`).

All 101 checked submissions match the official docs-page metric within displayed
rounding, and every checked CSV id set exactly matches the corresponding JSON
`test` split.

## Regression pages

| benchmark property | submissions | test rows | metric | report |
|---|---:|---:|---:|---|
| formation_energy_peratom | 15 | 5,572 | MAE | `metric_check.md` |
| ehull | 11 | 5,537 | MAE | `metric_check-ehull.md` |
| optb88vdw_bandgap | 14 | 5,572 | MAE | `metric_check-optb88vdw_bandgap.md` |
| optb88vdw_total_energy | 14 | 5,572 | MAE | `metric_check-optb88vdw_total_energy.md` |
| bulk_modulus_kv | 12 | 1,968 | MAE | `metric_check-bulk_modulus_kv.md` |
| slme | 13 | 906 | MAE | `metric_check-slme.md` |

## Classification pages

| benchmark property | submissions | test rows | metric | report |
|---|---:|---:|---:|---|
| magmom_oszicar | 3 | 5,222 | ACC | `metric_check-class-magmom_oszicar.md` |
| mbj_bandgap | 3 | 1,815 | ACC | `metric_check-class-mbj_bandgap.md` |
| n_powerfact | 3 | 2,321 | ACC | `metric_check-class-n_powerfact.md` |
| optb88vdw_bandgap | 3 | 5,572 | ACC | `metric_check-class-optb88vdw_bandgap.md` |
| p_Seebeck | 3 | 2,321 | ACC | `metric_check-class-p_Seebeck.md` |
| slme | 3 | 906 | ACC | `metric_check-class-slme.md` |
| spillage | 3 | 1,137 | ACC | `metric_check-class-spillage.md` |

## Spectra page

| benchmark property | submissions | test rows | metric | report |
|---|---:|---:|---:|---|
| ph_dos / edos_pdos | 1 | 1,424 | MULTIMAE | `metric_check-spectra-ph_dos.md` |

## Interpretation

This is a positive Layer A result: for the sampled JARVIS pages, the reported
leaderboard MAE/ACC/MULTIMAE values are exactly recoverable from the public
artifacts.

The closest adjacent score gaps are small on several pages, for example 0.0002 MAE
between `kgcnn_coNGN` and `potnet` on formation energy, and 0.0013 MAE between
`matminer_rf` and `cgcnn_model` on optB88vdW bandgap. The docs pages report point
estimates only, so uncertainty or split-sensitivity analysis is the natural Layer C
analogue if this becomes the main Paper-002 target.

One packaging note surfaced in the classification tasks: the outer zip filenames
correctly use `test-acc.csv.zip`, but the single CSV stored inside those zips is
named `test-mae.csv`. Upstream reads the zip directly and is unaffected; independent
tools should not assume the internal filename matches the outer archive.

## Layer B probe

The first execution-path probe inspected the public `matminer_rf`,
`matminer_xgboost`, `cfid`, and `cfid_chem` contribution runners. The current
Matbench audit venv lacks `jarvis`, `matminer`, `xgboost`, and `lightgbm`; a
`pip --dry-run` dependency solve succeeds, but would add a broad JARVIS stack to
the shared environment.

The runners are also not one-command fits for the audited dft_3d formation-energy
page: the matminer scripts are hardcoded to `snumat`, `matminer_xgboost` defaults
to `gpu_hist`, and the CFID scripts use a different benchmark path convention plus
full descriptor/data-directory generation. Details are in `layer_b_probe.md`.

## Next

The best next move is an isolated JARVIS env and a small `matminer_rf` wrapper for
`dft_3d` formation energy. If that is too slow or invasive, Paper-002 can be
stopped as a strong three-format Layer A audit with a documented Layer B blocker.
