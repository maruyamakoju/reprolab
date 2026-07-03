# Summary - JARVIS-Leaderboard Paper-002 Candidate

Status: Layer A metric recomputation has passed for 14 JARVIS-Leaderboard AI
benchmarks: 6 regression pages, 7 classification pages, and 1 spectra page.
Layer B has a bounded `matminer_rf` execution-path pre-smoke.
Layer C has a point-gap map across the checked pages.

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

## Layer B pre-smoke

An isolated JARVIS env was then created under `env/jarvis`, with `jarvis-tools` and
`matminer` installed. `scripts/jarvis_matminer_rf_smoke.py` ran a bounded CPU smoke
on the official dft_3d formation-energy split: 1024 train rows, 256 test rows, 273
Matminer feature columns, 100-tree random forest, 0 all-NaN feature rows, subset
MAE 0.26783845. Report: `layer_b_matminer_rf_smoke.md`.

This is not a full leaderboard regeneration and does not claim the official
`matminer_rf` MAE. It establishes that the public runner family can be adapted into
a traceable Layer B execution path without mutating the Paper-001 environment.

## Layer C point-gap map

`scripts/jarvis_resolution.py` parsed the 14 checked metric reports and sorted each
page by its metric direction. Across 87 adjacent pairs, 5 official gaps are
<=0.001, 29 are <=0.005, and 38 are <=0.010 in metric units. The closest adjacent
pair is `kgcnn_coNGN` to `potnet` on dft_3d formation energy: official MAE gap
0.0002, reproduced gap 0.00016852. Report: `layer_c_resolution.md`.

## Layer C paired bootstrap

`scripts/jarvis_bootstrap.py` then bootstrapped the 20 closest adjacent pairs over
the fixed public test rows (B=2000, seed=42). This is not retraining uncertainty or
alternate-split uncertainty; it asks whether the observed paired test-row advantage
is stable under resampling of the published test set.

Result: 17/20 closest adjacent-pair 95% CIs include zero. For the closest pair,
`kgcnn_coNGN` over `potnet` on dft_3d formation energy, the official MAE gap is
0.0002, the paired advantage is 0.00016852, the 95% CI is [-0.00160975,
0.00156560], and P(tie/reversal) is 0.4030. Report: `layer_c_bootstrap.md`.

## Next

The best next move is cautious scale-up of the `matminer_rf` smoke. If feature
runtime grows too quickly, Paper-002 can be stopped as a strong three-format Layer A
audit plus a bounded Layer B execution-path result and Layer C point-gap/bootstrap
map.
