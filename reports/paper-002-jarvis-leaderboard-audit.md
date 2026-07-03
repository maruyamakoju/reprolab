# ReproLab Paper-002 - JARVIS-Leaderboard Audit

_Generated: 2026-07-03 07:20 UTC_

> Auto-assembled from tracked artifacts by `scripts/make_jarvis_report.py`.

## 0. Executive summary

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



## 1. Benchmark metadata

```
# ReproLab Paper-002 candidate - JARVIS-Leaderboard
paper:
  title: "JARVIS-Leaderboard: a large scale benchmark of materials design methods"
  venue: npj Computational Materials
  volume_article: 10, 93
  year: 2024
  url: https://www.nature.com/articles/s41524-024-01259-w
  preprint: https://arxiv.org/abs/2306.11688

benchmark:
  name: JARVIS-Leaderboard
  repo: https://github.com/usnistgov/jarvis_leaderboard
  repo_commit_pinned: 57afc55f94c8a6f4562f73a3173968cd4b2f83b1
  website: https://pages.nist.gov/jarvis_leaderboard/
  license: NIST license file in upstream repo
  domain: materials design benchmarks

task_under_audit:
  category: AI
  subcategory: SinglePropertyPrediction
  dataset: dft_3d
  property: formation_energy_peratom
  split: test
  metric: MAE
  benchmark_file: jarvis_leaderboard/benchmarks/AI/SinglePropertyPrediction/dft_3d_formation_energy_peratom.json.zip
  official_page: https://pages.nist.gov/jarvis_leaderboard/AI/SinglePropertyPrediction/dft_3d_formation_energy_peratom/

layer_a_seed_models:
  kgcnn_coGN: 0.0271
  alignn_model: 0.0331
  matminer_rf: 0.096

layer_a_expanded_tasks:
  total_benchmarks: 14
  regression_benchmarks: 6
  classification_benchmarks: 7
  spectra_benchmarks: 1
  total_submissions: 101
  all_match_official_rounding: true
  all_csv_ids_match_json_test_split: true
  classification_zip_internal_name_note: outer archives use test-acc.csv.zip but
    internal CSV names use test-mae.csv

layer_b_probe:
  status: bounded_pre_smoke_passed
  model_execution_smoke_run: true
  current_venv_missing:
    - jarvis
    - matminer
    - xgboost
    - lightgbm
  dependency_dry_run_succeeds: true
  isolated_env: env/jarvis
  smoke:
    script: scripts/jarvis_matminer_rf_smoke.py
    report: papers/jarvis-leaderboard/layer_b_matminer_rf_smoke.md
    benchmark: AI-SinglePropertyPrediction-formation_energy_peratom-dft_3d-test-mae
    train_rows: 1024
    test_rows: 256
    feature_columns: 273
    all_nan_feature_rows: 0
    trees: 100
    subset_mae: 0.26783845117187505
  recommended_next: scale matminer_rf smoke cautiously or stop at bounded Layer B

layer_c_resolution:
  status: point_gap_map_completed
  script: scripts/jarvis_resolution.py
  report: papers/jarvis-leaderboard/layer_c_resolution.md
  reports_checked: 14
  submissions_checked: 101
  adjacent_pairs: 87
  adjacent_gaps_le_0_001: 5
  adjacent_gaps_le_0_005: 29
  adjacent_gaps_le_0_010: 38

layer_c_bootstrap:
  status: paired_bootstrap_completed
  script: scripts/jarvis_bootstrap.py
  report: papers/jarvis-leaderboard/layer_c_bootstrap.md
  adjacent_pairs_checked: 20
  bootstrap_draws: 2000
  seed: 42
  ci_cross_zero: 17
  closest_pair:
    target: AI-SinglePropertyPrediction-formation_energy_peratom-dft_3d-test-mae
    pair: kgcnn_coNGN over potnet
    official_gap: 0.0002
    paired_advantage: 0.00016852
    ci_low: -0.00160975
    ci_high: 0.00156560
    p_tie_or_reversal: 0.4030

```


## 2. Reproduction plan

# Reproduction Plan - JARVIS-Leaderboard (Paper-002 candidate)

Status: Layer A passed for 14 selected JARVIS-Leaderboard AI benchmarks
(101 total submissions) on 2026-07-03. Layer B bounded `matminer_rf` pre-smoke
passed on a 1024 train / 256 test dft_3d slice. Layer C point-gap map and paired
bootstrap completed.

## 0. Why this candidate

JARVIS-Leaderboard is a strong Paper-002 candidate because its official benchmark
pages expose the exact artifacts needed for a CPU-only metric audit: submission CSV
zip, benchmark JSON zip, run script, and metadata for each contribution. That makes
it possible to repeat the same first move as Paper-001: recompute metrics from
published predictions before attempting any model execution.

## 1. Initial target

Benchmark:
`AI-SinglePropertyPrediction-formation_energy_peratom-dft_3d-test-mae`

Official page:
https://pages.nist.gov/jarvis_leaderboard/AI/SinglePropertyPrediction/dft_3d_formation_energy_peratom/

Seed submissions:

| model | official MAE | reason |
|---|---:|---|
| kgcnn_coGN | 0.0271 | top listed score for this page |
| alignn_model | 0.0331 | JARVIS/NIST baseline family |
| matminer_rf | 0.096 | simpler classical baseline |

## 2. Metric path

Upstream path in the pinned clone:
`vendor/jarvis_leaderboard/jarvis_leaderboard/rebuild.py::get_metric_value`.

For MAE tasks the upstream function:

1. reads the contribution CSV zip with `id,prediction`;
2. opens the benchmark JSON zip named `{dataset}_{property}.json.zip`;
3. selects the requested split (`test`);
4. merges on `id`;
5. computes `mean_absolute_error(actual, prediction)`;
6. rounds the displayed score to 4 decimals, except pages may show fewer trailing
   digits for some submissions.

`scripts/jarvis_score.py` mirrors this path with stdlib-only parsing.

## 3. Command

```bash
python scripts/run_command.py --paper jarvis-leaderboard \
  --note "paper002 layerA JARVIS formation energy seed models" -- \
  .venv/Scripts/python.exe scripts/jarvis_score.py \
    --vendor vendor/jarvis_leaderboard \
    --out papers/jarvis-leaderboard/metric_check.md
```

## 4. Pass criteria

- All selected CSV ids exactly match the JSON `test` split ids.
- Recomputed MAE matches the official page within the page's displayed rounding.
- Any mismatch becomes a blocker note before broadening to all submissions.

## 5. Current result

`scripts/jarvis_score.py --models all` recomputed MAE for all 15 listed submissions.
Every submission matched the official page within displayed rounding, and every CSV
id set exactly matched the JSON `test` split (5,572 rows).

The same Layer A path was then extended to 5 additional regression pages, 7
classification pages, and 1 spectra page. Aggregate: 101/101 submissions pass, with
exact CSV-vs-JSON test id agreement in every checked submission.

| benchmark property | submissions | test rows | report |
|---|---:|---:|---|
| formation_energy_peratom | 15 | 5,572 | `metric_check.md` |
| ehull | 11 | 5,537 | `metric_check-ehull.md` |
| optb88vdw_bandgap | 14 | 5,572 | `metric_check-optb88vdw_bandgap.md` |
| optb88vdw_total_energy | 14 | 5,572 | `metric_check-optb88vdw_total_energy.md` |
| bulk_modulus_kv | 12 | 1,968 | `metric_check-bulk_modulus_kv.md` |
| slme | 13 | 906 | `metric_check-slme.md` |

Classification pages:

