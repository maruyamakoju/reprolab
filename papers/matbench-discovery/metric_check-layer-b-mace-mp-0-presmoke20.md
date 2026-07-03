# Metric Check — Layer B: MACE-MP-0 regenerated predictions (n=20)

Vertical slice: model relaxation -> prediction CSV -> Layer A metric path. Generation protocol per upstream `test_mace_discovery.py` (MACE-MP-0 checkpoint, FIRE, steps<=500, fmax=0.05, FrechetCellFilter, float64). Scored with `compare_metrics.py` functions unchanged.

published preds: `models/mace/mace-mp-0/2023-12-11-wbm-IS2RE-FIRE.csv.gz` | regenerated: `experiments/layer-b/mace-mp-0/presmoke20-run1.jsonl.gz`


## Per-structure: regenerated vs published e_form (eV/atom)

| material_id | formula | n_sites | steps | conv | published | regenerated | Δ meV/atom | stable(pub) | stable(regen) | agree |
|---|---|---|---|---|---|---|---|---|---|---|
| wbm-3-33636 | Ba2I6 | 8 | 40 | y | -1.7800 | -1.7800 | +0.0 | S | S | ✓ |
| wbm-3-24460 | Er4Fe2In5 | 11 | 36 | y | -0.2990 | -0.2990 | -0.0 | U | U | ✓ |
| wbm-2-29187 | N6Sr2Zn2 | 10 | 106 | y | -0.3802 | -0.3802 | -0.0 | U | U | ✓ |
| wbm-3-24851 | Fe2Tb1Yb1 | 4 | 16 | y | 0.2958 | 0.2958 | -0.0 | U | U | ✓ |
| wbm-1-49596 | Er2S6 | 8 | 47 | y | -1.6520 | -1.6520 | +0.0 | S | S | ✓ |
| wbm-1-38260 | Ca2Fe2O6 | 10 | 34 | y | -2.0778 | -2.0778 | +0.0 | U | U | ✓ |
| wbm-3-20857 | Cu2Eu2In2 | 6 | 23 | y | -0.2722 | -0.2722 | -0.0 | U | U | ✓ |
| wbm-2-36510 | Gd1O7Si2Zr1 | 11 | 34 | y | -3.4970 | -3.4970 | +0.0 | U | U | ✓ |
| wbm-2-31866 | In2Ni2Zn1 | 5 | 31 | y | -0.1191 | -0.1191 | +0.0 | U | U | ✓ |
| wbm-5-3711 | Ca1Ho1Pb2 | 4 | 22 | y | -0.5654 | -0.5653 | +0.1 | S | S | ✓ |
| wbm-4-16455 | Cl4H2Mg2 | 8 | 48 | y | -1.1892 | -1.1892 | -0.0 | U | U | ✓ |
| wbm-4-4335 | B1Ga2Ir2Lu1 | 6 | 17 | y | -0.6088 | -0.6088 | -0.0 | U | U | ✓ |
| wbm-3-11637 | C2Ge2La4 | 8 | 50 | y | -0.2536 | -0.2536 | +0.0 | U | U | ✓ |
| wbm-4-32299 | Au1Os1S2 | 4 | 12 | y | -0.4007 | -0.4007 | +0.0 | U | U | ✓ |
| wbm-2-24011 | In1Li4O5 | 10 | 24 | y | -1.6660 | -1.6660 | +0.0 | U | U | ✓ |
| wbm-4-28433 | Ga2Hf6O2 | 10 | 20 | y | -1.1019 | -1.1019 | -0.0 | U | U | ✓ |
| wbm-5-10472 | In2Pa2Re2 | 6 | 26 | y | 0.0966 | 0.0966 | -0.0 | U | U | ✓ |
| wbm-2-30414 | Au1Na1 | 2 | 9 | y | -0.2849 | -0.2848 | +0.1 | U | U | ✓ |
| wbm-2-17117 | Fe6In4Ru2 | 12 | 8 | y | 0.2870 | 0.2870 | +0.0 | U | U | ✓ |
| wbm-1-39713 | Dy2O6Sn2 | 10 | 52 | y | -2.7636 | -2.7637 | -0.1 | U | U | ✓ |

## Agreement stats (pre-registered thresholds: median |Δ|<=10 meV/atom, classification agreement >=95%)

- n scored = 20
- median |Δ| = **0.02 meV/atom** (threshold: <=10)
- mean |Δ| = 0.03 | p95 |Δ| = 0.06 | max |Δ| = 0.07 meV/atom
- within 10 meV/atom: 100.0%
- classification agreement: **100.0%** (threshold: >=95%)
- flips stable->unstable (pub->regen): 0 | unstable->stable: 0
- run1-vs-run2 |ΔE|/atom: median 0.000 / max 0.000 meV/atom (GPU run-to-run variance bound)

## Discovery metrics on this subset via the Layer A path (n=20 — subset-level, not leaderboard-comparable)

| metric | regenerated (indep) | regenerated (upstream_fn) | published (indep) | published (upstream_fn) |
|---|---|---|---|---|
| F1 | 0.400 | 0.400 | 0.400 | 0.400 |
| Precision | 0.333 | 0.333 | 0.333 | 0.333 |
| Recall | 0.500 | 0.500 | 0.500 | 0.500 |
| Accuracy | 0.850 | 0.850 | 0.850 | 0.850 |
| MAE | 0.099 | 0.099 | 0.099 | 0.099 |
| RMSE | 0.126 | 0.126 | 0.126 | 0.126 |
| TP | 1 | 1 | 1 | 1 |
| FP | 2 | 2 | 2 | 2 |
| TN | 16 | 16 | 16 | 16 |
| FN | 1 | 1 | 1 | 1 |
