# Metric Check — Layer B: ORB v2 regenerated predictions (n=20)

Vertical slice: model relaxation -> prediction CSV -> Layer A metric path. Generation protocol per upstream `test_orb_discovery.py` (ORB v2 checkpoint, FIRE, steps<=500, FrechetCellFilter; fmax recorded in the relaxation run log). Scored with `compare_metrics.py` functions unchanged.

published preds: `models/orb/orbff-v2/2024-10-11-wbm-IS2RE.csv.gz` | regenerated: `experiments/layer-b/orb-v2/presmoke20-fmax002-run1.jsonl.gz`


## Per-structure: regenerated vs published e_form (eV/atom)

| material_id | formula | n_sites | steps | conv | published | regenerated | Δ meV/atom | stable(pub) | stable(regen) | agree |
|---|---|---|---|---|---|---|---|---|---|---|
| wbm-3-33636 | Ba2I6 | 8 | 83 | y | -1.5799 | -1.5800 | -0.1 | S | S | ✓ |
| wbm-3-24460 | Er4Fe2In5 | 11 | 23 | y | -0.2672 | -0.2672 | -0.0 | U | U | ✓ |
| wbm-2-29187 | N6Sr2Zn2 | 10 | 36 | y | -0.3102 | -0.3102 | -0.0 | U | U | ✓ |
| wbm-3-24851 | Fe2Tb1Yb1 | 4 | 7 | y | 0.3480 | 0.3479 | -0.1 | U | U | ✓ |
| wbm-1-49596 | Er2S6 | 8 | 25 | y | -1.4790 | -1.4791 | -0.1 | U | U | ✓ |
| wbm-1-38260 | Ca2Fe2O6 | 10 | 76 | y | -2.1469 | -2.1470 | -0.1 | U | U | ✓ |
| wbm-3-20857 | Cu2Eu2In2 | 6 | 23 | y | -0.2499 | -0.2499 | -0.0 | U | U | ✓ |
| wbm-2-36510 | Gd1O7Si2Zr1 | 11 | 21 | y | -3.4129 | -3.4129 | +0.0 | U | U | ✓ |
| wbm-2-31866 | In2Ni2Zn1 | 5 | 16 | y | -0.1390 | -0.1391 | -0.1 | U | U | ✓ |
| wbm-5-3711 | Ca1Ho1Pb2 | 4 | 0 | y | -0.4132 | -0.4132 | +0.0 | U | U | ✓ |
| wbm-4-16455 | Cl4H2Mg2 | 8 | 24 | y | -0.9686 | -0.9685 | +0.1 | U | U | ✓ |
| wbm-4-4335 | B1Ga2Ir2Lu1 | 6 | 9 | y | -0.5033 | -0.5033 | +0.0 | U | U | ✓ |
| wbm-3-11637 | C2Ge2La4 | 8 | 23 | y | -0.1711 | -0.1712 | -0.1 | U | U | ✓ |
| wbm-4-32299 | Au1Os1S2 | 4 | 3 | y | -0.2696 | -0.2696 | -0.0 | U | U | ✓ |
| wbm-2-24011 | In1Li4O5 | 10 | 20 | y | -1.6359 | -1.6360 | -0.1 | U | U | ✓ |
| wbm-4-28433 | Ga2Hf6O2 | 10 | 13 | y | -1.3962 | -1.3962 | -0.0 | U | U | ✓ |
| wbm-5-10472 | In2Pa2Re2 | 6 | 4 | y | -0.0208 | -0.0208 | +0.0 | U | U | ✓ |
| wbm-2-30414 | Au1Na1 | 2 | 16 | y | -0.2719 | -0.2719 | +0.0 | U | U | ✓ |
| wbm-2-17117 | Fe6In4Ru2 | 12 | 8 | y | 0.1789 | 0.1789 | -0.0 | U | U | ✓ |
| wbm-1-39713 | Dy2O6Sn2 | 10 | 43 | y | -2.6449 | -2.6450 | -0.1 | U | U | ✓ |

## Agreement stats (pre-registered thresholds: median |Δ|<=10 meV/atom, classification agreement >=95%)

- n scored = 20
- median |Δ| = **0.04 meV/atom** (threshold: <=10)
- mean |Δ| = 0.05 | p95 |Δ| = 0.12 | max |Δ| = 0.12 meV/atom
- within 10 meV/atom: 100.0%
- classification agreement: **100.0%** (threshold: >=95%)
- flips stable->unstable (pub->regen): 0 | unstable->stable: 0
- run1-vs-run2 |ΔE|/atom: median 0.014 / max 0.127 meV/atom (GPU run-to-run variance bound)

## Discovery metrics on this subset via the Layer A path (n=20 — subset-level, not leaderboard-comparable)

| metric | regenerated (indep) | regenerated (upstream_fn) | published (indep) | published (upstream_fn) |
|---|---|---|---|---|
| F1 | 0.667 | 0.667 | 0.667 | 0.667 |
| Precision | 1.000 | 1.000 | 1.000 | 1.000 |
| Recall | 0.500 | 0.500 | 0.500 | 0.500 |
| Accuracy | 0.950 | 0.950 | 0.950 | 0.950 |
| MAE | 0.034 | 0.034 | 0.034 | 0.034 |
| RMSE | 0.063 | 0.063 | 0.063 | 0.063 |
| TP | 1 | 1 | 1 | 1 |
| FP | 0 | 0 | 0 | 0 |
| TN | 18 | 18 | 18 | 18 |
| FN | 1 | 1 | 1 | 1 |
