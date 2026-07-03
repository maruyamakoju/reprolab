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

## Result — Layer B (GPU, prediction regeneration, n=500)

Beyond re-scoring published predictions, we regenerated predictions from scratch for
**three models** on the same deterministic 500-structure WBM subset (seed-42 sample of
`unique_prototypes`, ids committed in `layer_b_subset.csv`): initial structure → FIRE
relaxation with the model-specific upstream/YAML protocol (steps≤500,
FrechetCellFilter; fmax noted per model) →
formation energy → scored through the *same* Layer A metric path. The CHGNet
thresholds were pre-registered in `layer_b_plan.md` §7 before the first GPU smoke;
the MACE-MP-0 and ORB v2 extensions reused the same subset and acceptance criteria.

- **CHGNet: 500/500 relaxed, 0 failures** — RTX 4090, mean 1.06 s/structure (median 0.99,
  max 6.16), 9.3 min total GPU; 477/500 converged within the 500-step cap (the
  published pipeline ran under the same cap)
- CHGNet **median |Δe_form| = 0.03 meV/atom vs published** (threshold: ≤10);
  p95 = 0.07, max = 1.08 meV/atom; 100% of structures within 10 meV/atom — despite a
  2023→2026 dependency gap (torch 1.11→2.11, ase 3.22→3.29, chgnet package 0.4.2
  loading the same 0.3.0 weights, 412,525 params verified)
- CHGNet **100% stable/unstable classification agreement** (threshold: ≥95%); **zero flips**
  in either direction
- CHGNet discovery metrics computed from regenerated and published predictions are
  **identical** through both metric implementations (F1 0.584, MAE 0.067,
  TP/FP/TN/FN = 47/47/386/20 on this subset)
- GPU run-to-run variance bounded first on the 20-structure pre-smoke (two runs):
  median 0.000, max 0.232 meV/atom — far below the threshold, so deltas are
  interpretable
- Worst structure: wbm-2-42265 (S6Sr3), Δ = +1.1 meV/atom, classification unchanged
- **MACE-MP-0: 500/500 relaxed, 0 failures, 500/500 converged** — RTX 4090,
  mean 1.18 s/structure (median 1.04, max 6.99), 10.1 min total GPU; checkpoint
  `2023-12-03-mace-128-L1_epoch-199.model`, `mace-torch==0.3.16`, float64
- MACE-MP-0 **median |Δe_form| = 0.03 meV/atom vs published** (threshold: ≤10);
  p95 = 0.06, mean = 0.95, max = 216.65 meV/atom; 99.4% within 10 meV/atom
- MACE-MP-0 **99.6% stable/unstable classification agreement** (threshold: ≥95%);
  1 published-stable→regenerated-unstable flip and 1 unstable→stable flip. The
  unstable→stable flip is a threshold-boundary case (`wbm-3-56172`: each_pred
  0.000→−0.001 eV/atom, Δe_form = −0.1 meV/atom); the stable→unstable flip is the
  correction-drift outlier `wbm-2-28782`.
- The three large MACE-MP-0 e_form outliers are exactly the three structures already
  isolated by Layer C as MP2020 anion-correction version-drift cases
  (wbm-2-28782, wbm-4-28450, wbm-4-15908). Outside that correction edge case, the
  regenerated MACE predictions match the published CSV at rounding scale. Subset
  classification metrics match through both implementations (F1 0.655, Precision
  0.538, Recall 0.836, Accuracy 0.882; TP/FP/TN/FN = 56/48/385/11), while MAE/RMSE
  differ by 0.001 due to the correction-drift outliers.
- **ORB v2: 500/500 relaxed, 0 failures, 500/500 converged** — RTX 4090,
  mean 0.60 s/structure (median 0.50, max 3.05), 5.2 min total GPU; checkpoint
  `orb-v2-20241011.ckpt`, `orb-models==0.4.0`, S3 checkpoint URL from the upstream
  YAML. Normal dependency resolution would downgrade torch/numpy, so we installed
  ORB without those dependency downgrades and ran against `torch==2.11.0+cu128`.
- ORB v2 **median |Δe_form| = 0.05 meV/atom vs published** (threshold: ≤10);
  p95 = 0.17, mean = 0.11, max = 16.86 meV/atom; 99.8% within 10 meV/atom.
  Stable/unstable classification agreement is **100.0%** with zero flips. Subset
  classification metrics match through both implementations (F1 0.879, Precision
  0.892, Recall 0.866, Accuracy 0.968; TP/FP/TN/FN = 58/7/426/9), while MAE differs
  by 0.001.
- ORB v2 reproduced only when using the YAML hyperparameter `max_force: 0.02`. The
  upstream runner's default `force_max=0.05` produced a two-structure pre-smoke
  failure (Ba2I6 Δe_form = +212.3 meV/atom and a classification flip), while fmax
  0.02 reproduced the same two structures to ≤0.1 meV/atom and the 20-structure
  pre-smoke to max 0.12 meV/atom. This is a protocol-ambiguity finding, not a model
  failure.

**Verdict: the published CHGNet predictions reproduce from model execution** on this
subset, to well within the published CSV's own rounding scale. **MACE-MP-0 also
passes the same Layer B smoke criteria**, with the only large deviations tracing to
the same MP2020 correction-version dependency found independently in the ground-truth
audit. **ORB v2 also passes**, provided the YAML fmax=0.02 setting is used instead
of the runner's 0.05 default.

## Scope and limits

Layer A verifies that leaderboard metrics are correctly derived from the *published*
predictions (4/4 models exact). Layer B regenerates predictions for three models
(CHGNet, MACE-MP-0, and ORB v2) on a 500-structure deterministic subset — a small
but valid audit of the generation path, not a full leaderboard reproduction. Next
steps: package the external report/update or move to another paper. Full-WBM (257k)
regeneration is out of scope for v0.x.