| benchmark property | submissions | test rows | report |
|---|---:|---:|---|
| magmom_oszicar | 3 | 5,222 | `metric_check-class-magmom_oszicar.md` |
| mbj_bandgap | 3 | 1,815 | `metric_check-class-mbj_bandgap.md` |
| n_powerfact | 3 | 2,321 | `metric_check-class-n_powerfact.md` |
| optb88vdw_bandgap | 3 | 5,572 | `metric_check-class-optb88vdw_bandgap.md` |
| p_Seebeck | 3 | 2,321 | `metric_check-class-p_Seebeck.md` |
| slme | 3 | 906 | `metric_check-class-slme.md` |
| spillage | 3 | 1,137 | `metric_check-class-spillage.md` |

Spectra page:

| benchmark property | submissions | test rows | report |
|---|---:|---:|---|
| ph_dos / edos_pdos | 1 | 1,424 | `metric_check-spectra-ph_dos.md` |

Closest adjacent official gaps in the selected leaderboard are small:

- `kgcnn_coNGN` vs `potnet`: 0.0002 MAE
- `matformer_256` vs `alignn_model`: 0.0009 MAE
- `kgcnn_coGN` vs `kgcnn_coNGN`: 0.0020 MAE

The page reports point estimates only; uncertainty or split-sensitivity checks would
be the natural Layer C analogue.

## 6. Layer B execution-path probe

The first Layer B probe inspected the public contribution runners for
`matminer_rf`, `matminer_xgboost`, `cfid`, and `cfid_chem`, then checked dependency
availability in the current `.venv`.

Current `.venv` import probe:

- present: `sklearn`, `pymatgen`
- missing: `jarvis`, `matminer`, `xgboost`, `lightgbm`

Dependency resolution is feasible (`pip install --dry-run jarvis-tools matminer
xgboost lightgbm` exits 0), but installing those packages into the shared Paper-001
audit venv would broaden the environment materially. The public scripts also need
minor adaptation before they represent a clean dft_3d formation-energy smoke:
`matminer_rf` and `matminer_xgboost` are hardcoded to `snumat`, the XGBoost runner
uses `gpu_hist`, and the CFID runners assume a different benchmark path layout.

Details: `layer_b_probe.md`.

## 7. Layer B bounded pre-smoke

After the probe, an isolated JARVIS environment was created under ignored
`env/jarvis` and populated with `jarvis-tools` and `matminer`. A small wrapper,
`scripts/jarvis_matminer_rf_smoke.py`, executes the same broad path as the public
`matminer_rf` runner without mutating the shared Paper-001 venv.

Bounded smoke result:

| train rows | test rows | feature columns | all-NaN feature rows | RF trees | subset MAE | report |
|---:|---:|---:|---:|---:|---:|---|
| 1024 | 256 | 273 | 0 | 100 | 0.26783845 | `layer_b_matminer_rf_smoke.md` |

Scope note: this is not a full leaderboard reproduction and does not claim to
reproduce the official `matminer_rf` MAE. It proves the Layer B execution path can
load official JARVIS structures, compute Matminer features, train the RF baseline,
and emit a prediction CSV on a deterministic official-split subset.

## 8. Layer C point-gap map

`scripts/jarvis_resolution.py` parses the 14 Layer A reports and sorts each page by
its metric direction. This is not an uncertainty estimate; it is a map of adjacent
official point-estimate gaps.

Result:

| reports | submissions | adjacent pairs | gaps <= 0.001 | gaps <= 0.005 | gaps <= 0.010 | report |
|---:|---:|---:|---:|---:|---:|---|
| 14 | 101 | 87 | 5 | 29 | 38 | `layer_c_resolution.md` |

The closest adjacent pair is `kgcnn_coNGN` to `potnet` on dft_3d formation energy
(official MAE gap 0.0002; reproduced gap 0.00016852).

## 9. Layer C paired bootstrap

`scripts/jarvis_bootstrap.py` takes the 20 closest adjacent pairs from the point-gap
map and performs a paired nonparametric bootstrap over the fixed public test rows.
This is not a retraining uncertainty estimate and does not sample alternate splits.

Result:

| pairs | draws | seed | CIs crossing zero | report |
|---:|---:|---:|---:|---|
| 20 | 2000 | 42 | 17 | `layer_c_bootstrap.md` |

For the closest pair, `kgcnn_coNGN` over `potnet` on dft_3d formation energy, the
official MAE gap is 0.0002, the paired advantage is 0.00016852, the 95% CI is
[-0.00160975, 0.00156560], and P(tie/reversal) is 0.4030.

## 10. Next

1. Scale the `matminer_rf` smoke cautiously toward the full split only if feature
   runtime remains manageable.
2. If Paper-002 becomes the main target, package the JARVIS findings for external
   review.
3. If runtime becomes too broad, stop at Layer A + bounded Layer B + Layer C
   point-gap/bootstrap results.



## 3. Layer B execution-path probe

# Layer B Probe - JARVIS-Leaderboard

Date: 2026-07-03

Question: can one public JARVIS-Leaderboard contribution runner be executed as a
small model-execution smoke in the current ReproLab environment?

## Result

No model-execution smoke was run in the shared Matbench audit venv. The public
JARVIS contribution scripts are available, but the tractable baseline candidates
need extra dependencies and minor protocol adaptation before they can serve as a
clean Layer B smoke.

The dependency resolver itself is not blocked: `pip install --dry-run jarvis-tools
matminer xgboost lightgbm` succeeds. The blocker is practical isolation and script
fit, not package availability.

## Environment probe

Import check in the current `.venv`:

| module | status |
|---|---|
| sklearn | present (`1.9.0`) |
| pymatgen | present |
| jarvis | missing |
| matminer | missing |
| xgboost | missing |
| lightgbm | missing |

The dry-run install would add:

`jarvis-tools-2026.6.12`, `matminer-0.10.1`, `xgboost-3.2.0`,
`lightgbm-4.6.0`, plus dependency updates/additions including `pandas-2.3.3`,
`pymongo`, `dnspython`, `toolz`, `xmltodict`, and `pytz`.

Because Paper-001 already depends on this venv for traceability, the safer next
move is a separate JARVIS-specific env rather than mutating the existing one.

## Runner inspection

| candidate | inspected files | fit for immediate smoke |
|---|---|---|
| `matminer_rf` | `contributions/matminer_rf/run.py`, `run.bash` | Not immediate. It imports `jarvis` and `matminer`, then hardcodes `task = 'SinglePropertyPrediction'` and `for db in ['snumat']`. A dft_3d formation-energy smoke needs a small wrapper or patch. |
| `matminer_xgboost` | `contributions/matminer_xgboost/run.py`, `run.bash` | Not immediate. It adds `xgboost` and hardcodes `tree_method = 'gpu_hist'` plus the same `snumat` loop. A CPU smoke would need `hist` and the target dataset/property wired explicitly. |
| `cfid` | `contributions/cfid/run.py`, `run.sh` | Not immediate. It imports `lightgbm` and `jarvis`, iterates a broad property list, and expects benchmark zips under `../../dataset/AI/...` rather than the current sparse-checkout benchmark path. |
| `cfid_chem` | `contributions/cfid_chem/run.py`, `run_chem.py` | Not immediate. It also needs `lightgbm` and JARVIS CFID descriptors, writes full POSCAR directories, and is heavier than the desired first smoke. |

## Decision and follow-up

Treat this as a completed execution-path probe, not a failed reproduction. The
next productive Layer B move was:

1. create an isolated JARVIS env;
2. install only the dependencies for `matminer_rf`;
3. patch or wrap the runner so `db='dft_3d'` and
   `prop='formation_energy_peratom'` are explicit;
4. run a bounded CPU smoke on the official train/val/test split;
5. score the generated test CSV through `scripts/jarvis_score.py`.

