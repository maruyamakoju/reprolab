# Metric Check — Layer B: CHGNet regenerated predictions (n=500)

Vertical slice: model relaxation -> prediction CSV -> Layer A metric path. Generation protocol per upstream `test_chgnet_discovery.py` (FIRE, steps<=500, fmax=0.05, relax_cell, FrechetCellFilter). Scored with `compare_metrics.py` functions unchanged.

published preds: `models/chgnet/chgnet-0.3.0/2023-12-21-wbm-IS2RE.csv.gz` | regenerated: `experiments/layer-b/chgnet/smoke500-run1.jsonl.gz`


## Worst 15 structures by |Δ| (full data in experiments/)

| material_id | formula | n_sites | steps | conv | published | regenerated | Δ meV/atom | stable(pub) | stable(regen) | agree |
|---|---|---|---|---|---|---|---|---|---|---|
| wbm-2-42265 | S6Sr3 | 9 | 80 | y | -1.6900 | -1.6889 | +1.1 | U | U | ✓ |
| wbm-3-5904 | As4Gd2 | 6 | 37 | y | -0.9494 | -0.9488 | +0.6 | U | U | ✓ |
| wbm-2-14997 | Al4F8 | 12 | 93 | y | -3.2045 | -3.2040 | +0.5 | U | U | ✓ |
| wbm-2-45027 | Se6Sm2 | 8 | 49 | y | -1.4907 | -1.4904 | +0.3 | S | S | ✓ |
| wbm-4-16455 | Cl4H2Mg2 | 8 | 44 | y | -1.1990 | -1.1989 | +0.1 | U | U | ✓ |
| wbm-1-36458 | Au2Hg2O4 | 8 | 44 | y | -0.5065 | -0.5066 | -0.1 | U | U | ✓ |
| wbm-1-25586 | Li1Ni2Pb1 | 4 | 18 | y | 0.0417 | 0.0418 | +0.1 | U | U | ✓ |
| wbm-1-11292 | Co3Ir1 | 4 | 37 | y | 0.0611 | 0.0612 | +0.1 | U | U | ✓ |
| wbm-1-7045 | Al4C5Th2 | 11 | 41 | y | -0.1514 | -0.1515 | -0.1 | U | U | ✓ |
| wbm-4-24096 | Ir1Ni2Zr1 | 4 | 34 | y | -0.4924 | -0.4923 | +0.1 | U | U | ✓ |
| wbm-5-5141 | Au1Cr1Fe2 | 4 | 16 | y | 0.2683 | 0.2684 | +0.1 | U | U | ✓ |
| wbm-1-21801 | Ho2I6 | 8 | 49 | y | -1.6823 | -1.6824 | -0.1 | U | U | ✓ |
| wbm-4-18193 | As2Co2Li1Nd1 | 6 | 30 | y | -0.6785 | -0.6784 | +0.1 | U | U | ✓ |
| wbm-4-6677 | Cl6Fe1Rb2 | 9 | 35 | y | -1.6191 | -1.6190 | +0.1 | S | S | ✓ |
| wbm-4-15908 | H8Nd2Pt2 | 12 | 42 | y | -0.5504 | -0.5503 | +0.1 | S | S | ✓ |

## Agreement stats (pre-registered thresholds: median |Δ|<=10 meV/atom, classification agreement >=95%)

- n scored = 500
- median |Δ| = **0.03 meV/atom** (threshold: <=10)
- mean |Δ| = 0.03 | p95 |Δ| = 0.07 | max |Δ| = 1.08 meV/atom
- within 10 meV/atom: 100.0%
- classification agreement: **100.0%** (threshold: >=95%)
- flips stable->unstable (pub->regen): 0 | unstable->stable: 0

## Discovery metrics on this subset via the Layer A path (n=500 — subset-level, not leaderboard-comparable)

| metric | regenerated (indep) | regenerated (upstream_fn) | published (indep) | published (upstream_fn) |
|---|---|---|---|---|
| F1 | 0.584 | 0.584 | 0.584 | 0.584 |
| Precision | 0.500 | 0.500 | 0.500 | 0.500 |
| Recall | 0.701 | 0.701 | 0.701 | 0.701 |
| Accuracy | 0.866 | 0.866 | 0.866 | 0.866 |
| MAE | 0.067 | 0.067 | 0.067 | 0.067 |
| RMSE | 0.104 | 0.104 | 0.104 | 0.104 |
| TP | 47 | 47 | 47 | 47 |
| FP | 47 | 47 | 47 | 47 |
| TN | 386 | 386 | 386 | 386 |
| FN | 20 | 20 | 20 | 20 |
