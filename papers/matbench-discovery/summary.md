## What this is

An independent, third-party reproducibility audit of the **Matbench Discovery**
leaderboard (Riebesell et al., *Nature Machine Intelligence* 7, 836–847, 2025;
repo `janosh/matbench-discovery`, commit `eaa7550`, pkg 1.3.1). We ask a narrow,
checkable question: **do the published per-model stability metrics follow from the
published predictions and the bundled ground truth?**

## Result — Layer A (metric recomputation, CPU, deterministic)

For each model we recompute the discovery-task metrics from its published prediction CSV
and the bundled WBM ground truth, **two independent ways** — a from-scratch
re-implementation and the upstream `stable_metrics` — and diff against the values
committed in the model's YAML.

| Model | Subset | F1 (official / repro) | MAE eV/atom (official / repro) | Confusion counts | Verdict |
|---|---|---|---|---|---|
| CHGNet | unique_prototypes | 0.613 / 0.613 | 0.063 / 0.063 | exact | ✅ MATCH |
| CHGNet | full_test_set | 0.612 / 0.612 | 0.061 / 0.061 | exact | ✅ MATCH |
| SevenNet-0 | unique_prototypes | 0.724 / 0.724 | 0.048 / 0.048 | exact | ✅ MATCH |
| SevenNet-0 | full_test_set | 0.719 / 0.719 | 0.046 / 0.046 | exact | ✅ MATCH |
| MACE-MP-0 | unique_prototypes | 0.669 / 0.669 | 0.057 / 0.057 | exact | ✅ MATCH |
| MACE-MP-0 | full_test_set | 0.668 / 0.668 | 0.055 / 0.055 | exact | ✅ MATCH |
| ORB v2 | unique_prototypes | 0.880 / 0.880 | 0.028 / 0.028 | exact | ✅ MATCH |
| ORB v2 | full_test_set | 0.858 / 0.858 | 0.028 / 0.028 | exact | ✅ MATCH |

**4 of 4 models reproduce exactly** — every reported fraction to 3 decimals and every
integer confusion-matrix count (TP/FP/TN/FN) identical, on both audited subsets. The
outlier/missing-prediction accounting also matches in two distinct regimes: filter-driven
(CHGNet 2, SevenNet 3, ORB v2 2 dropped by the 5 eV/atom rule) and genuine-NaN-driven
(MACE 38 full / 34 uniq, filter dropped 0). The four models span three architecture
families and the leaderboard's F1 range from 0.61 (CHGNet) to 0.88 (ORB v2).

## Reproducibility findings (worth knowing before you trust `pip install`)

1. **Prediction URLs are WAF-blocked for naive downloaders.** The `pred_file_url` fields
   (`figshare.com/files/<id>`) return an empty body to a plain GET; the working endpoint
   is the Figshare API (`api.figshare.com/v2/file/download/<id>`). The package rewrites
   this internally, so only independent re-users hit it.
2. **PyPI wheel ≠ GitHub HEAD under the same version `1.3.1`.** The wheel ships a flat
   module layout (`metrics.py`); the repo HEAD ships a package layout
   (`metrics/discovery.py`). Import paths differ. We therefore audit the *cloned repo*
   and use pip only for dependencies.
3. **One transient native crash (0xC0000005)** occurred on the combined
   download+compute path (SevenNet, first attempt); it did not recur once download and
   compute were split (`--download-only`). Recorded as a Windows-environment note.

## Result — Layer B pre-smoke (GPU, prediction regeneration)

Beyond re-scoring published predictions, we regenerated predictions from scratch for
**CHGNet** on a deterministic 20-structure WBM subset (seed-42 sample of
`unique_prototypes`, ids committed in `layer_b_subset.csv`): initial structure → FIRE
relaxation with the upstream protocol (steps≤500, fmax=0.05, FrechetCellFilter) →
formation energy → scored through the *same* Layer A metric path.

- **20/20 relaxed, 0 failures, 20/20 converged** — RTX 4090, mean 1.26 s/structure
  (median 0.94, max 5.35)
- **Regenerated e_form matches published values within 0.1 meV/atom on every
  structure** (max |Δ| = 0.1 meV/atom = the published CSV's rounding precision;
  median 0.0), despite a 2023→2026 dependency gap (torch 1.11→2.11, ase 3.22→3.29,
  chgnet package 0.4.2 loading the same 0.3.0 weights, 412,525 params verified)
- **100% stable/unstable classification agreement**; discovery metrics computed from
  regenerated and published predictions are identical through both metric
  implementations
- GPU run-to-run variance (two independent runs): median 0.000, max 0.232 meV/atom —
  far below the 10 meV/atom reproduce threshold, so the comparison is interpretable
- Largest discrepancies (all +/−0.1 meV/atom): wbm-2-29187, wbm-4-16455, wbm-4-32299

**Scaling to the 500-structure smoke run is justified** (estimated ~10–15 min GPU);
pre-registered thresholds in `layer_b_plan.md` §7 formally apply at n=500.

## Scope and limits

Layer A verifies that leaderboard metrics are correctly derived from the *published*
predictions (4/4 models exact). Layer B so far regenerates predictions for one model on
20 structures — a vertical-slice wiring proof, not yet a statistical claim. Next steps:
the 500-structure smoke run, then (optionally) additional models. Full-WBM (257k)
regeneration is out of scope for v0.x.
