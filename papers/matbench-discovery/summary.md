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

## Scope and limits

This is **Layer A** only: it verifies that leaderboard metrics are correctly derived
from the *published* predictions. It does **not** yet re-generate those predictions.
**Layer B** — running each model over the WBM initial structures on a GPU and re-scoring
— is the next step and will test the deeper claim that the predictions themselves
reproduce.
