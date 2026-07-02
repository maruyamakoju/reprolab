# Metric Check — Layer B pre-smoke: CHGNet regenerated predictions (n=20)

Vertical slice: model relaxation -> prediction CSV -> Layer A metric path. Generation protocol per upstream `test_chgnet_discovery.py` (FIRE, steps<=500, fmax=0.05, relax_cell, FrechetCellFilter). Scored with `compare_metrics.py` functions unchanged.

published preds: `models/chgnet/chgnet-0.3.0/2023-12-21-wbm-IS2RE.csv.gz` | regenerated: `experiments/layer-b/chgnet/presmoke-run1.jsonl.gz`


## Per-structure: regenerated vs published e_form (eV/atom)

| material_id | formula | n_sites | steps | conv | published | regenerated | Δ meV/atom | stable(pub) | stable(regen) | agree |
|---|---|---|---|---|---|---|---|---|---|---|
| wbm-3-33636 | Ba2I6 | 8 | 33 | y | -1.5250 | -1.5251 | -0.1 | U | U | ✓ |
| wbm-3-24460 | Er4Fe2In5 | 11 | 66 | y | -0.3176 | -0.3176 | -0.0 | U | U | ✓ |
| wbm-2-29187 | N6Sr2Zn2 | 10 | 163 | y | -0.3653 | -0.3652 | +0.1 | U | U | ✓ |
| wbm-3-24851 | Fe2Tb1Yb1 | 4 | 17 | y | 0.3891 | 0.3891 | +0.0 | U | U | ✓ |
| wbm-1-49596 | Er2S6 | 8 | 31 | y | -1.5463 | -1.5463 | +0.0 | S | S | ✓ |
| wbm-1-38260 | Ca2Fe2O6 | 10 | 40 | y | -2.0748 | -2.0748 | -0.0 | U | U | ✓ |
| wbm-3-20857 | Cu2Eu2In2 | 6 | 22 | y | -0.2940 | -0.2940 | -0.0 | U | U | ✓ |
| wbm-2-36510 | Gd1O7Si2Zr1 | 11 | 30 | y | -3.4816 | -3.4816 | -0.0 | U | U | ✓ |
| wbm-2-31866 | In2Ni2Zn1 | 5 | 19 | y | -0.1561 | -0.1561 | -0.0 | U | U | ✓ |
| wbm-5-3711 | Ca1Ho1Pb2 | 4 | 19 | y | -0.5297 | -0.5297 | -0.0 | S | S | ✓ |
| wbm-4-16455 | Cl4H2Mg2 | 8 | 44 | y | -1.1990 | -1.1989 | +0.1 | U | U | ✓ |
| wbm-4-4335 | B1Ga2Ir2Lu1 | 6 | 28 | y | -0.6008 | -0.6008 | +0.0 | U | U | ✓ |
| wbm-3-11637 | C2Ge2La4 | 8 | 40 | y | -0.2782 | -0.2782 | +0.0 | U | U | ✓ |
| wbm-4-32299 | Au1Os1S2 | 4 | 5 | y | -0.3713 | -0.3712 | +0.1 | U | U | ✓ |
| wbm-2-24011 | In1Li4O5 | 10 | 31 | y | -1.6828 | -1.6828 | -0.0 | U | U | ✓ |
| wbm-4-28433 | Ga2Hf6O2 | 10 | 31 | y | -1.1969 | -1.1969 | +0.0 | U | U | ✓ |
| wbm-5-10472 | In2Pa2Re2 | 6 | 33 | y | -0.0932 | -0.0932 | -0.0 | S | S | ✓ |
| wbm-2-30414 | Au1Na1 | 2 | 19 | y | -0.3156 | -0.3156 | +0.0 | U | U | ✓ |
| wbm-2-17117 | Fe6In4Ru2 | 12 | 20 | y | 0.1066 | 0.1066 | +0.0 | U | U | ✓ |
| wbm-1-39713 | Dy2O6Sn2 | 10 | 117 | y | -2.7777 | -2.7777 | -0.0 | U | U | ✓ |

## Agreement stats (pre-registered thresholds apply at n=500; this is the wiring/variance run)

- median |Δ| = **0.0 meV/atom** (reproduce threshold: <=10)
- mean |Δ| = 0.0 | max |Δ| = 0.1 meV/atom
- within 10 meV/atom: 100%
- classification agreement: **100%** (threshold: >=95%)
- run1-vs-run2 |ΔE|/atom: median 0.000 / max 0.232 meV/atom (GPU run-to-run variance bound)

## Discovery metrics on this subset via the Layer A path (n=20 — wiring proof, not leaderboard-comparable)

| metric | regenerated (indep) | regenerated (upstream_fn) | published (indep) | published (upstream_fn) |
|---|---|---|---|---|
| F1 | 0.400 | 0.400 | 0.400 | 0.400 |
| Precision | 0.333 | 0.333 | 0.333 | 0.333 |
| Recall | 0.500 | 0.500 | 0.500 | 0.500 |
| Accuracy | 0.850 | 0.850 | 0.850 | 0.850 |
| MAE | 0.082 | 0.082 | 0.082 | 0.082 |
| RMSE | 0.104 | 0.104 | 0.104 | 0.104 |
| TP | 1 | 1 | 1 | 1 |
| FP | 2 | 2 | 2 | 2 |
| TN | 16 | 16 | 16 | 16 |
| FN | 1 | 1 | 1 | 1 |