If that proves too slow, stop Paper-002 at the current Layer A result and use the
Layer B probe as the documented reason.

Follow-up status: a bounded `matminer_rf`-style pre-smoke passed in `env/jarvis`.
See `layer_b_matminer_rf_smoke.md`.



## 4. Layer B bounded matminer_rf pre-smoke

# Layer B Pre-smoke - JARVIS matminer_rf

Target: `AI-SinglePropertyPrediction-formation_energy_peratom-dft_3d-test-mae`

Status: passed. This is a bounded CPU execution-path smoke, not a full
leaderboard reproduction and not a claim to reproduce the official
`matminer_rf` MAE.

## Result

- Train rows: 1024
- Test rows: 256
- Feature columns: 273
- All-NaN feature rows: 0
- Random forest trees: 100
- Subset MAE: 0.26783845
- Runtime seconds: 103.6
- Prediction CSV: `experiments\jarvis-leaderboard\matminer_rf_smoke1024\predictions.csv`

## Scope

- Uses the official benchmark train/test split, truncated deterministically
  to the first `--train-size` train ids and first `--test-size` test ids.
- Uses JARVIS `dft_3d` structures fetched by `jarvis-tools`.
- Uses the same broad Matminer feature family and RF hyperparameters as the
  public `matminer_rf` script, but does not run the full 55k-row test page.
- Intended to prove the Layer B execution path is viable in an isolated env.

## Sample ids

- First train id: `JVASP-21450`
- First test id: `JVASP-38636`



## 4b. Layer C point-gap map

# Leaderboard Resolution - JARVIS Layer A

This is a point-gap analysis of the 14 checked JARVIS-Leaderboard pages.
It is not an uncertainty estimate. It only asks how close adjacent official
point estimates are after sorting each page by its metric direction.

## Aggregate

- Reports checked: 14
- Submissions checked: 101
- Adjacent pairs: 87
- Adjacent gaps <= 0.001: 5
- Adjacent gaps <= 0.005: 29
- Adjacent gaps <= 0.010: 38

## Per-page Summary

| target | metric | models | adjacent pairs | min gap | median gap | gaps <= 0.001 | gaps <= 0.005 | closest pair |
|---|---|---:|---:|---:|---:|---:|---:|---|
| `SinglePropertyClass / magmom_oszicar / dft_3d` | ACC | 3 | 2 | 0.00080000 | 0.00195000 | 1 | 2 | matminer_rf to alignn_model |
| `SinglePropertyClass / mbj_bandgap / dft_3d` | ACC | 3 | 2 | 0.00710000 | 0.00850000 | 0 | 0 | matminer_xgboost to matminer_rf |
| `SinglePropertyClass / n_powerfact / dft_3d` | ACC | 3 | 2 | 0.01210000 | 0.01445000 | 0 | 0 | matminer_xgboost to matminer_rf |
| `SinglePropertyClass / optb88vdw_bandgap / dft_3d` | ACC | 3 | 2 | 0.00090000 | 0.00215000 | 1 | 2 | alignn_model to matminer_rf |
| `SinglePropertyClass / p_Seebeck / dft_3d` | ACC | 3 | 2 | 0.00220000 | 0.00475000 | 0 | 1 | alignn_model to matminer_rf |
| `SinglePropertyClass / slme / dft_3d` | ACC | 3 | 2 | 0.00110000 | 0.00555000 | 0 | 1 | matminer_rf to matminer_xgboost |
| `SinglePropertyClass / spillage / dft_3d` | ACC | 3 | 2 | 0.00530000 | 0.01145000 | 0 | 0 | matminer_xgboost to matminer_rf |
| `SinglePropertyPrediction / bulk_modulus_kv / dft_3d` | MAE | 12 | 11 | 0.08910000 | 0.41390000 | 0 | 0 | matminer_rf to cfid |
| `SinglePropertyPrediction / ehull / dft_3d` | MAE | 11 | 10 | 0.00110000 | 0.00765000 | 0 | 5 | kgcnn_cgcnn to matminer_xgboost |
| `SinglePropertyPrediction / formation_energy_peratom / dft_3d` | MAE | 15 | 14 | 0.00020000 | 0.00605000 | 2 | 6 | kgcnn_coNGN to potnet |
| `SinglePropertyPrediction / optb88vdw_bandgap / dft_3d` | MAE | 14 | 13 | 0.00130000 | 0.01130000 | 0 | 6 | matminer_rf to cgcnn_model |
| `SinglePropertyPrediction / optb88vdw_total_energy / dft_3d` | MAE | 14 | 13 | 0.00070000 | 0.00740000 | 1 | 6 | alignn_model to kgcnn_schnet |
| `SinglePropertyPrediction / slme / dft_3d` | MAE | 13 | 12 | 0.00790000 | 0.09520000 | 0 | 0 | kgcnn_coNGN to kgcnn_coGN |
| `Spectra / ph_dos / edos_pdos` | MULTIMAE | 1 | 0 | n/a | n/a | 0 | 0 | n/a |

## Closest Adjacent Pairs

| rank | target | metric | pair | official gap | reproduced gap |
|---:|---|---|---|---:|---:|
| 1 | `SinglePropertyPrediction / formation_energy_peratom / dft_3d` | MAE | kgcnn_coNGN to potnet | 0.00020000 | 0.00016852 |
| 2 | `SinglePropertyPrediction / optb88vdw_total_energy / dft_3d` | MAE | alignn_model to kgcnn_schnet | 0.00070000 | 0.00068863 |
| 3 | `SinglePropertyClass / magmom_oszicar / dft_3d` | ACC | matminer_rf to alignn_model | 0.00080000 | 0.00076599 |
| 4 | `SinglePropertyPrediction / formation_energy_peratom / dft_3d` | MAE | matformer_256 to alignn_model | 0.00090000 | 0.00093247 |
| 5 | `SinglePropertyClass / optb88vdw_bandgap / dft_3d` | ACC | alignn_model to matminer_rf | 0.00090000 | 0.00089734 |
| 6 | `SinglePropertyClass / slme / dft_3d` | ACC | matminer_rf to matminer_xgboost | 0.00110000 | 0.00110376 |
| 7 | `SinglePropertyPrediction / optb88vdw_total_energy / dft_3d` | MAE | kgcnn_coGN to kgcnn_coNGN | 0.00110000 | 0.00111477 |
| 8 | `SinglePropertyPrediction / ehull / dft_3d` | MAE | kgcnn_cgcnn to matminer_xgboost | 0.00110000 | 0.00107190 |
| 9 | `SinglePropertyPrediction / optb88vdw_bandgap / dft_3d` | MAE | matminer_rf to cgcnn_model | 0.00130000 | 0.00136523 |
| 10 | `SinglePropertyPrediction / optb88vdw_bandgap / dft_3d` | MAE | kgcnn_cgcnn to matminer_xgboost | 0.00160000 | 0.00158356 |
| 11 | `SinglePropertyPrediction / ehull / dft_3d` | MAE | kgcnn_coGN to kgcnn_coNGN | 0.00190000 | 0.00191120 |
| 12 | `SinglePropertyPrediction / optb88vdw_total_energy / dft_3d` | MAE | kgcnn_schnet to kgcnn_megnet | 0.00190000 | 0.00190516 |
| 13 | `SinglePropertyPrediction / formation_energy_peratom / dft_3d` | MAE | kgcnn_coGN to kgcnn_coNGN | 0.00200000 | 0.00198041 |
| 14 | `SinglePropertyPrediction / ehull / dft_3d` | MAE | kgcnn_megnet to kgcnn_cgcnn | 0.00210000 | 0.00210703 |
| 15 | `SinglePropertyPrediction / optb88vdw_bandgap / dft_3d` | MAE | potnet to kgcnn_coNGN | 0.00210000 | 0.00205852 |
| 16 | `SinglePropertyClass / p_Seebeck / dft_3d` | ACC | alignn_model to matminer_rf | 0.00220000 | 0.00215424 |
| 17 | `SinglePropertyPrediction / optb88vdw_bandgap / dft_3d` | MAE | matminer_xgboost to matminer_rf | 0.00220000 | 0.00213012 |
| 18 | `SinglePropertyPrediction / formation_energy_peratom / dft_3d` | MAE | kgcnn_dimenetPP to kgcnn_cgcnn | 0.00230000 | 0.00226462 |
| 19 | `SinglePropertyPrediction / optb88vdw_bandgap / dft_3d` | MAE | kgcnn_coGN to potnet | 0.00270000 | 0.00274676 |
| 20 | `SinglePropertyPrediction / formation_energy_peratom / dft_3d` | MAE | potnet to matformer_256 | 0.00290000 | 0.00292089 |

