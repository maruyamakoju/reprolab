# Metric Check — Layer B: ORB v2 regenerated predictions (n=2)

Vertical slice: model relaxation -> prediction CSV -> Layer A metric path. Generation protocol per upstream `test_orb_discovery.py` (ORB v2 checkpoint, FIRE, steps<=500, fmax=0.05, FrechetCellFilter). Scored with `compare_metrics.py` functions unchanged.

published preds: `models/orb/orbff-v2/2024-10-11-wbm-IS2RE.csv.gz` | regenerated: `experiments/layer-b/orb-v2/presmoke2-fmax002-run1.jsonl.gz`


## Per-structure: regenerated vs published e_form (eV/atom)

| material_id | formula | n_sites | steps | conv | published | regenerated | Δ meV/atom | stable(pub) | stable(regen) | agree |
|---|---|---|---|---|---|---|---|---|---|---|
| wbm-3-33636 | Ba2I6 | 8 | 83 | y | -1.5799 | -1.5800 | -0.1 | S | S | ✓ |
| wbm-3-24460 | Er4Fe2In5 | 11 | 23 | y | -0.2672 | -0.2672 | -0.0 | U | U | ✓ |

## Agreement stats (pre-registered thresholds: median |Δ|<=10 meV/atom, classification agreement >=95%)

- n scored = 2
- median |Δ| = **0.04 meV/atom** (threshold: <=10)
- mean |Δ| = 0.04 | p95 |Δ| = 0.05 | max |Δ| = 0.05 meV/atom
- within 10 meV/atom: 100.0%
- classification agreement: **100.0%** (threshold: >=95%)
- flips stable->unstable (pub->regen): 0 | unstable->stable: 0

## Discovery metrics on this subset via the Layer A path (n=2 — subset-level, not leaderboard-comparable)

| metric | regenerated (indep) | regenerated (upstream_fn) | published (indep) | published (upstream_fn) |
|---|---|---|---|---|
| F1 | 1.000 | 1.000 | 1.000 | 1.000 |
| Precision | 1.000 | 1.000 | 1.000 | 1.000 |
| Recall | 1.000 | 1.000 | 1.000 | 1.000 |
| Accuracy | 1.000 | 1.000 | 1.000 | 1.000 |
| MAE | 0.013 | 0.013 | 0.013 | 0.013 |
| RMSE | 0.014 | 0.014 | 0.014 | 0.014 |
| TP | 1 | 1 | 1 | 1 |
| FP | 0 | 0 | 0 | 0 |
| TN | 1 | 1 | 1 | 1 |
| FN | 0 | 0 | 0 | 0 |
