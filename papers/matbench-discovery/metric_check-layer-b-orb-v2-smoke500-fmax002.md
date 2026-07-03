# Metric Check — Layer B: ORB v2 regenerated predictions (n=500)

Vertical slice: model relaxation -> prediction CSV -> Layer A metric path. Generation protocol per upstream `test_orb_discovery.py` (ORB v2 checkpoint, FIRE, steps<=500, FrechetCellFilter; fmax recorded in the relaxation run log). Scored with `compare_metrics.py` functions unchanged.

published preds: `models/orb/orbff-v2/2024-10-11-wbm-IS2RE.csv.gz` | regenerated: `experiments/layer-b/orb-v2/smoke500-fmax002-run1.jsonl.gz`


## Worst 15 structures by |Δ| (full data in experiments/)

| material_id | formula | n_sites | steps | conv | published | regenerated | Δ meV/atom | stable(pub) | stable(regen) | agree |
|---|---|---|---|---|---|---|---|---|---|---|
| wbm-3-9104 | B3Cu6Zr3 | 12 | 19 | y | -0.0572 | -0.0741 | -16.9 | U | U | ✓ |
| wbm-2-19678 | Ba2Ge4Rh2 | 8 | 21 | y | -0.5764 | -0.5751 | +1.3 | U | U | ✓ |
| wbm-1-32148 | N2O4Sr2V2 | 10 | 28 | y | -2.0686 | -2.0673 | +1.3 | U | U | ✓ |
| wbm-1-19979 | Ge3Ru6 | 9 | 16 | y | 0.0512 | 0.0501 | -1.1 | U | U | ✓ |
| wbm-2-25852 | Cr1Mg1Sb1 | 3 | 7 | y | 0.0745 | 0.0753 | +0.8 | U | U | ✓ |
| wbm-1-50851 | S1Ta1 | 2 | 8 | y | -0.4104 | -0.4109 | -0.5 | U | U | ✓ |
| wbm-1-36988 | Cs2F2O4Se2 | 10 | 36 | y | -1.9336 | -1.9340 | -0.4 | S | S | ✓ |
| wbm-2-29024 | Ce2N6Rh2 | 10 | 25 | y | -0.6712 | -0.6709 | +0.3 | U | U | ✓ |
| wbm-1-30574 | Ho2N4Sr2 | 8 | 17 | y | -1.0411 | -1.0414 | -0.3 | U | U | ✓ |
| wbm-1-34166 | Ir1Nb1Sb1 | 3 | 3 | y | -0.2915 | -0.2912 | +0.3 | U | U | ✓ |
| wbm-2-20755 | Ge4Np4Rh4 | 12 | 34 | y | -0.4704 | -0.4701 | +0.3 | S | S | ✓ |
| wbm-2-7301 | C4Fe2U2 | 8 | 18 | y | -0.0660 | -0.0657 | +0.3 | U | U | ✓ |
| wbm-2-21952 | H1N1U1 | 3 | 17 | y | -0.6531 | -0.6529 | +0.2 | U | U | ✓ |
| wbm-2-42779 | Cs2Pd4S6 | 12 | 36 | y | -0.8508 | -0.8510 | -0.2 | U | U | ✓ |
| wbm-4-31321 | Ir2Rh1Th1 | 4 | 9 | y | -0.6272 | -0.6270 | +0.2 | U | U | ✓ |

## Agreement stats (pre-registered thresholds: median |Δ|<=10 meV/atom, classification agreement >=95%)

- n scored = 500
- median |Δ| = **0.05 meV/atom** (threshold: <=10)
- mean |Δ| = 0.11 | p95 |Δ| = 0.17 | max |Δ| = 16.86 meV/atom
- within 10 meV/atom: 99.8%
- classification agreement: **100.0%** (threshold: >=95%)
- flips stable->unstable (pub->regen): 0 | unstable->stable: 0

## Discovery metrics on this subset via the Layer A path (n=500 — subset-level, not leaderboard-comparable)

| metric | regenerated (indep) | regenerated (upstream_fn) | published (indep) | published (upstream_fn) |
|---|---|---|---|---|
| F1 | 0.879 | 0.879 | 0.879 | 0.879 |
| Precision | 0.892 | 0.892 | 0.892 | 0.892 |
| Recall | 0.866 | 0.866 | 0.866 | 0.866 |
| Accuracy | 0.968 | 0.968 | 0.968 | 0.968 |
| MAE | 0.032 | 0.032 | 0.031 | 0.031 |
| RMSE | 0.072 | 0.072 | 0.072 | 0.072 |
| TP | 58 | 58 | 58 | 58 |
| FP | 7 | 7 | 7 | 7 |
| TN | 426 | 426 | 426 | 426 |
| FN | 9 | 9 | 9 | 9 |