## Interpretation

The checked pages contain many adjacent point estimates below 0.005 in metric
units. Those small gaps are the natural targets for a later uncertainty,
split-sensitivity, or bootstrap-style analysis. Layer A already established
that these point estimates are internally reproducible from public artifacts.



## 4c. Layer C paired bootstrap

# Layer C Bootstrap - JARVIS Close Adjacent Pairs

This is a paired, nonparametric bootstrap over fixed public test rows for
the closest adjacent pairs identified by `layer_c_resolution.md`.

It is not a retraining uncertainty estimate and does not sample alternate
train/validation/test splits. It only tests whether the observed paired
test-row advantage of the official higher-ranked model is stable under
resampling of the published test set.

## Settings

- Bootstrap draws: 2000
- Seed: 42
- Pairs checked: 20

## Results

| rank | target | metric | official pair | rows | official gap | paired advantage | 95% CI | P(tie/reversal) |
|---:|---|---|---|---:|---:|---:|---:|---:|
| 1 | `SinglePropertyPrediction / formation_energy_peratom / dft_3d` | MAE | kgcnn_coNGN over potnet | 5572 | 0.00020000 | 0.00016852 | [-0.00160975, 0.00156560] | 0.4030 |
| 2 | `SinglePropertyPrediction / optb88vdw_total_energy / dft_3d` | MAE | alignn_model over kgcnn_schnet | 5572 | 0.00070000 | 0.00068863 | [-0.00285602, 0.00462995] | 0.3635 |
| 3 | `SinglePropertyClass / magmom_oszicar / dft_3d` | ACC | matminer_rf over alignn_model | 5222 | 0.00080000 | 0.00076599 | [-0.00555343, 0.00746840] | 0.4245 |
| 4 | `SinglePropertyPrediction / formation_energy_peratom / dft_3d` | MAE | matformer_256 over alignn_model | 5572 | 0.00090000 | 0.00093247 | [-0.00016749, 0.00204791] | 0.0470 |
| 5 | `SinglePropertyClass / optb88vdw_bandgap / dft_3d` | ACC | alignn_model over matminer_rf | 5572 | 0.00090000 | 0.00089734 | [-0.00574300, 0.00789663] | 0.3940 |
| 6 | `SinglePropertyClass / slme / dft_3d` | ACC | matminer_rf over matminer_xgboost | 906 | 0.00110000 | 0.00110375 | [-0.01545254, 0.01876380] | 0.4555 |
| 7 | `SinglePropertyPrediction / optb88vdw_total_energy / dft_3d` | MAE | kgcnn_coGN over kgcnn_coNGN | 5572 | 0.00110000 | 0.00111477 | [-0.00006757, 0.00254979] | 0.0390 |
| 8 | `SinglePropertyPrediction / ehull / dft_3d` | MAE | kgcnn_cgcnn over matminer_xgboost | 5537 | 0.00110000 | 0.00107191 | [-0.00321573, 0.00501498] | 0.3075 |
| 9 | `SinglePropertyPrediction / optb88vdw_bandgap / dft_3d` | MAE | matminer_rf over cgcnn_model | 5572 | 0.00130000 | 0.00136523 | [-0.00857241, 0.01167811] | 0.4240 |
| 10 | `SinglePropertyPrediction / optb88vdw_bandgap / dft_3d` | MAE | kgcnn_cgcnn over matminer_xgboost | 5572 | 0.00160000 | 0.00158357 | [-0.00966971, 0.01293096] | 0.3860 |
| 11 | `SinglePropertyPrediction / ehull / dft_3d` | MAE | kgcnn_coGN over kgcnn_coNGN | 5537 | 0.00190000 | 0.00191120 | [-0.00189713, 0.00609254] | 0.1655 |
| 12 | `SinglePropertyPrediction / optb88vdw_total_energy / dft_3d` | MAE | kgcnn_schnet over kgcnn_megnet | 5572 | 0.00190000 | 0.00190516 | [0.00046759, 0.00331262] | 0.0050 |
| 13 | `SinglePropertyPrediction / formation_energy_peratom / dft_3d` | MAE | kgcnn_coGN over kgcnn_coNGN | 5572 | 0.00200000 | 0.00198041 | [0.00073827, 0.00336273] | 0.0000 |
| 14 | `SinglePropertyPrediction / ehull / dft_3d` | MAE | kgcnn_megnet over kgcnn_cgcnn | 5537 | 0.00210000 | 0.00210703 | [-0.00182812, 0.00635259] | 0.1545 |
| 15 | `SinglePropertyPrediction / optb88vdw_bandgap / dft_3d` | MAE | potnet over kgcnn_coNGN | 5572 | 0.00210000 | 0.00205851 | [-0.00626258, 0.01019696] | 0.3120 |
| 16 | `SinglePropertyClass / p_Seebeck / dft_3d` | ACC | alignn_model over matminer_rf | 2321 | 0.00220000 | 0.00215424 | [-0.00904782, 0.01379793] | 0.3775 |
| 17 | `SinglePropertyPrediction / optb88vdw_bandgap / dft_3d` | MAE | matminer_xgboost over matminer_rf | 5572 | 0.00220000 | 0.00213012 | [-0.00256972, 0.00645132] | 0.1855 |
| 18 | `SinglePropertyPrediction / formation_energy_peratom / dft_3d` | MAE | kgcnn_dimenetPP over kgcnn_cgcnn | 5572 | 0.00230000 | 0.00226462 | [-0.00414618, 0.00743016] | 0.2270 |
| 19 | `SinglePropertyPrediction / optb88vdw_bandgap / dft_3d` | MAE | kgcnn_coGN over potnet | 5572 | 0.00270000 | 0.00274677 | [-0.00438651, 0.01058822] | 0.2325 |
| 20 | `SinglePropertyPrediction / formation_energy_peratom / dft_3d` | MAE | potnet over matformer_256 | 5572 | 0.00290000 | 0.00292089 | [0.00205824, 0.00384399] | 0.0000 |

## Interpretation

- Pairs whose 95% CI includes zero: 17 / 20
- `paired advantage` is positive when the official higher-ranked model has
  the better metric on the resampled test set.
- For MAE/MULTIMAE, advantage is mean(error_lower-ranked - error_higher-ranked).
- For ACC, advantage is mean(correct_higher-ranked - correct_lower-ranked).
- A high `P(tie/reversal)` means the official adjacent ordering is fragile
  under this fixed-test-set bootstrap.

Pairs with CI crossing zero:

