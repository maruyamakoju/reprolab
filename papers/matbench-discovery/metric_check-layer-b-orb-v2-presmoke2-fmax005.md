# Metric Check — Layer B: ORB v2 regenerated predictions (n=2)

Vertical slice: model relaxation -> prediction CSV -> Layer A metric path. Generation protocol per upstream `test_orb_discovery.py` (ORB v2 checkpoint, FIRE, steps<=500, FrechetCellFilter; fmax recorded in the relaxation run log). Scored with `compare_metrics.py` functions unchanged.

published preds: `models/orb/orbff-v2/2024-10-11-wbm-IS2RE.csv.gz` | regenerated: `experiments/layer-b/orb-v2/presmoke2-run1.jsonl.gz`


## Per-structure: regenerated vs published e_form (eV/atom)

| material_id | formula | n_sites | steps | conv | published | regenerated | Δ meV/atom | stable(pub) | stable(regen) | agree |
|---|---|---|---|---|---|---|---|---|---|---|
| wbm-3-33636 | Ba2I6 | 8 | 20 | y | -1.5799 | -1.3676 | +212.3 | S | U | ✗ |
| wbm-3-24460 | Er4Fe2In5 | 11 | 22 | y | -0.2672 | -0.2657 | +1.5 | U | U | ✓ |

## Agreement stats (pre-registered thresholds: median |Δ|<=10 meV/atom, classification agreement >=95%)

- n scored = 2
- median |Δ| = **106.89 meV/atom** (threshold: <=10)
- mean |Δ| = 106.89 | p95 |Δ| = 201.75 | max |Δ| = 212.29 meV/atom
- within 10 meV/atom: 50.0%
- classification agreement: **50.0%** (threshold: >=95%)
- flips stable->unstable (pub->regen): 1 | unstable->stable: 0

## Stable/unstable classification flips

| material_id | formula | published each_pred | regenerated each_pred | Δe_form meV/atom | direction |
|---|---|---|---|---|---|
| wbm-3-33636 | Ba2I6 | -0.0160 | 0.1960 | +212.3 | stable->unstable |

## Discovery metrics on this subset via the Layer A path (n=2 — subset-level, not leaderboard-comparable)

| metric | regenerated (indep) | regenerated (upstream_fn) | published (indep) | published (upstream_fn) |
|---|---|---|---|---|
| F1 | nan | nan | 1.000 | 1.000 |
| Precision | nan | nan | 1.000 | 1.000 |
| Recall | 0.000 | 0.000 | 1.000 | 1.000 |
| Accuracy | 0.500 | 0.500 | 1.000 | 1.000 |
| MAE | 0.110 | 0.110 | 0.013 | 0.013 |
| RMSE | 0.143 | 0.143 | 0.014 | 0.014 |
| TP | 0 | 0 | 1 | 1 |
| FP | 0 | 0 | 0 | 0 |
| TN | 1 | 1 | 1 | 1 |
| FN | 1 | 1 | 0 | 0 |
