# Reproduction Plan — Matbench Discovery (Paper-001)

Status: **metric path confirmed at code level** (2026-07-02). Execution starts 2026-07-03.

## 0. What "reproducing the leaderboard" actually means here

The Matbench Discovery leaderboard has **two independently checkable layers**. This
matters: only Layer B needs a GPU.

| Layer | Claim tested | Inputs | Compute | Determinism |
|-------|--------------|--------|---------|-------------|
| **A. Metric recomputation** | "The reported F1/MAE follow correctly from the model's *published* predictions" | published prediction CSV + WBM ground truth | **CPU only, minutes** | fully deterministic |
| **B. Prediction regeneration** | "Those predictions can themselves be reproduced by running the model" | WBM initial structures + model checkpoint | **1 GPU, ~hours–days** | approximate (relaxation, HW) |

We do **Layer A first** (it is the cleanest possible reproduction and is where the
leaderboard numbers are literally computed), then Layer B on the RTX 5090/4090.

---

## 1. Target metric (Layer A)

Primary: **CHGNet, `unique_prototypes` subset** (the leaderboard default).
- **F1 = 0.613**, Precision = 0.514, Recall = 0.758, Accuracy = 0.851
- **MAE = 0.063 eV/atom**, RMSE = 0.103, R² = 0.689
- Confusion counts: TP 25313 / FP 23955 / TN 158159 / FN 8061

Also reproduce `full_test_set` (F1 = 0.612, MAE = 0.061) as a cross-check.
`most_stable_10k` deferred until the selection rule is confirmed from source (§6).

## 2. Source-code path (traceability)

Everything below is in `vendor/matbench-discovery/` (commit `eaa7550`, pkg v1.3.1).

| Step | Code | Key detail |
|------|------|-----------|
| Stability threshold | `matbench_discovery/__init__.py:65` | `STABILITY_THRESHOLD = 0` |
| Ground-truth columns | `matbench_discovery/enums.py:49,58,85` | `e_form_per_atom_mp2020_corrected`, `e_above_hull_mp2020_corrected_ppd_mp`, `unique_prototype` |
| EACH_pred derivation | `matbench_discovery/preds/discovery.py:33-35` | `each_pred = each_true + e_form_pred − e_form_dft` (fixed DFT hull) |
| Error filter | `matbench_discovery/data.py:291-305` | `|e_form_pred − e_form_dft| > 5` → NaN |
| Classify TP/FP/TN/FN | `metrics/discovery.py:20-84` `classify_stable` | NaN preds filled as **unstable** (`fillna=True`) |
| Compute F1/MAE/… | `metrics/discovery.py:87-186` `stable_metrics` | returns F1, Precision, Recall, Accuracy, MAE, RMSE, R2, DAF, TPR/FPR/TNR/FNR, TP/FP/TN/FN |
| Official values read from | `metrics/__init__.py:10-41` `metrics_df_from_yaml` | leaderboard table = the numbers stored in each model YAML |
| CHGNet official values | `models/chgnet/chgnet-0.3.0.yml:109-166` | `metrics.discovery.{full_test_set,unique_prototypes,most_stable_10k}` |

The official recompute-and-write entrypoint is:
`python matbench_discovery/preds/discovery.py chgnet-0.3.0`
(it **overwrites** the YAML). Our audit does **not** overwrite; `compare_metrics.py`
recomputes into a separate table and diffs against the committed YAML values.

## 3. Required data

| Artifact | Path | Source | Size | In clone? |
|----------|------|--------|------|-----------|
| WBM ground truth | `data/wbm/2023-12-13-wbm-summary.csv.gz` | bundled | ~a few MB | **yes** |
| CHGNet predictions | `models/chgnet/chgnet-0.3.0/2023-12-21-wbm-IS2RE.csv.gz` | Figshare file `52057526` | ~tens of MB | **no → download** |

No DFT, no wet lab, no checkpoint needed for Layer A.

## 4. Command to run (Layer A)

```bash
# from reprolab/, inside the venv that has matbench-discovery installed
python scripts/run_command.py -- \
  python scripts/compare_metrics.py \
    --repo vendor/matbench-discovery \
    --model chgnet-0.3.0 \
    --subsets unique_prototypes full_test_set \
    --out papers/matbench-discovery/metric_check.md
```

`compare_metrics.py` will: load ground truth → download+load CHGNet preds →
derive `each_pred` → apply the 5 eV/atom filter → compute metrics **two ways**
(official `stable_metrics` + our independent re-implementation) → read official YAML
values → emit a diff table.

## 5. Expected output & pass criterion

A table like:

| subset | metric | official | reproduced | Δ | pass |
|--------|--------|----------|-----------|---|------|
| unique_prototypes | F1 | 0.613 | 0.6xx | … | ✓/✗ |

**Pass (Layer A):** reproduced matches official within rounding
(±0.001 on fractions, ±0.001 eV/atom on MAE/RMSE, exact on TP/FP/TN/FN).
Any deviation is a *finding* → `failure_notes.md` with the suspected cause
(column drift, filter handling, subset definition, pandas/numpy version behavior).

## 6. Comparison method / open questions to resolve during execution

1. **`most_stable_10k` selection rule** — confirm from source whether it is the 10k
   lowest predicted EACH (nsmallest) before scoring; implement only after confirming.
2. **`missing_preds`** — CHGNet reports 2 missing on full_test_set, 0 on uniq_protos.
   Verify our load reproduces the same missing count (sanity check on data join).
3. **Independent vs official metric fn** — if our re-implementation and the package
   function disagree, that is itself an audit finding about the metric code.
4. **Rounding** — the YAML stores rounded values (`.round(3)` on preds too, see
   `preds/discovery.py:28`); reproduce the rounding before diffing.

## 7. Layer B (GPU, Jul 3+ stretch)

Regenerate CHGNet predictions locally to test the deeper claim:
- Script: `models/chgnet/test_chgnet_discovery.py` (IS2RE, FIRE optimizer,
  `max_steps=500`, `fmax=0.05`, `FrechetCellFilter`).
- Needs local edits: strip `slurm_submit`/`wandb`, loop over all ~257k WBM initial
  structures (`DataFiles.wbm_initial_structures`), run on `cuda`.
- Deps: `pip install chgnet` (+ torch CUDA). Fits one RTX 4090/5090; wall time is the
  cost driver (relaxation of ~257k structures) → run a **subset first** (e.g. 2k) to
  validate the pipeline, then scale.
- Then feed regenerated preds through the same `compare_metrics.py` and compare the
  Layer-B metrics against both the official YAML and our Layer-A numbers.