| target | metric | pair | 95% CI | P(tie/reversal) |
|---|---|---|---:|---:|
| `SinglePropertyPrediction / formation_energy_peratom / dft_3d` | MAE | kgcnn_coNGN over potnet | [-0.00160975, 0.00156560] | 0.4030 |
| `SinglePropertyPrediction / optb88vdw_total_energy / dft_3d` | MAE | alignn_model over kgcnn_schnet | [-0.00285602, 0.00462995] | 0.3635 |
| `SinglePropertyClass / magmom_oszicar / dft_3d` | ACC | matminer_rf over alignn_model | [-0.00555343, 0.00746840] | 0.4245 |
| `SinglePropertyPrediction / formation_energy_peratom / dft_3d` | MAE | matformer_256 over alignn_model | [-0.00016749, 0.00204791] | 0.0470 |
| `SinglePropertyClass / optb88vdw_bandgap / dft_3d` | ACC | alignn_model over matminer_rf | [-0.00574300, 0.00789663] | 0.3940 |
| `SinglePropertyClass / slme / dft_3d` | ACC | matminer_rf over matminer_xgboost | [-0.01545254, 0.01876380] | 0.4555 |
| `SinglePropertyPrediction / optb88vdw_total_energy / dft_3d` | MAE | kgcnn_coGN over kgcnn_coNGN | [-0.00006757, 0.00254979] | 0.0390 |
| `SinglePropertyPrediction / ehull / dft_3d` | MAE | kgcnn_cgcnn over matminer_xgboost | [-0.00321573, 0.00501498] | 0.3075 |
| `SinglePropertyPrediction / optb88vdw_bandgap / dft_3d` | MAE | matminer_rf over cgcnn_model | [-0.00857241, 0.01167811] | 0.4240 |
| `SinglePropertyPrediction / optb88vdw_bandgap / dft_3d` | MAE | kgcnn_cgcnn over matminer_xgboost | [-0.00966971, 0.01293096] | 0.3860 |
| `SinglePropertyPrediction / ehull / dft_3d` | MAE | kgcnn_coGN over kgcnn_coNGN | [-0.00189713, 0.00609254] | 0.1655 |
| `SinglePropertyPrediction / ehull / dft_3d` | MAE | kgcnn_megnet over kgcnn_cgcnn | [-0.00182812, 0.00635259] | 0.1545 |
| `SinglePropertyPrediction / optb88vdw_bandgap / dft_3d` | MAE | potnet over kgcnn_coNGN | [-0.00626258, 0.01019696] | 0.3120 |
| `SinglePropertyClass / p_Seebeck / dft_3d` | ACC | alignn_model over matminer_rf | [-0.00904782, 0.01379793] | 0.3775 |
| `SinglePropertyPrediction / optb88vdw_bandgap / dft_3d` | MAE | matminer_xgboost over matminer_rf | [-0.00256972, 0.00645132] | 0.1855 |
| `SinglePropertyPrediction / formation_energy_peratom / dft_3d` | MAE | kgcnn_dimenetPP over kgcnn_cgcnn | [-0.00414618, 0.00743016] | 0.2270 |
| `SinglePropertyPrediction / optb88vdw_bandgap / dft_3d` | MAE | kgcnn_coGN over potnet | [-0.00438651, 0.01058822] | 0.2325 |



## 5. Metric check - metric_check-bulk_modulus_kv

# Metric Check - JARVIS-Leaderboard Layer A

Target: `AI-SinglePropertyPrediction-bulk_modulus_kv-dft_3d-test-mae`
Vendor repo: `vendor/jarvis_leaderboard`
Ground-truth split sizes: {'train': 15744, 'val': 1968, 'test': 1968}

The score is recomputed from the public submission CSV zip and benchmark JSON zip artifacts. This mirrors the upstream `rebuild.py::get_metric_value` path for `mae` but uses a small stdlib-only implementation.
Models scored: 12

| model | team | official MAE | reproduced MAE | rows | id check | pass |
|---|---|---:|---:|---:|---|---|
| kgcnn_coNGN | kgcnn | 8.7022 | 8.70219322 | 1968 | exact | yes |
| kgcnn_coGN | kgcnn | 8.992 | 8.99203924 | 1968 | exact | yes |
| kgcnn_schnet | kgcnn | 10.7105 | 10.71047255 | 1968 | exact | yes |
| matminer_lgbm | Matminer | 15.4752 | 15.47517687 | 1968 | exact | yes |
| kgcnn_megnet | kgcnn | 11.4287 | 11.42867602 | 1968 | exact | yes |
| kgcnn_dimenetPP | kgcnn | 13.3743 | 13.37431796 | 1968 | exact | yes |
| cfid_chem | JARVIS | 15.5726 | 15.57257995 | 1968 | exact | yes |
| cfid | JARVIS | 14.1999 | 14.19994925 | 1968 | exact | yes |
| alignn_model | ALIGNN | 10.3988 | 10.39883748 | 1968 | exact | yes |
| matminer_rf | UofT | 14.1108 | 14.11083439 | 1968 | exact | yes |
| matminer_xgboost | UofT | 12.7411 | 12.74114673 | 1968 | exact | yes |
| kgcnn_cgcnn | kgcnn | 11.0148 | 11.01483561 | 1968 | exact | yes |

## Closest adjacent scores

The official page reports point estimates only; this table flags adjacent MAE gaps that may deserve uncertainty or sensitivity checks later.

| pair | official MAE gap | reproduced MAE gap |
|---|---:|---:|
| matminer_rf to cfid | 0.0891 | 0.08911486 |
| matminer_lgbm to cfid_chem | 0.0974 | 0.09740308 |
| kgcnn_coNGN to kgcnn_coGN | 0.2898 | 0.28984601 |
| kgcnn_schnet to kgcnn_cgcnn | 0.3043 | 0.30436306 |
| alignn_model to kgcnn_schnet | 0.3117 | 0.31163507 |

## Scope

- Layer A only: metric recomputation from already-published artifacts.
- No model training or model execution yet.
- The target was chosen because the official page exposes CSV predictions, JSON ground truth, run scripts, and metadata.

## Next

Next, decide whether to broaden across more JARVIS tasks or attempt one Layer B model-execution smoke for a tractable baseline.



## 5. Metric check - metric_check-class-magmom_oszicar

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



## 5. Metric check - metric_check-class-mbj_bandgap

# Metric Check - JARVIS-Leaderboard Layer A

Target: `AI-SinglePropertyClass-mbj_bandgap-dft_3d-test-acc`
Vendor repo: `vendor/jarvis_leaderboard`
Ground-truth split sizes: {'train': 14535, 'val': 1817, 'test': 1815}

The score is recomputed from the public submission CSV zip and benchmark JSON zip artifacts. This mirrors the upstream `rebuild.py::get_metric_value` path for `acc` but uses a small stdlib-only implementation.
Models scored: 3

| model | team | official ACC | reproduced ACC | rows | id check | pass |
|---|---|---:|---:|---:|---|---|
| alignn_model | ALIGNN | 0.9229 | 0.92286501 | 1815 | exact | yes |
| matminer_rf | UofT | 0.9328 | 0.93278237 | 1815 | exact | yes |
| matminer_xgboost | UofT | 0.9399 | 0.93994490 | 1815 | exact | yes |

## Closest adjacent scores

The official page reports point estimates only; this table flags adjacent ACC gaps that may deserve uncertainty or sensitivity checks later.

| pair | official ACC gap | reproduced ACC gap |
|---|---:|---:|
| matminer_rf to matminer_xgboost | 0.0071 | 0.00716253 |
| alignn_model to matminer_rf | 0.0099 | 0.00991736 |

## Scope

- Layer A only: metric recomputation from already-published artifacts.
- No model training or model execution yet.
- The target was chosen because the official page exposes CSV predictions, JSON ground truth, run scripts, and metadata.

## Next

