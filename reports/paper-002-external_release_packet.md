# External Release Packet - Paper-002 JARVIS-Leaderboard Audit

Date: 2026-07-03
Repo: https://github.com/maruyamakoju/reprolab
Audit target: https://github.com/usnistgov/jarvis_leaderboard at commit
`57afc55f94c8a6f4562f73a3173968cd4b2f83b1`

This packet is the short handoff for maintainers, reviewers, or collaborators who
need the JARVIS result without reading the full assembled report first.

## Bottom line

The checked JARVIS-Leaderboard public artifacts are internally reproducible, but
many adjacent leaderboard point estimates are not stable under a fixed-test-set
bootstrap.

- **Layer A:** 14 JARVIS-Leaderboard AI pages checked across regression,
  classification, and spectra tasks. All 101/101 submissions reproduce the official
  MAE/ACC/MULTIMAE within displayed rounding, and every checked CSV id set exactly
  matches the corresponding JSON test split.
- **Layer B:** public baseline runners exist, but they are heterogeneous and not
  one-command fits for the audited dft_3d target. In an isolated JARVIS env, a
  bounded `matminer_rf`-style CPU execution-path smoke passed on a deterministic
  512 train / 128 test dft_3d formation-energy slice.
- **Layer C:** across the 14 checked pages, 29/87 adjacent official point gaps are
  <=0.005 and 38/87 are <=0.010 in metric units. For the 20 closest adjacent pairs,
  paired bootstrap over fixed public test rows gives 17/20 95% CIs crossing zero.

## Key numbers

| Check | Scope | Result |
|---|---:|---|
| Layer A metric recomputation | 14 pages, 101 submissions | 101/101 match official rounding |
| CSV-vs-JSON ids | all checked submissions | exact test-id agreement |
| Regression pages | 6 pages, 79 submissions | all MAE values reproduce |
| Classification pages | 7 pages, 21 submissions | all ACC values reproduce |
| Spectra page | 1 page, 1 submission | MULTIMAE reproduces |
| Layer B bounded pre-smoke | 512 train / 128 test | 273 Matminer features, 0 all-NaN rows, subset MAE 0.28496479 |
| Layer C point-gap map | 87 adjacent pairs | 29 gaps <=0.005; 38 gaps <=0.010 |
| Layer C bootstrap | 20 closest adjacent pairs | 17/20 95% CIs include zero |

## Closest bootstrap example

Formation energy page, dft_3d:

| Pair | Official MAE gap | Paired advantage | 95% CI | P(tie/reversal) |
|---|---:|---:|---:|---:|
| `kgcnn_coNGN` over `potnet` | 0.0002 | 0.00016852 | [-0.00160975, 0.00156560] | 0.4030 |

Interpretation: the point estimates are reproducible, but this adjacent ordering is
fragile under resampling of the fixed public test set.

## Evidence map

- Full assembled report: `reports/paper-002-jarvis-leaderboard-audit.md`
- Summary: `papers/jarvis-leaderboard/summary.md`
- Reproduction plan: `papers/jarvis-leaderboard/reproduction_plan.md`
- Metadata: `papers/jarvis-leaderboard/metadata.yaml`
- Layer A metric reports: `papers/jarvis-leaderboard/metric_check*.md`
- Layer B execution-path probe: `papers/jarvis-leaderboard/layer_b_probe.md`
- Layer B bounded pre-smoke: `papers/jarvis-leaderboard/layer_b_matminer_rf_smoke.md`
- Layer C point-gap map: `papers/jarvis-leaderboard/layer_c_resolution.md`
- Layer C paired bootstrap: `papers/jarvis-leaderboard/layer_c_bootstrap.md`
- Command log: `papers/jarvis-leaderboard/run_log.md`
- Core scripts:
  - `scripts/jarvis_score.py`
  - `scripts/jarvis_matminer_rf_smoke.py`
  - `scripts/jarvis_resolution.py`
  - `scripts/jarvis_bootstrap.py`
  - `scripts/make_jarvis_report.py`

## Packaging notes

- Several classification submission zips are named `test-acc.csv.zip`, but the
  single CSV inside is named `test-mae.csv`. Upstream reads the zip directly and is
  unaffected; independent tools should not assume the internal filename matches the
  outer archive.
- The public contribution runners are real, but their entrypoints are not uniform:
  `matminer_rf` and `matminer_xgboost` are hardcoded to `snumat`, XGBoost defaults
  to `gpu_hist`, and the CFID scripts assume a different benchmark path layout.

## Claims to avoid

- Do not claim a full JARVIS model-regeneration audit. Layer B is a bounded
  execution-path smoke, not a full leaderboard regeneration.
- Do not claim the bounded `matminer_rf` smoke reproduces the official
  `matminer_rf` MAE. It proves the adapted execution path can load structures,
  featurize, train, predict, and emit a traceable CSV on a deterministic slice.
- Do not describe the bootstrap as retraining uncertainty. It resamples fixed
  public test rows only.
- Do not imply the JARVIS leaderboard numbers are internally wrong. The main Layer A
  result is positive: the published point estimates are recoverable from public
  artifacts.

## Suggested short wording

> I ran a second ReproLab audit on JARVIS-Leaderboard. The result is positive for
> artifact integrity: 101/101 checked submissions across 14 benchmark pages
> reproduce the official MAE/ACC/MULTIMAE values from public CSV and JSON zips, with
> exact test-id agreement. The interpretability finding is that many adjacent
> leaderboard ranks are very close: among the 20 closest adjacent pairs, 17 have
> fixed-test-set bootstrap 95% CIs crossing zero. I also verified a bounded
> `matminer_rf` execution path in an isolated JARVIS environment.

## Next useful moves

1. Share this packet with one or two JARVIS/NIST or materials-ML reviewers for a
   sanity check before broad outreach.
2. If deeper Layer B is needed, scale the `matminer_rf` smoke cautiously toward a
   larger split slice.
3. If deeper Layer C is needed, add split-sensitivity or task-level uncertainty
   analysis beyond fixed-test-set bootstrap.
