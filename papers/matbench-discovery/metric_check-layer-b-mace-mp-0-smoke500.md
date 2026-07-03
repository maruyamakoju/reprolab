# Metric Check — Layer B: MACE-MP-0 regenerated predictions (n=500)

Vertical slice: model relaxation -> prediction CSV -> Layer A metric path. Generation protocol per upstream `test_mace_discovery.py` (MACE-MP-0 checkpoint, FIRE, steps<=500, fmax=0.05, FrechetCellFilter, float64). Scored with `compare_metrics.py` functions unchanged.

published preds: `models/mace/mace-mp-0/2023-12-11-wbm-IS2RE-FIRE.csv.gz` | regenerated: `experiments/layer-b/mace-mp-0/smoke500-run1.jsonl.gz`


## Worst 15 structures by |Δ| (full data in experiments/)

| material_id | formula | n_sites | steps | conv | published | regenerated | Δ meV/atom | stable(pub) | stable(regen) | agree |
|---|---|---|---|---|---|---|---|---|---|---|
| wbm-2-28782 | Br2N6Sr2 | 10 | 79 | y | -1.1176 | -0.9010 | +216.6 | S | U | ✗ |
| wbm-4-28450 | I2O2Pa2 | 6 | 16 | y | -2.5213 | -2.3950 | +126.3 | U | U | ✓ |
| wbm-4-15908 | H8Nd2Pt2 | 12 | 46 | y | -0.5421 | -0.6614 | -119.3 | S | S | ✓ |
| wbm-3-70895 | Cu1Pu2Si1 | 4 | 32 | y | -0.0160 | -0.0159 | +0.1 | U | U | ✓ |
| wbm-3-4455 | Al1Ge1Tb2 | 4 | 13 | y | -0.6151 | -0.6152 | -0.1 | U | U | ✓ |
| wbm-3-5167 | Al2Cs2S6Zn2 | 12 | 29 | y | -1.2541 | -1.2540 | +0.1 | S | S | ✓ |
| wbm-5-3711 | Ca1Ho1Pb2 | 4 | 22 | y | -0.5654 | -0.5653 | +0.1 | S | S | ✓ |
| wbm-4-18193 | As2Co2Li1Nd1 | 6 | 24 | y | -0.6343 | -0.6342 | +0.1 | U | U | ✓ |
| wbm-4-35943 | Ho2Ni2Si1 | 5 | 18 | y | -0.6670 | -0.6669 | +0.1 | S | S | ✓ |
| wbm-2-27095 | Ir2Mg1Zn1 | 4 | 32 | y | -0.2366 | -0.2365 | +0.1 | U | U | ✓ |
| wbm-4-29557 | Ir2P2Rb2 | 6 | 22 | y | -0.5950 | -0.5949 | +0.1 | S | S | ✓ |
| wbm-4-2254 | Ag6Al2K4 | 12 | 31 | y | -0.0217 | -0.0218 | -0.1 | U | U | ✓ |
| wbm-4-31321 | Ir2Rh1Th1 | 4 | 19 | y | -0.6269 | -0.6268 | +0.1 | U | U | ✓ |
| wbm-1-6032 | Be2Er2Si2 | 6 | 24 | y | -0.5965 | -0.5964 | +0.1 | S | S | ✓ |
| wbm-1-49747 | Ge2Ni4S6 | 12 | 21 | y | -0.5382 | -0.5381 | +0.1 | U | U | ✓ |

## Agreement stats (pre-registered thresholds: median |Δ|<=10 meV/atom, classification agreement >=95%)

- n scored = 500
- median |Δ| = **0.03 meV/atom** (threshold: <=10)
- mean |Δ| = 0.95 | p95 |Δ| = 0.06 | max |Δ| = 216.65 meV/atom
- within 10 meV/atom: 99.4%
- classification agreement: **99.6%** (threshold: >=95%)
- flips stable->unstable (pub->regen): 1 | unstable->stable: 1

## Stable/unstable classification flips

| material_id | formula | published each_pred | regenerated each_pred | Δe_form meV/atom | direction |
|---|---|---|---|---|---|
| wbm-3-56172 | Co1Cs1Mo2O8 | 0.0000 | -0.0010 | -0.1 | unstable->stable |
| wbm-2-28782 | Br2N6Sr2 | -0.0010 | 0.2160 | +216.6 | stable->unstable |

## Discovery metrics on this subset via the Layer A path (n=500 — subset-level, not leaderboard-comparable)

| metric | regenerated (indep) | regenerated (upstream_fn) | published (indep) | published (upstream_fn) |
|---|---|---|---|---|
| F1 | 0.655 | 0.655 | 0.655 | 0.655 |
| Precision | 0.538 | 0.538 | 0.538 | 0.538 |
| Recall | 0.836 | 0.836 | 0.836 | 0.836 |
| Accuracy | 0.882 | 0.882 | 0.882 | 0.882 |
| MAE | 0.063 | 0.063 | 0.062 | 0.062 |
| RMSE | 0.109 | 0.109 | 0.108 | 0.108 |
| TP | 56 | 56 | 56 | 56 |
| FP | 48 | 48 | 48 | 48 |
| TN | 385 | 385 | 385 | 385 |
| FN | 11 | 11 | 11 | 11 |