Next, decide whether to broaden across more JARVIS tasks or attempt one Layer B model-execution smoke for a tractable baseline.



## 5. Metric check - metric_check-class-n_powerfact

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



## 5. Metric check - metric_check-class-optb88vdw_bandgap

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



## 5. Metric check - metric_check-class-p_Seebeck

# Metric Check - JARVIS-Leaderboard Layer A

Target: `AI-SinglePropertyClass-p_Seebeck-dft_3d-test-acc`
Vendor repo: `vendor/jarvis_leaderboard`
Ground-truth split sizes: {'train': 18568, 'val': 2321, 'test': 2321}

The score is recomputed from the public submission CSV zip and benchmark JSON zip artifacts. This mirrors the upstream `rebuild.py::get_metric_value` path for `acc` but uses a small stdlib-only implementation.
Models scored: 3

| model | team | official ACC | reproduced ACC | rows | id check | pass |
|---|---|---:|---:|---:|---|---|
| alignn_model | ALIGNN | 0.9259 | 0.92589401 | 2321 | exact | yes |
| matminer_rf | UofT | 0.9237 | 0.92373977 | 2321 | exact | yes |
| matminer_xgboost | UofT | 0.9332 | 0.93321844 | 2321 | exact | yes |

## Closest adjacent scores

The official page reports point estimates only; this table flags adjacent ACC gaps that may deserve uncertainty or sensitivity checks later.

| pair | official ACC gap | reproduced ACC gap |
|---|---:|---:|
| matminer_rf to alignn_model | 0.0022 | 0.00215424 |
| alignn_model to matminer_xgboost | 0.0073 | 0.00732443 |

## Scope

- Layer A only: metric recomputation from already-published artifacts.
- No model training or model execution yet.
- The target was chosen because the official page exposes CSV predictions, JSON ground truth, run scripts, and metadata.

## Next

Next, decide whether to broaden across more JARVIS tasks or attempt one Layer B model-execution smoke for a tractable baseline.



## 5. Metric check - metric_check-class-slme

# Metric Check - JARVIS-Leaderboard Layer A

Target: `AI-SinglePropertyClass-slme-dft_3d-test-acc`
Vendor repo: `vendor/jarvis_leaderboard`
Ground-truth split sizes: {'train': 7250, 'val': 906, 'test': 906}

The score is recomputed from the public submission CSV zip and benchmark JSON zip artifacts. This mirrors the upstream `rebuild.py::get_metric_value` path for `acc` but uses a small stdlib-only implementation.
Models scored: 3

| model | team | official ACC | reproduced ACC | rows | id check | pass |
|---|---|---:|---:|---:|---|---|
| alignn_model | ALIGNN | 0.8311 | 0.83112583 | 906 | exact | yes |
| matminer_rf | UofT | 0.8422 | 0.84216336 | 906 | exact | yes |
| matminer_xgboost | UofT | 0.8411 | 0.84105960 | 906 | exact | yes |

## Closest adjacent scores

The official page reports point estimates only; this table flags adjacent ACC gaps that may deserve uncertainty or sensitivity checks later.

| pair | official ACC gap | reproduced ACC gap |
|---|---:|---:|
| matminer_xgboost to matminer_rf | 0.0011 | 0.00110375 |
| alignn_model to matminer_xgboost | 0.0100 | 0.00993377 |

## Scope

- Layer A only: metric recomputation from already-published artifacts.
- No model training or model execution yet.
- The target was chosen because the official page exposes CSV predictions, JSON ground truth, run scripts, and metadata.

## Next

Next, decide whether to broaden across more JARVIS tasks or attempt one Layer B model-execution smoke for a tractable baseline.



## 5. Metric check - metric_check-class-spillage

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



## 5. Metric check - metric_check-ehull

# Metric Check - JARVIS-Leaderboard Layer A

Target: `AI-SinglePropertyPrediction-ehull-dft_3d-test-mae`
Vendor repo: `vendor/jarvis_leaderboard`
Ground-truth split sizes: {'train': 44290, 'val': 5537, 'test': 5537}

The score is recomputed from the public submission CSV zip and benchmark JSON zip artifacts. This mirrors the upstream `rebuild.py::get_metric_value` path for `mae` but uses a small stdlib-only implementation.
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



## 5. Metric check - metric_check-optb88vdw_bandgap

# Metric Check - JARVIS-Leaderboard Layer A

Target: `AI-SinglePropertyPrediction-optb88vdw_bandgap-dft_3d-test-mae`
Vendor repo: `vendor/jarvis_leaderboard`
Ground-truth split sizes: {'train': 44569, 'val': 5572, 'test': 5572}

The score is recomputed from the public submission CSV zip and benchmark JSON zip artifacts. This mirrors the upstream `rebuild.py::get_metric_value` path for `mae` but uses a small stdlib-only implementation.
Models scored: 14

| model | team | official MAE | reproduced MAE | rows | id check | pass |
|---|---|---:|---:|---:|---|---|
| kgcnn_coNGN | kgcnn | 0.1267 | 0.12669279 | 5572 | exact | yes |
| kgcnn_coGN | kgcnn | 0.1219 | 0.12188751 | 5572 | exact | yes |
| cgcnn_model | CGCNN | 0.1908 | 0.19082040 | 5572 | exact | yes |
| potnet | DIVE@TAMU | 0.1246 | 0.12463427 | 5572 | exact | yes |
| kgcnn_schnet | kgcnn | 0.698 | 0.69798998 | 5572 | exact | yes |
| matminer_lgbm | Matminer | 0.2021 | 0.20208063 | 5572 | exact | yes |
| kgcnn_megnet | kgcnn | 0.146 | 0.14604425 | 5572 | exact | yes |
| kgcnn_dimenetPP | kgcnn | 0.2247 | 0.22467448 | 5572 | exact | yes |
| cfid_chem | JARVIS | 0.4057 | 0.40568531 | 5572 | exact | yes |
| cfid | JARVIS | 0.299 | 0.29904368 | 5572 | exact | yes |
| alignn_model | ALIGNN | 0.1423 | 0.14232787 | 5572 | exact | yes |
| matminer_rf | UofT | 0.1895 | 0.18945517 | 5572 | exact | yes |
| matminer_xgboost | UofT | 0.1873 | 0.18732505 | 5572 | exact | yes |
| kgcnn_cgcnn | kgcnn | 0.1857 | 0.18574149 | 5572 | exact | yes |

## Closest adjacent scores

The official page reports point estimates only; this table flags adjacent MAE gaps that may deserve uncertainty or sensitivity checks later.

| pair | official MAE gap | reproduced MAE gap |
|---|---:|---:|
| matminer_rf to cgcnn_model | 0.0013 | 0.00136523 |
| kgcnn_cgcnn to matminer_xgboost | 0.0016 | 0.00158357 |
| potnet to kgcnn_coNGN | 0.0021 | 0.00205851 |
| matminer_xgboost to matminer_rf | 0.0022 | 0.00213012 |
| kgcnn_coGN to potnet | 0.0027 | 0.00274677 |

## Scope

- Layer A only: metric recomputation from already-published artifacts.
- No model training or model execution yet.
- The target was chosen because the official page exposes CSV predictions, JSON ground truth, run scripts, and metadata.

## Next

Next, decide whether to broaden across more JARVIS tasks or attempt one Layer B model-execution smoke for a tractable baseline.



## 5. Metric check - metric_check-optb88vdw_total_energy

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



## 5. Metric check - metric_check-slme

# Metric Check - JARVIS-Leaderboard Layer A

Target: `AI-SinglePropertyPrediction-slme-dft_3d-test-mae`
Vendor repo: `vendor/jarvis_leaderboard`
Ground-truth split sizes: {'train': 7250, 'val': 906, 'test': 906}

