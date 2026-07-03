# Metric Check — Layer B: MACE-MP-0 regenerated predictions (n=2)

Vertical slice: model relaxation -> prediction CSV -> Layer A metric path. Generation protocol per upstream `test_mace_discovery.py` (MACE-MP-0 checkpoint, FIRE, steps<=500, fmax=0.05, FrechetCellFilter, float64). Scored with `compare_metrics.py` functions unchanged.

published preds: `models/mace/mace-mp-0/2023-12-11-wbm-IS2RE-FIRE.csv.gz` | regenerated: `experiments/layer-b/mace-mp-0/presmoke2-run2.jsonl.gz`


## Per-structure: regenerated vs published e_form (eV/atom)

| material_id | formula | n_sites | steps | conv | published | regenerated | Δ meV/atom | stable(pub) | stable(regen) | agree |
|---|---|---|---|---|---|---|---|---|---|---|
| wbm-3-33636 | Ba2I6 | 8 | 40 | y | -1.7800 | -1.7800 | +0.0 | S | S | ✓ |
| wbm-3-24460 | Er4Fe2In5 | 11 | 36 | y | -0.2990 | -0.2990 | -0.0 | U | U | ✓ |

## Agreement stats (pre-registered thresholds: median |Δ|<=10 meV/atom, classification agreement >=95%)

- n scored = 2
- median |Δ| = **0.03 meV/atom** (threshold: <=10)
- mean |Δ| = 0.03 | p95 |Δ| = 0.04 | max |Δ| = 0.05 meV/atom
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
| MAE | 0.112 | 0.112 | 0.112 | 0.112 |
| RMSE | 0.149 | 0.149 | 0.149 | 0.149 |
| TP | 1 | 1 | 1 | 1 |
| FP | 0 | 0 | 0 | 0 |
| TN | 1 | 1 | 1 | 1 |
| FN | 0 | 0 | 0 | 0 |