The score is recomputed from the public submission CSV zip and benchmark JSON zip artifacts. This mirrors the upstream `rebuild.py::get_metric_value` path for `mae` but uses a small stdlib-only implementation.
Models scored: 13

| model | team | official MAE | reproduced MAE | rows | id check | pass |
|---|---|---:|---:|---:|---|---|
| kgcnn_coNGN | kgcnn | 4.4428 | 4.44277482 | 906 | exact | yes |
| kgcnn_coGN | kgcnn | 4.4507 | 4.45069549 | 906 | exact | yes |
| cgcnn_model | CGCNN | 5.6603 | 5.66033686 | 906 | exact | yes |
| kgcnn_schnet | kgcnn | 5.3222 | 5.32216693 | 906 | exact | yes |
| matminer_lgbm | Matminer | 5.4242 | 5.42422043 | 906 | exact | yes |
| kgcnn_megnet | kgcnn | 5.0614 | 5.06136079 | 906 | exact | yes |
| kgcnn_dimenetPP | kgcnn | 5.6403 | 5.64029506 | 906 | exact | yes |
| cfid_chem | JARVIS | 6.5321 | 6.53214181 | 906 | exact | yes |
| cfid | JARVIS | 6.2607 | 6.26070041 | 906 | exact | yes |
| alignn_model | ALIGNN | 4.5207 | 4.52067485 | 906 | exact | yes |
| matminer_rf | UofT | 5.1235 | 5.12345466 | 906 | exact | yes |
| matminer_xgboost | UofT | 4.9255 | 4.92548902 | 906 | exact | yes |
| kgcnn_cgcnn | kgcnn | 5.0139 | 5.01394452 | 906 | exact | yes |

## Closest adjacent scores

The official page reports point estimates only; this table flags adjacent MAE gaps that may deserve uncertainty or sensitivity checks later.

| pair | official MAE gap | reproduced MAE gap |
|---|---:|---:|
| kgcnn_coNGN to kgcnn_coGN | 0.0079 | 0.00792067 |
| kgcnn_dimenetPP to cgcnn_model | 0.0200 | 0.02004180 |
| kgcnn_cgcnn to kgcnn_megnet | 0.0475 | 0.04741627 |
| kgcnn_megnet to matminer_rf | 0.0621 | 0.06209388 |
| kgcnn_coGN to alignn_model | 0.0700 | 0.06997936 |

## Scope

- Layer A only: metric recomputation from already-published artifacts.
- No model training or model execution yet.
- The target was chosen because the official page exposes CSV predictions, JSON ground truth, run scripts, and metadata.

## Next

Next, decide whether to broaden across more JARVIS tasks or attempt one Layer B model-execution smoke for a tractable baseline.



## 5. Metric check - metric_check-spectra-ph_dos

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



## 5. Metric check - metric_check

# Metric Check - JARVIS-Leaderboard Layer A

Target: `AI-SinglePropertyPrediction-formation_energy_peratom-dft_3d-test-mae`
Vendor repo: `vendor/jarvis_leaderboard`
Ground-truth split sizes: {'train': 44569, 'val': 5572, 'test': 5572}

The score is recomputed from the public submission CSV zip and benchmark JSON zip artifacts. This mirrors the upstream `rebuild.py::get_metric_value` path for `mae` but uses a small stdlib-only implementation.
Models scored: 15

| model | team | official MAE | reproduced MAE | rows | id check | pass |
|---|---|---:|---:|---:|---|---|
| kgcnn_coNGN | kgcnn | 0.0291 | 0.02909801 | 5572 | exact | yes |
| kgcnn_coGN | kgcnn | 0.0271 | 0.02711760 | 5572 | exact | yes |
| cgcnn_model | CGCNN | 0.0625 | 0.06250565 | 5572 | exact | yes |
| potnet | DIVE@TAMU | 0.0293 | 0.02926653 | 5572 | exact | yes |
| kgcnn_schnet | kgcnn | 0.0365 | 0.03649074 | 5572 | exact | yes |
| matminer_lgbm | Matminer | 0.1023 | 0.10231528 | 5572 | exact | yes |
| kgcnn_megnet | kgcnn | 0.0423 | 0.04229563 | 5572 | exact | yes |
| kgcnn_dimenetPP | kgcnn | 0.0528 | 0.05282269 | 5572 | exact | yes |
| cfid_chem | JARVIS | 0.2226 | 0.22264128 | 5572 | exact | yes |
| matformer_256 | DIVE@TAMU | 0.0322 | 0.03218742 | 5572 | exact | yes |
| cfid | JARVIS | 0.1419 | 0.14186013 | 5572 | exact | yes |
| alignn_model | ALIGNN | 0.0331 | 0.03311989 | 5572 | exact | yes |
| matminer_rf | UofT | 0.096 | 0.09595936 | 5572 | exact | yes |
| matminer_xgboost | UofT | 0.0734 | 0.07339676 | 5572 | exact | yes |
| kgcnn_cgcnn | kgcnn | 0.0551 | 0.05508731 | 5572 | exact | yes |

## Closest adjacent scores

The official page reports point estimates only; this table flags adjacent MAE gaps that may deserve uncertainty or sensitivity checks later.

| pair | official MAE gap | reproduced MAE gap |
|---|---:|---:|
| kgcnn_coNGN to potnet | 0.0002 | 0.00016852 |
| matformer_256 to alignn_model | 0.0009 | 0.00093247 |
| kgcnn_coGN to kgcnn_coNGN | 0.0020 | 0.00198041 |
| kgcnn_dimenetPP to kgcnn_cgcnn | 0.0023 | 0.00226462 |
| potnet to matformer_256 | 0.0029 | 0.00292089 |

## Scope

- Layer A only: metric recomputation from already-published artifacts.
- No model training or model execution yet.
- The target was chosen because the official page exposes CSV predictions, JSON ground truth, run scripts, and metadata.

## Next

Next, decide whether to broaden across more JARVIS tasks or attempt one Layer B model-execution smoke for a tractable baseline.



## 6. Run log (tail)


```

### 2026-07-03 07:14 UTC — paper002 bootstrap smoke top5

```
$ .venv\Scripts\python.exe scripts\jarvis_bootstrap.py --top 5 --draws 500 --seed 42 --out papers\jarvis-leaderboard\layer_c_bootstrap_top5_smoke.md
```

- exit code: **0**  | duration: 1.8s  | raw log: `logs/cmd-20260703-071434.log`

output tail:
```
{'pairs': 5, 'draws': 500, 'ci_cross_zero': 5, 'out': 'papers\\jarvis-leaderboard\\layer_c_bootstrap_top5_smoke.md'}
```

### 2026-07-03 07:14 UTC — paper002 bootstrap close adjacent pairs top20

```
$ .venv\Scripts\python.exe scripts\jarvis_bootstrap.py --top 20 --draws 2000 --seed 42 --out papers\jarvis-leaderboard\layer_c_bootstrap.md
```

- exit code: **0**  | duration: 2.1s  | raw log: `logs/cmd-20260703-071446.log`

output tail:
```
{'pairs': 20, 'draws': 2000, 'ci_cross_zero': 17, 'out': 'papers\\jarvis-leaderboard\\layer_c_bootstrap.md'}
```

### 2026-07-03 07:16 UTC — verify paper002 layerC bootstrap docs

```
$ .venv\Scripts\python.exe -c from pathlib import Path; import yaml; meta=yaml.safe_load(Path('papers/jarvis-leaderboard/metadata.yaml').read_text(encoding='utf-8')); summary=Path('papers/jarvis-leaderboard/summary.md').read_text(encoding='utf-8'); plan=Path('papers/jarvis-leaderboard/reproduction_plan.md').read_text(encoding='utf-8'); readme=Path('README.md').read_text(encoding='utf-8'); bootstrap=Path('papers/jarvis-leaderboard/layer_c_bootstrap.md').read_text(encoding='utf-8'); script=Path('scripts/jarvis_bootstrap.py').read_text(encoding='utf-8'); layer=meta['layer_c_bootstrap']; checks=[layer['adjacent_pairs_checked']==20,layer['bootstrap_draws']==2000,layer['ci_cross_zero']==17,'17/20 closest adjacent-pair 95% CIs include zero' in summary,'Layer C paired bootstrap' in plan,'17/20 95% CIs' in readme,'kgcnn_coNGN over potnet' in bootstrap,'paired_advantages' in script,not Path('papers/jarvis-leaderboard/layer_c_bootstrap_top5_smoke.md').exists()]; print({'layer_c_bootstrap': layer, 'checks': checks}); raise SystemExit(0 if all(checks) else 1)
```

- exit code: **0**  | duration: 0.1s  | raw log: `logs/cmd-20260703-071621.log`

output tail:
```
{'layer_c_bootstrap': {'status': 'paired_bootstrap_completed', 'script': 'scripts/jarvis_bootstrap.py', 'report': 'papers/jarvis-leaderboard/layer_c_bootstrap.md', 'adjacent_pairs_checked': 20, 'bootstrap_draws': 2000, 'seed': 42, 'ci_cross_zero': 17, 'closest_pair': {'target': 'AI-SinglePropertyPrediction-formation_energy_peratom-dft_3d-test-mae', 'pair': 'kgcnn_coNGN over potnet', 'official_gap': 0.0002, 'paired_advantage': 0.00016852, 'ci_low': -0.00160975, 'ci_high': 0.0015656, 'p_tie_or_reversal': 0.403}}, 'checks': [True, True, True, True, True, True, True, True, True]}
```

### 2026-07-03 07:16 UTC — reassemble Paper-002 report after bootstrap

```
$ .venv\Scripts\python.exe scripts\make_jarvis_report.py
```

- exit code: **0**  | duration: 0.2s  | raw log: `logs/cmd-20260703-071638.log`

output tail:
```
wrote C:\Users\07013\Desktop\0702fable\reprolab\reports\paper-002-jarvis-leaderboard-audit.md
```

### 2026-07-03 07:16 UTC — verify Paper-002 assembled report after bootstrap

```
$ .venv\Scripts\python.exe -c from pathlib import Path; report=Path('reports/paper-002-jarvis-leaderboard-audit.md').read_text(encoding='utf-8'); readme=Path('README.md').read_text(encoding='utf-8'); checks=['4c. Layer C paired bootstrap' in report,'17/20 closest adjacent-pair 95% CIs include zero' in report,'kgcnn_coNGN over potnet' in report,'layer_c_bootstrap.md' in readme,'scripts/jarvis_bootstrap.py' in readme,not Path('papers/jarvis-leaderboard/layer_c_bootstrap_top5_smoke.md').exists()]; print({'report_lines': len(report.splitlines()), 'checks': checks}); raise SystemExit(0 if all(checks) else 1)
```

- exit code: **0**  | duration: 0.1s  | raw log: `logs/cmd-20260703-071656.log`

output tail:
```
{'report_lines': 1394, 'checks': [True, True, True, True, True, True]}
```

### 2026-07-03 07:17 UTC — verify Paper-002 external packet

```
$ .venv\Scripts\python.exe -c from pathlib import Path; packet=Path('reports/paper-002-external_release_packet.md').read_text(encoding='utf-8'); readme=Path('README.md').read_text(encoding='utf-8'); one=Path('reports/one_page_summary.md').read_text(encoding='utf-8'); checks=['101/101 checked submissions' in packet,'17/20 95% CIs' in packet,'Claims to avoid' in packet,'kgcnn_coNGN' in packet,'paper-002-external_release_packet.md' in readme,'paper-002-external_release_packet.md' in one]; print({'packet_lines': len(packet.splitlines()), 'checks': checks}); raise SystemExit(0 if all(checks) else 1)
```

- exit code: **0**  | duration: 0.1s  | raw log: `logs/cmd-20260703-071754.log`

output tail:
```
{'packet_lines': 112, 'checks': [True, True, True, True, True, True]}
```

### 2026-07-03 07:18 UTC — paper002 matminer_rf scaled pre-smoke 1024x256

```
$ env\jarvis\Scripts\python.exe scripts\jarvis_matminer_rf_smoke.py --train-size 1024 --test-size 256 --trees 100 --pred-out experiments\jarvis-leaderboard\matminer_rf_smoke1024\predictions.csv --out papers\jarvis-leaderboard\layer_b_matminer_rf_smoke1024.md
```

- exit code: **0**  | duration: 106.8s  | raw log: `logs/cmd-20260703-071828.log`

output tail:
```
Loading the zipfile...
Loading completed.
{
  "all_nan_feature_rows": 0,
  "benchmark": "AI-SinglePropertyPrediction-formation_energy_peratom-dft_3d-test-mae",
  "feature_columns": 273,
  "first_test_id": "JVASP-38636",
  "first_train_id": "JVASP-21450",
  "mae": 0.26783845117187505,
  "pred_out": "experiments\\jarvis-leaderboard\\matminer_rf_smoke1024\\predictions.csv",
  "seconds": 103.64893198013306,
  "test_rows": 256,
  "train_rows": 1024,
  "trees": 100
}
```

### 2026-07-03 07:20 UTC — verify paper002 matminer_rf 1024x256 docs

```
$ .venv\Scripts\python.exe -c from pathlib import Path; import yaml; meta=yaml.safe_load(Path('papers/jarvis-leaderboard/metadata.yaml').read_text(encoding='utf-8')); report=Path('papers/jarvis-leaderboard/layer_b_matminer_rf_smoke.md').read_text(encoding='utf-8'); summary=Path('papers/jarvis-leaderboard/summary.md').read_text(encoding='utf-8'); plan=Path('papers/jarvis-leaderboard/reproduction_plan.md').read_text(encoding='utf-8'); readme=Path('README.md').read_text(encoding='utf-8'); packet=Path('reports/paper-002-external_release_packet.md').read_text(encoding='utf-8'); smoke=meta['layer_b_probe']['smoke']; checks=[smoke['train_rows']==1024,smoke['test_rows']==256,smoke['feature_columns']==273,smoke['all_nan_feature_rows']==0,abs(smoke['subset_mae']-0.26783845117187505)<1e-15,'1024' in report,'0.26783845' in report,'1024 train / 256 test' in readme,'1024 train rows, 256 test rows' in summary,'1024 | 256' in plan,'1024 train / 256 test' in packet,not Path('papers/jarvis-leaderboard/layer_b_matminer_rf_smoke1024.md').exists()]; print({'smoke': smoke, 'checks': checks}); raise SystemExit(0 if all(checks) else 1)
```

- exit code: **0**  | duration: 0.1s  | raw log: `logs/cmd-20260703-072050.log`

output tail:
```
{'smoke': {'script': 'scripts/jarvis_matminer_rf_smoke.py', 'report': 'papers/jarvis-leaderboard/layer_b_matminer_rf_smoke.md', 'benchmark': 'AI-SinglePropertyPrediction-formation_energy_peratom-dft_3d-test-mae', 'train_rows': 1024, 'test_rows': 256, 'feature_columns': 273, 'all_nan_feature_rows': 0, 'trees': 100, 'subset_mae': 0.26783845117187505}, 'checks': [True, True, True, True, True, True, True, True, True, True, True, True]}
```

