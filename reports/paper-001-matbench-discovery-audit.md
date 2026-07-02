# ReproLab Paper-001 — Independent Reproducibility Audit of Matbench Discovery

_Generated: 2026-07-02 08:08 UTC_

> Auto-assembled from tracked artifacts by `scripts/make_report.py`.

## 0. Executive summary

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
**CHGNet** on a deterministic 500-structure WBM subset (seed-42 sample of
`unique_prototypes`, ids committed in `layer_b_subset.csv`): initial structure → FIRE
relaxation with the upstream protocol (steps≤500, fmax=0.05, FrechetCellFilter) →
formation energy → scored through the *same* Layer A metric path. All thresholds were
pre-registered in `layer_b_plan.md` §7 **before** the run.

- **500/500 relaxed, 0 failures** — RTX 4090, mean 1.06 s/structure (median 0.99,
  max 6.16), 9.3 min total GPU; 477/500 converged within the 500-step cap (the
  published pipeline ran under the same cap)
- **median |Δe_form| = 0.03 meV/atom vs published** (pre-registered threshold: ≤10);
  p95 = 0.07, max = 1.08 meV/atom; 100% of structures within 10 meV/atom — despite a
  2023→2026 dependency gap (torch 1.11→2.11, ase 3.22→3.29, chgnet package 0.4.2
  loading the same 0.3.0 weights, 412,525 params verified)
- **100% stable/unstable classification agreement** (threshold: ≥95%); **zero flips**
  in either direction
- Discovery metrics computed from regenerated and published predictions are
  **identical** through both metric implementations (F1 0.584, MAE 0.067,
  TP/FP/TN/FN = 47/47/386/20 on this subset)
- GPU run-to-run variance bounded first on the 20-structure pre-smoke (two runs):
  median 0.000, max 0.232 meV/atom — far below the threshold, so deltas are
  interpretable
- Worst structure: wbm-2-42265 (S6Sr3), Δ = +1.1 meV/atom, classification unchanged

**Verdict: the published CHGNet predictions reproduce from model execution** on this
subset, to well within the published CSV's own rounding scale.

## Scope and limits

Layer A verifies that leaderboard metrics are correctly derived from the *published*
predictions (4/4 models exact). Layer B regenerates predictions for one model
(CHGNet) on a 500-structure deterministic subset — a small but valid audit of the
generation path, not a full leaderboard reproduction. Next steps: additional Layer B
models (ORB / MACE) or another paper. Full-WBM (257k) regeneration is out of scope
for v0.x.



## 1. Benchmark metadata

```
# ReproLab Paper-001 — benchmark metadata (single source of truth for the audit)
paper:
  title: A framework to evaluate machine learning crystal stability predictions
  authors: Riebesell, Goodall, Benner, et al.
  venue: Nature Machine Intelligence
  volume_pages: 7, 836-847
  year: 2025
  doi: 10.1038/s42256-025-01055-1
  preprint: arXiv:2308.14920

benchmark:
  name: Matbench Discovery
  repo: https://github.com/janosh/matbench-discovery
  repo_commit_pinned: eaa755066edccbc5224b0404369e626e7f2294fd  # HEAD at clone time 2026-07-02
  package_version: 1.3.1
  license: MIT
  leaderboard: https://matbench-discovery.materialsproject.org/
  figshare_article: https://figshare.com/articles/dataset/22715158
  domain: materials (ML interatomic potentials / crystal thermodynamic stability)

task_under_audit:
  name: discovery            # stable/unstable classification + energy regression
  test_task: IS2RE-SR        # initial structure -> relaxed energy (structure relaxation)
  stability_threshold_eV_per_atom: 0     # matbench_discovery.STABILITY_THRESHOLD
  max_error_threshold_eV_per_atom: 5.0   # preds with |e_form_pred-e_form_dft|>5 -> NaN(unstable)

# Column names in the WBM summary (ground truth) — from matbench_discovery/enums.py MbdKey
ground_truth:
  file: data/wbm/2023-12-13-wbm-summary.csv.gz   # bundled in clone; DataFiles.wbm_summary
  each_true_col: e_above_hull_mp2020_corrected_ppd_mp   # DFT energy above MP convex hull
  e_form_dft_col: e_form_per_atom_mp2020_corrected      # DFT formation energy (corrected)
  id_col: material_id
  uniq_proto_col: unique_prototype                      # boolean mask for uniq_protos subset

# First model to audit
primary_model:
  key: chgnet-0.3.0
  label: CHGNet
  pred_col: e_form_per_atom_chgnet
  pred_file: models/chgnet/chgnet-0.3.0/2023-12-21-wbm-IS2RE.csv.gz  # NOT in clone
  pred_file_url: https://figshare.com/files/52057526                # download at runtime
  yaml: models/chgnet/chgnet-0.3.0.yml                              # holds official metrics

# Official published metric values to reproduce (from models/chgnet/chgnet-0.3.0.yml)
official_metrics:
  unique_prototypes:   # leaderboard default subset
    F1: 0.613
    Precision: 0.514
    Recall: 0.758
    Accuracy: 0.851
    MAE: 0.063     # eV/atom
    RMSE: 0.103    # eV/atom
    R2: 0.689
    TP: 25313
    FP: 23955
    TN: 158159
    FN: 8061
    missing_preds: 0
  full_test_set:
    F1: 0.612
    MAE: 0.061
    RMSE: 0.1
    R2: 0.69
    TP: 32642
    FP: 29979
    TN: 182892
    FN: 11450
    missing_preds: 2
  most_stable_10k:
    F1: 0.92
    Precision: 0.851
    MAE: 0.063
    R2: 0.816

# Candidate second models to extend to (ideal line, Jul 4)
secondary_models:
  - key: mace-mp-0
    yaml: models/mace/mace-mp-0.yml
  - key: mace-mpa-0
    yaml: models/mace/mace-mpa-0.yml
  - key: sevennet-0
    yaml: models/sevennet/sevennet-0.yml
  - key: orb-v2
    yaml: models/orb/orb-v2.yml

```


## 2. Reproduction plan

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



## 3. Environment

# Environment

_Captured: 2026-07-02 05:09:27 UTC_

- **timestamp_utc**: `2026-07-02 05:09:27 UTC`
- **platform**: `Windows-10-10.0.26200-SP0`
- **python_version**: `3.11.9 (tags/v3.11.9:de54cf5, Apr  2 2024, 10:12:12) [MSC v.1938 64 bit (AMD64)]`
- **python_executable**: `C:\Users\07013\Desktop\0702fable\reprolab\.venv\Scripts\python.exe`
- **nvidia_smi**: `NVIDIA GeForce RTX 4090, 24564 MiB, 596.36`
- **git_vendor_commit**: `eaa755066edccbc5224b0404369e626e7f2294fd`

## pip freeze

```
annotated-types==0.7.0
anywidget==0.11.0
ase==3.29.0
asttokens==3.0.1
bibtexparser==1.4.4
certifi==2026.6.17
charset-normalizer==3.4.7
chgnet==0.4.2
click==8.4.2
colorama==0.4.6
comm==0.2.3
contourpy==1.3.3
cycler==0.12.1
Cython==3.2.8
decorator==5.3.1
executing==2.2.1
filelock==3.29.0
fonttools==4.63.0
fsspec==2026.4.0
gitdb==4.0.12
GitPython==3.1.50
idna==3.18
ipython==9.15.0
ipython_pygments_lexers==1.1.1
ipywidgets==8.1.8
jedi==0.20.0
Jinja2==3.1.6
joblib==1.5.3
jupyterlab_widgets==3.0.16
kiwisolver==1.5.0
lxml==6.1.1
MarkupSafe==3.0.3
matbench-discovery==1.3.1
matplotlib==3.11.0
matplotlib-inline==0.2.2
monty==2026.5.18
moyopy==0.13.0
mpmath==1.3.0
narwhals==2.23.0
networkx==3.6.1
numpy==2.4.6
nvidia-ml-py3==7.352.0
orjson==3.11.9
packaging==26.2
palettable==3.3.3
pandas==3.0.3
parso==0.8.7
pillow==12.3.0
platformdirs==4.10.0
plotly==6.8.0
prompt_toolkit==3.0.52
protobuf==7.35.1
psutil==7.2.2
psygnal==0.15.1
pure_eval==0.2.3
pydantic==2.13.4
pydantic_core==2.46.4
Pygments==2.20.0
pymatgen==2026.5.4
pymatgen-core==2026.5.18
pymatviz==0.18.0
pyparsing==3.3.2
python-dateutil==2.9.0.post0
PyYAML==6.0.3
requests==2.34.2
ruamel.yaml==0.18.17
ruamel.yaml.clib==0.2.15
scikit-learn==1.9.0
scipy==1.17.1
seaborn==0.13.2
sentry-sdk==2.64.0
six==1.17.0
smmap==5.0.3
spglib==2.7.0
stack-data==0.6.3
sympy==1.14.0
tabulate==0.10.0
threadpoolctl==3.6.0
torch==2.11.0+cu128
tqdm==4.68.3
traitlets==5.15.1
typing-inspection==0.4.2
typing_extensions==4.15.0
tzdata==2026.2
uncertainties==3.2.3
urllib3==2.7.0
wandb==0.28.0
wcwidth==0.8.2
widgetsnbextension==4.0.15
```



## 4. Metric check — metric_check-layer-b-chgnet-presmoke

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



## 4. Metric check — metric_check-layer-b-chgnet-smoke500

# Metric Check — Layer B: CHGNet regenerated predictions (n=500)

Vertical slice: model relaxation -> prediction CSV -> Layer A metric path. Generation protocol per upstream `test_chgnet_discovery.py` (FIRE, steps<=500, fmax=0.05, relax_cell, FrechetCellFilter). Scored with `compare_metrics.py` functions unchanged.

published preds: `models/chgnet/chgnet-0.3.0/2023-12-21-wbm-IS2RE.csv.gz` | regenerated: `experiments/layer-b/chgnet/smoke500-run1.jsonl.gz`


## Worst 15 structures by |Δ| (full data in experiments/)

| material_id | formula | n_sites | steps | conv | published | regenerated | Δ meV/atom | stable(pub) | stable(regen) | agree |
|---|---|---|---|---|---|---|---|---|---|---|
| wbm-2-42265 | S6Sr3 | 9 | 80 | y | -1.6900 | -1.6889 | +1.1 | U | U | ✓ |
| wbm-3-5904 | As4Gd2 | 6 | 37 | y | -0.9494 | -0.9488 | +0.6 | U | U | ✓ |
| wbm-2-14997 | Al4F8 | 12 | 93 | y | -3.2045 | -3.2040 | +0.5 | U | U | ✓ |
| wbm-2-45027 | Se6Sm2 | 8 | 49 | y | -1.4907 | -1.4904 | +0.3 | S | S | ✓ |
| wbm-4-16455 | Cl4H2Mg2 | 8 | 44 | y | -1.1990 | -1.1989 | +0.1 | U | U | ✓ |
| wbm-1-36458 | Au2Hg2O4 | 8 | 44 | y | -0.5065 | -0.5066 | -0.1 | U | U | ✓ |
| wbm-1-25586 | Li1Ni2Pb1 | 4 | 18 | y | 0.0417 | 0.0418 | +0.1 | U | U | ✓ |
| wbm-1-11292 | Co3Ir1 | 4 | 37 | y | 0.0611 | 0.0612 | +0.1 | U | U | ✓ |
| wbm-1-7045 | Al4C5Th2 | 11 | 41 | y | -0.1514 | -0.1515 | -0.1 | U | U | ✓ |
| wbm-4-24096 | Ir1Ni2Zr1 | 4 | 34 | y | -0.4924 | -0.4923 | +0.1 | U | U | ✓ |
| wbm-5-5141 | Au1Cr1Fe2 | 4 | 16 | y | 0.2683 | 0.2684 | +0.1 | U | U | ✓ |
| wbm-1-21801 | Ho2I6 | 8 | 49 | y | -1.6823 | -1.6824 | -0.1 | U | U | ✓ |
| wbm-4-18193 | As2Co2Li1Nd1 | 6 | 30 | y | -0.6785 | -0.6784 | +0.1 | U | U | ✓ |
| wbm-4-6677 | Cl6Fe1Rb2 | 9 | 35 | y | -1.6191 | -1.6190 | +0.1 | S | S | ✓ |
| wbm-4-15908 | H8Nd2Pt2 | 12 | 42 | y | -0.5504 | -0.5503 | +0.1 | S | S | ✓ |

## Agreement stats (pre-registered thresholds: median |Δ|<=10 meV/atom, classification agreement >=95%)

- n scored = 500
- median |Δ| = **0.03 meV/atom** (threshold: <=10)
- mean |Δ| = 0.03 | p95 |Δ| = 0.07 | max |Δ| = 1.08 meV/atom
- within 10 meV/atom: 100.0%
- classification agreement: **100.0%** (threshold: >=95%)
- flips stable->unstable (pub->regen): 0 | unstable->stable: 0

## Discovery metrics on this subset via the Layer A path (n=500 — subset-level, not leaderboard-comparable)

| metric | regenerated (indep) | regenerated (upstream_fn) | published (indep) | published (upstream_fn) |
|---|---|---|---|---|
| F1 | 0.584 | 0.584 | 0.584 | 0.584 |
| Precision | 0.500 | 0.500 | 0.500 | 0.500 |
| Recall | 0.701 | 0.701 | 0.701 | 0.701 |
| Accuracy | 0.866 | 0.866 | 0.866 | 0.866 |
| MAE | 0.067 | 0.067 | 0.067 | 0.067 |
| RMSE | 0.104 | 0.104 | 0.104 | 0.104 |
| TP | 47 | 47 | 47 | 47 |
| FP | 47 | 47 | 47 | 47 |
| TN | 386 | 386 | 386 | 386 |
| FN | 20 | 20 | 20 | 20 |



## 4. Metric check — metric_check-mace-mp-0

# Metric Check — MACE-MP-0

repo commit: `C:\Users\07013\Desktop\0702fable\reprolab\vendor\matbench-discovery` | pred_col: `e_form_per_atom_mace` | filtered(|Δ|>5): 0 | missing_preds: 38


## unique_prototypes  (n=215,488)

| metric | official | reproduced | upstream_fn | Δ(off−repro) | pass |
|---|---|---|---|---|---|
| F1 | 0.669 | 0.669 | 0.669 | -0.000 | ✓ |
| Precision | 0.577 | 0.577 | 0.577 | -0.000 | ✓ |
| Recall | 0.796 | 0.796 | 0.796 | -0.000 | ✓ |
| Accuracy | 0.878 | 0.878 | 0.878 | -0.000 | ✓ |
| MAE | 0.057 | 0.057 | 0.057 | 0.000 | ✓ |
| RMSE | 0.101 | 0.101 | 0.101 | -0.000 | ✓ |
| R2 | 0.697 | 0.697 | 0.697 | -0.000 | ✓ |
| TP | 26582.000 | 26582 | 26582 | 0.000 | ✓ |
| FP | 19457.000 | 19457 | 19457 | 0.000 | ✓ |
| TN | 162657.000 | 162657 | 162657 | 0.000 | ✓ |
| FN | 6792.000 | 6792 | 6792 | 0.000 | ✓ |

## full_test_set  (n=256,963)

| metric | official | reproduced | upstream_fn | Δ(off−repro) | pass |
|---|---|---|---|---|---|
| F1 | 0.668 | 0.668 | 0.668 | 0.000 | ✓ |
| Precision | 0.583 | 0.583 | 0.583 | -0.000 | ✓ |
| Recall | 0.781 | 0.781 | 0.781 | 0.000 | ✓ |
| Accuracy | 0.867 | 0.867 | 0.867 | 0.000 | ✓ |
| MAE | 0.055 | 0.055 | 0.055 | 0.000 | ✓ |
| RMSE | 0.099 | 0.099 | 0.099 | 0.000 | ✓ |
| R2 | 0.698 | 0.698 | 0.698 | -0.000 | ✓ |
| TP | 34420.000 | 34420 | 34420 | 0.000 | ✓ |
| FP | 24576.000 | 24576 | 24576 | 0.000 | ✓ |
| TN | 188295.000 | 188295 | 188295 | 0.000 | ✓ |
| FN | 9672.000 | 9672 | 9672 | 0.000 | ✓ |



## 4. Metric check — metric_check-orb-v2

# Metric Check — ORB v2

repo commit: `vendor/matbench-discovery` | pred_col: `e_form_per_atom_orb` | filtered(|Δ|>5): 2 | missing_preds: 2


## unique_prototypes  (n=215,488)

| metric | official | reproduced | upstream_fn | Δ(off−repro) | pass |
|---|---|---|---|---|---|
| F1 | 0.880 | 0.880 | 0.880 | -0.000 | ✓ |
| Precision | 0.924 | 0.924 | 0.924 | 0.000 | ✓ |
| Recall | 0.841 | 0.841 | 0.841 | 0.000 | ✓ |
| Accuracy | 0.965 | 0.965 | 0.965 | 0.000 | ✓ |
| MAE | 0.028 | 0.028 | 0.028 | -0.000 | ✓ |
| RMSE | 0.077 | 0.077 | 0.077 | -0.000 | ✓ |
| R2 | 0.824 | 0.824 | 0.824 | -0.000 | ✓ |
| TP | 28055.000 | 28055 | 28055 | 0.000 | ✓ |
| FP | 2323.000 | 2323 | 2323 | 0.000 | ✓ |
| TN | 179791.000 | 179791 | 179791 | 0.000 | ✓ |
| FN | 5319.000 | 5319 | 5319 | 0.000 | ✓ |

## full_test_set  (n=256,963)

| metric | official | reproduced | upstream_fn | Δ(off−repro) | pass |
|---|---|---|---|---|---|
| F1 | 0.858 | 0.858 | 0.858 | -0.000 | ✓ |
| Precision | 0.906 | 0.906 | 0.906 | -0.000 | ✓ |
| Recall | 0.815 | 0.815 | 0.815 | -0.000 | ✓ |
| Accuracy | 0.954 | 0.954 | 0.954 | 0.000 | ✓ |
| MAE | 0.028 | 0.028 | 0.028 | -0.000 | ✓ |
| RMSE | 0.078 | 0.078 | 0.078 | 0.000 | ✓ |
| R2 | 0.814 | 0.814 | 0.814 | 0.000 | ✓ |
| TP | 35949.000 | 35949 | 35949 | 0.000 | ✓ |
| FP | 3725.000 | 3725 | 3725 | 0.000 | ✓ |
| TN | 209146.000 | 209146 | 209146 | 0.000 | ✓ |
| FN | 8143.000 | 8143 | 8143 | 0.000 | ✓ |



## 4. Metric check — metric_check-sevennet

# Metric Check — SevenNet-0

repo commit: `C:\Users\07013\Desktop\0702fable\reprolab\vendor\matbench-discovery` | pred_col: `e_form_per_atom_sevennet` | filtered(|Δ|>5): 3 | missing_preds: 3


## unique_prototypes  (n=215,488)

| metric | official | reproduced | upstream_fn | Δ(off−repro) | pass |
|---|---|---|---|---|---|
| F1 | 0.724 | 0.724 | 0.724 | -0.000 | ✓ |
| Precision | 0.650 | 0.650 | 0.650 | 0.000 | ✓ |
| Recall | 0.818 | 0.818 | 0.818 | -0.000 | ✓ |
| Accuracy | 0.904 | 0.904 | 0.904 | 0.000 | ✓ |
| MAE | 0.048 | 0.048 | 0.048 | -0.000 | ✓ |
| RMSE | 0.092 | 0.092 | 0.092 | -0.000 | ✓ |
| R2 | 0.750 | 0.750 | 0.750 | -0.000 | ✓ |
| TP | 27304.000 | 27304 | 27304 | 0.000 | ✓ |
| FP | 14703.000 | 14703 | 14703 | 0.000 | ✓ |
| TN | 167411.000 | 167411 | 167411 | 0.000 | ✓ |
| FN | 6070.000 | 6070 | 6070 | 0.000 | ✓ |

## full_test_set  (n=256,963)

| metric | official | reproduced | upstream_fn | Δ(off−repro) | pass |
|---|---|---|---|---|---|
| F1 | 0.719 | 0.719 | 0.719 | 0.000 | ✓ |
| Precision | 0.653 | 0.653 | 0.653 | 0.000 | ✓ |
| Recall | 0.800 | 0.800 | 0.800 | 0.000 | ✓ |
| Accuracy | 0.893 | 0.893 | 0.893 | 0.000 | ✓ |
| MAE | 0.046 | 0.046 | 0.046 | -0.000 | ✓ |
| RMSE | 0.090 | 0.090 | 0.090 | 0.000 | ✓ |
| R2 | 0.750 | 0.750 | 0.750 | -0.000 | ✓ |
| TP | 35259.000 | 35259 | 35259 | 0.000 | ✓ |
| FP | 18765.000 | 18765 | 18765 | 0.000 | ✓ |
| TN | 194106.000 | 194106 | 194106 | 0.000 | ✓ |
| FN | 8833.000 | 8833 | 8833 | 0.000 | ✓ |



## 4. Metric check — metric_check

# Metric Check — CHGNet

repo commit: `C:\Users\07013\Desktop\0702fable\reprolab\vendor\matbench-discovery` | pred_col: `e_form_per_atom_chgnet` | filtered(|Δ|>5): 2 | missing_preds: 2


## unique_prototypes  (n=215,488)

| metric | official | reproduced | upstream_fn | Δ(off−repro) | pass |
|---|---|---|---|---|---|
| F1 | 0.613 | 0.613 | 0.613 | 0.000 | ✓ |
| Precision | 0.514 | 0.514 | 0.514 | 0.000 | ✓ |
| Recall | 0.758 | 0.758 | 0.758 | -0.000 | ✓ |
| Accuracy | 0.851 | 0.851 | 0.851 | -0.000 | ✓ |
| MAE | 0.063 | 0.063 | 0.063 | -0.000 | ✓ |
| RMSE | 0.103 | 0.103 | 0.103 | 0.000 | ✓ |
| R2 | 0.689 | 0.689 | 0.689 | -0.000 | ✓ |
| TP | 25313.000 | 25313 | 25313 | 0.000 | ✓ |
| FP | 23955.000 | 23955 | 23955 | 0.000 | ✓ |
| TN | 158159.000 | 158159 | 158159 | 0.000 | ✓ |
| FN | 8061.000 | 8061 | 8061 | 0.000 | ✓ |

## full_test_set  (n=256,963)

| metric | official | reproduced | upstream_fn | Δ(off−repro) | pass |
|---|---|---|---|---|---|
| F1 | 0.612 | 0.612 | 0.612 | 0.000 | ✓ |
| Precision | 0.521 | 0.521 | 0.521 | -0.000 | ✓ |
| Recall | 0.740 | 0.740 | 0.740 | -0.000 | ✓ |
| Accuracy | 0.839 | 0.839 | 0.839 | 0.000 | ✓ |
| MAE | 0.061 | 0.061 | 0.061 | -0.000 | ✓ |
| RMSE | 0.100 | 0.100 | 0.100 | -0.000 | ✓ |
| R2 | 0.690 | 0.690 | 0.690 | -0.000 | ✓ |
| TP | 32642.000 | 32642 | 32642 | 0.000 | ✓ |
| FP | 29979.000 | 29979 | 29979 | 0.000 | ✓ |
| TN | 182892.000 | 182892 | 182892 | 0.000 | ✓ |
| FN | 11450.000 | 11450 | 11450 | 0.000 | ✓ |



## 4b. Layer C — statistical audit of the leaderboard

# Layer C — Statistical audit of the Matbench Discovery leaderboard

Subset: `unique_prototypes` (n=215,488); models: CHGNet, SevenNet-0, MACE-MP-0, ORB v2; paired bootstrap B=2000, seed=42; each_pred built by the exact Layer A path (`compare_metrics.build_each_pred`). **Exploratory analysis** (not pre-registered, unlike Layer B).


## Q1 — Uncertainty and ranking significance (not reported upstream)

| model | F1 | 95% CI | CI width | MAE eV/atom | 95% CI |
|---|---|---|---|---|---|
| ORB v2 | 0.8801 | [0.8775, 0.8827] | 0.0052 | 0.0282 | [0.0279, 0.0285] |
| SevenNet-0 | 0.7244 | [0.7207, 0.7281] | 0.0074 | 0.0484 | [0.0481, 0.0487] |
| MACE-MP-0 | 0.6695 | [0.6657, 0.6733] | 0.0076 | 0.0569 | [0.0566, 0.0573] |
| CHGNet | 0.6126 | [0.6087, 0.6165] | 0.0078 | 0.0635 | [0.0631, 0.0638] |

| pair (better vs worse) | ΔF1 | 95% CI | P(flip) |
|---|---|---|---|
| ORB v2 vs SevenNet-0 | +0.1557 | [+0.1519, +0.1596] | 0 |
| ORB v2 vs MACE-MP-0 | +0.2107 | [+0.2066, +0.2147] | 0 |
| ORB v2 vs CHGNet | +0.2675 | [+0.2634, +0.2718] | 0 |
| SevenNet-0 vs MACE-MP-0 | +0.0550 | [+0.0515, +0.0582] | 0 |
| SevenNet-0 vs CHGNet | +0.1118 | [+0.1083, +0.1153] | 0 |
| MACE-MP-0 vs CHGNet | +0.0569 | [+0.0536, +0.0601] | 0 |

Context — leaderboard resolution: the widest 95% CI measured here is 0.0078 F1. On the full leaderboard at this commit (60 models with a uniq-protos F1), **43 of 59 adjacent pairs are separated by less than that CI width**, i.e. their published order is unlikely to be statistically resolvable without a paired significance test:
  - EquiformerV3+DeNS-OAM vs EquFlashV2: ΔF1 = 0.002
  - EquFlashV2 vs TACE-OAM-RRA-Preview: ΔF1 = 0.001
  - TACE-OAM-RRA-Preview vs eSEN-30M-OAM: ΔF1 = 0.003
  - eSEN-30M-OAM vs PET-OAM-XL: ΔF1 = 0.001
  - PET-OAM-XL vs MatRIS-10M-OAM: ΔF1 = 0.003
  - MatRIS-10M-OAM vs EquFlash: ΔF1 = 0.002
  - EquFlash vs eqV2 M: ΔF1 = 0.002
  - eqV2 M vs TACE-OAM-L: ΔF1 = 0.007
  - TACE-OAM-L vs Nequip-OAM-XL: ΔF1 = 0.004
  - Nequip-OAM-XL vs SevenNet-Omni-i12: ΔF1 = 0.000
  - SevenNet-Omni-i12 vs ORB v3: ΔF1 = 0.001
  - ORB v3 vs AlphaNet-v1-OAM: ΔF1 = 0.004
  - AlphaNet-v1-OAM vs SevenNet-MF-ompa: ΔF1 = 0.000
  - SevenNet-MF-ompa vs Allegro-OAM-L: ΔF1 = 0.006
  - Allegro-OAM-L vs Nequip-OAM-L: ΔF1 = 0.002
  - Nequip-OAM-L vs DPA3-v2-OpenLAM: ΔF1 = 0.003
  - DPA3-v2-OpenLAM vs TACE-v1-OAM-M: ΔF1 = 0.001
  - TACE-v1-OAM-M vs DPA-3.1-3M-FT: ΔF1 = 0.005
  - DPA-3.1-3M-FT vs DPA3-v1-OpenLAM: ΔF1 = 0.001
  - DPA3-v1-OpenLAM vs GRACE-2L-OAM-L: ΔF1 = 0.000
  - GRACE-2L-OAM-L vs GRACE-2L-OAM: ΔF1 = 0.003
  - GRACE-2L-OAM vs ORB v2: ΔF1 = 0.000
  - EquiformerV3+DeNS-MP vs MatterSim v1 5M: ΔF1 = 0.001
  - MatterSim v1 5M vs DPA-4.0.1-Pro-MPtrj: ΔF1 = 0.005
  - DPA-4.0.1-Pro-MPtrj vs MACE-MPA-0: ΔF1 = 0.005
  - MACE-MPA-0 vs DPA-4.0-Pro-MPtrj: ΔF1 = 0.002
  - DPA-4.0-Pro-MPtrj vs MatRIS-10M-MP: ΔF1 = 0.003
  - eSEN-30M-MP vs GNoME: ΔF1 = 0.002
  - GNoME vs GRACE-1L-OAM: ΔF1 = 0.005
  - eqV2 S DeNS vs MatRIS v0.5.0 MPtrj: ΔF1 = 0.006
  - MatRIS v0.5.0 MPtrj vs DPA-3.1-MPtrj: ΔF1 = 0.006
  - DPA-3.1-MPtrj vs AlphaNet-v1-MPtrj: ΔF1 = 0.004
  - DPA3-v2-MPtrj vs Eqnorm MPtrj: ΔF1 = 0.000
  - DPA3-v1-MPtrj vs ORB v2 MPtrj: ΔF1 = 0.000
  - ORB v2 MPtrj vs Nequip-MP-L: ΔF1 = 0.004
  - Nequip-MP-L vs SevenNet-l3i5: ΔF1 = 0.001
  - Allegro-MP-L vs Nequix MP: ΔF1 = 0.000
  - Nequix MP vs Nequix MP PFT: ΔF1 = 0.003
  - ESNet vs M3GNet: ΔF1 = 0.003
  - M3GNet vs ALIGNN: ΔF1 = 0.002
  - MEGNet vs CGCNN: ΔF1 = 0.003
  - CGCNN vs CGCNN+P: ΔF1 = 0.007
  - BOWSR vs AlchemBERT: ΔF1 = 0.002

(Caveat: CI width varies by model; a definitive statement needs the paired bootstrap on each pair's prediction files, as done above for four models. The point stands that the leaderboard reports no uncertainty at all while many gaps are of this order.)

## Q2 — Sensitivity to the 0 eV/atom stability threshold

Same threshold applied to truth and predictions (leaderboard convention in `stable_metrics`). DFT hull energies themselves carry O(10 meV/atom) uncertainty, so ranking stability inside this band matters.

| τ (meV/atom) | ORB v2 | SevenNet-0 | MACE-MP-0 | CHGNet | ranking |
|---|---|---|---|---|---|
| -100 | 0.8803 | 0.7266 | 0.6406 | 0.6367 | ORB v2 > SevenNet-0 > MACE-MP-0 > CHGNet |
| -75 | 0.8773 | 0.7126 | 0.6321 | 0.6145 | ORB v2 > SevenNet-0 > MACE-MP-0 > CHGNet |
| -50 | 0.8787 | 0.7052 | 0.6303 | 0.6005 | ORB v2 > SevenNet-0 > MACE-MP-0 > CHGNet |
| -40 | 0.8775 | 0.7073 | 0.6351 | 0.5990 | ORB v2 > SevenNet-0 > MACE-MP-0 > CHGNet |
| -30 | 0.8783 | 0.7076 | 0.6409 | 0.5988 | ORB v2 > SevenNet-0 > MACE-MP-0 > CHGNet |
| -20 | 0.8816 | 0.7126 | 0.6506 | 0.6007 | ORB v2 > SevenNet-0 > MACE-MP-0 > CHGNet |
| -10 | 0.8820 | 0.7163 | 0.6554 | 0.6007 | ORB v2 > SevenNet-0 > MACE-MP-0 > CHGNet |
| -5 | 0.8794 | 0.7195 | 0.6614 | 0.6058 | ORB v2 > SevenNet-0 > MACE-MP-0 > CHGNet |
| +0 | 0.8801 | 0.7244 | 0.6695 | 0.6126 | ORB v2 > SevenNet-0 > MACE-MP-0 > CHGNet |
| +5 | 0.8817 | 0.7361 | 0.6820 | 0.6264 | ORB v2 > SevenNet-0 > MACE-MP-0 > CHGNet |
| +10 | 0.8853 | 0.7479 | 0.6970 | 0.6419 | ORB v2 > SevenNet-0 > MACE-MP-0 > CHGNet |
| +20 | 0.8942 | 0.7722 | 0.7274 | 0.6747 | ORB v2 > SevenNet-0 > MACE-MP-0 > CHGNet |
| +30 | 0.9028 | 0.7944 | 0.7562 | 0.7073 | ORB v2 > SevenNet-0 > MACE-MP-0 > CHGNet |
| +40 | 0.9095 | 0.8122 | 0.7775 | 0.7351 | ORB v2 > SevenNet-0 > MACE-MP-0 > CHGNet |
| +50 | 0.9167 | 0.8274 | 0.7984 | 0.7628 | ORB v2 > SevenNet-0 > MACE-MP-0 > CHGNet |
| +75 | 0.9288 | 0.8612 | 0.8367 | 0.8120 | ORB v2 > SevenNet-0 > MACE-MP-0 > CHGNet |
| +100 | 0.9385 | 0.8867 | 0.8675 | 0.8487 | ORB v2 > SevenNet-0 > MACE-MP-0 > CHGNet |

The τ=0 ranking is unchanged at every swept threshold in [-100, +100] meV/atom.

## Q3 — Error correlation and joint blind spots

Signed formation-energy errors (e_form_pred − e_form_dft), common non-NaN rows (n=215,453).

| Pearson | CHGNet | SevenNet-0 | MACE-MP-0 | ORB v2 |
|---|---|---|---|---|
| CHGNet | 1.000 | 0.765 | 0.764 | 0.449 |
| SevenNet-0 | 0.765 | 1.000 | 0.765 | 0.507 |
| MACE-MP-0 | 0.764 | 0.765 | 1.000 | 0.431 |
| ORB v2 | 0.449 | 0.507 | 0.431 | 1.000 |

| Spearman | CHGNet | SevenNet-0 | MACE-MP-0 | ORB v2 |
|---|---|---|---|---|
| CHGNet | 1.000 | 0.667 | 0.677 | 0.157 |
| SevenNet-0 | 0.667 | 1.000 | 0.653 | 0.231 |
| MACE-MP-0 | 0.677 | 0.653 | 1.000 | 0.187 |
| ORB v2 | 0.157 | 0.231 | 0.187 | 1.000 |

- Among the 33,374 DFT-stable structures, **3.59%** are missed (FN) by *all four* models simultaneously; under error independence this would be 0.14% (joint-miss lift **25x**). Per-model miss rates: CHGNet 24.2%, SevenNet-0 18.2%, MACE-MP-0 20.4%, ORB v2 15.9%.
- In the near-hull band |E_hull| ≤ 50 meV/atom (n=66,576), all four models misclassify the same structure 2.61% of the time vs 0.21% under independence (lift 12x).
- Unique true positives (stable materials found by that model and missed by the other three): CHGNet 341, SevenNet-0 361, MACE-MP-0 388, ORB v2 1,886.

## Limitations

- Bootstrap treats WBM as an i.i.d. sample; WBM structures are generated by element substitution from shared seeds, so effective sample size is somewhat smaller than n — CIs here are, if anything, slightly narrow.
- Threshold sweep reuses the same data at every τ (no multiple-comparison correction); it is a sensitivity analysis, not a hypothesis test.
- Analyses are exploratory and were designed after Layers A/B; they should be treated as descriptive audit findings, not confirmatory statistics.



## 4c. Layer C — ground-truth hull recomputation

# Layer C (ground truth) — e_above_hull recomputed from the MP phase diagram

Subset: the committed Layer B ids (n=500); CSE source `data/wbm/2022-10-19-wbm-computed-structure-entries.jsonl.gz`; hull source `data/mp/2023-02-07-ppd-mp.pkl.gz` (2023 pickle) unpickled under pymatgen 2026.5.18. Corrections: entries shipped with adjustments for 0/500; MP2020 applied by us to the rest; 0 dropped by compatibility processing; 0 hull lookups failed.

## Result

- compared: **500/500** subset structures
- median |Δ| = **0.0003 meV/atom** | p95 = 0.0005 | max = 216.5996 meV/atom
- within 0.1 meV/atom: 99.4% | within 1 meV/atom: 99.4%
- stable/unstable label (<=0) agreement with published column: 99.6%

| material_id | published | recomputed | Δ meV/atom |
|---|---|---|---|
| wbm-2-28782 | 0.024147 | 0.240747 | +216.5996 |
| wbm-4-28450 | -0.028060 | 0.098273 | +126.3330 |
| wbm-4-15908 | 0.032848 | -0.086485 | -119.3332 |
| wbm-1-57937 | 0.024024 | 0.024024 | +0.0005 |
| wbm-3-53078 | -0.120219 | -0.120219 | -0.0005 |
| wbm-1-57885 | 0.191865 | 0.191865 | -0.0005 |
| wbm-4-12603 | 0.041207 | 0.041207 | -0.0005 |
| wbm-1-1604 | 0.368311 | 0.368311 | -0.0005 |
| wbm-1-37417 | 0.666768 | 0.666768 | +0.0005 |
| wbm-3-4711 | 0.204088 | 0.204088 | -0.0005 |

## Diagnosis of the 3 outliers (`layer_c_gt_diagnose.py`, logged in run_log)

For all three, the e_above_hull delta equals the **e_form delta to <0.001 meV/atom**
(+216.601, +126.307, −119.303), so the phase-diagram lookup is not implicated — the
entire discrepancy is in the **MP2020 energy-correction assignment**, and all three
are cases where that assignment hinges on pymatgen's oxidation-state guessing:

| id | formula | our correction | interpretation |
|---|---|---|---|
| wbm-2-28782 | SrBrN3 | Br anion only (−1.068 eV) | upstream value implies an additional/different anion (nitride) correction |
| wbm-4-28450 | PaIO | oxide (−1.374 eV) after explicit pymatgen warning "Failed to guess oxidation states… assigning anion correction to only the most electronegative atom" | heuristic fallback, version-dependent |
| wbm-4-15908 | NdH4Pt | hydride H (−1.432 eV) | upstream value implies no hydride correction was applied |

**Finding:** the benchmark's ground-truth column embeds correction heuristics that are
not stable across pymatgen versions. Under pymatgen 2026.5, 3/500 subset structures
(0.6%) shift by 119–217 meV/atom and 2/500 stability labels flip relative to the
published column. 497/500 reproduce to ≤0.001 meV/atom (median 0.0003), and the 2023
`PatchedPhaseDiagram` pickle unpickles cleanly under pymatgen 2026. Reproducing the
ground truth *bit-exactly* therefore requires the correction behavior of the original
2022/2023-era environment — a version-pinning requirement the benchmark does not
currently state. At leaderboard scale, ~0.4–0.6% label ambiguity is material when
adjacent models are separated by ΔF1 of 0.001–0.003 (see the statistical audit).



## 5. Failure notes

# Failure Notes — Paper-001

Classified blockers and discrepancies. Each entry: what, where, suspected cause,
status. A metric that does not reproduce is a *finding*, not a dead end.

## Classification tags
- `env` — dependency / install / platform issue
- `data` — data access, download, or schema drift
- `metric` — reproduced value differs from official
- `interp` — evaluation assumption that is easy to get wrong (documented, not a bug)

## Known evaluation assumptions to watch (interp) — identified 2026-07-02
- **5 eV/atom error filter** (`data.py:291-305`): predictions with
  `|e_form_pred − e_form_dft| > 5` are dropped to NaN *before* scoring and then
  counted as "predicted unstable". Skipping this changes F1/MAE. Reproduced in
  `compare_metrics.py`.
- **NaN = unstable** (`metrics/discovery.py`, `fillna=True`): missing predictions are
  scored as unstable, not excluded from classification (but excluded from MAE/RMSE/R²).
- **3-decimal rounding** of the merged frame (`preds/discovery.py:28`) happens before
  metrics are computed; must round to match the YAML.
- **Subset order**: filter is applied on the full set, *then* the `unique_prototypes`
  mask is applied.
- **Step-cap non-convergence is part of the published protocol** (Layer B): 23/500
  smoke structures (4.6%) hit the 500-step FIRE cap without reaching fmax ≤ 0.05.
  The upstream generation script ran under the same cap, so the published predictions
  contain the same regime; regenerated e_form still agreed to ≤1.1 meV/atom and
  classification agreement was 100%. Not a defect — an evaluation assumption to state
  when describing Layer B.

## Findings so far (2026-07-02)

- **[env] PyPI wheel ≠ GitHub HEAD under the same version `1.3.1`.** The installed
  wheel has a *flat* layout (`matbench_discovery/metrics.py`, `preds.py`, `slurm.py`,
  `figshare/`), while the repo HEAD (commit `eaa7550`) has a restructured *package*
  layout (`metrics/discovery.py`, `preds/discovery.py`, `hpc.py`, `remote/`). Same
  version string, divergent code and import paths. Consequence: `pip install
  matbench-discovery` alone does not reproduce the repo's evaluation entrypoints; the
  repo scripts' imports (`from matbench_discovery.metrics.discovery import ...`) fail
  against the wheel. **Mitigation:** we audit the *cloned repo at the pinned commit*
  and use pip only for dependencies (`compare_metrics.py` prepends the clone to
  `sys.path`). This is a reproducibility observation to include in the report.

- **[env] Local Anaconda base Python is broken** (prefix resolves to CWD → venv fails).
  Not an upstream issue; used Store Python 3.11.9 instead. Documented so the env is
  reproducible.

- **[data] `pred_file_url` is WAF-blocked for naive downloaders.** The model YAML lists
  `pred_file_url: https://figshare.com/files/52057526`. A plain GET (urllib) returned a
  **0-byte** body → `pandas EmptyDataError`. The working endpoint is the Figshare API:
  `https://api.figshare.com/v2/file/download/52057526`. Upstream `remote/fetch.py`
  rewrites the URL internally, so users of the package don't see this — but an
  independent auditor hitting the URL directly does. `compare_metrics.py` now applies
  the same rewrite and validates the gzip magic bytes. Reproducibility note for report.

- **[env] Transient native crash (0xC0000005) on the download+compute run.** The first
  SevenNet run — the one that had to download the prediction CSV — hard-crashed with a
  Windows access violation and no Python traceback (exit 3221225477, ~9 s). The
  downloaded file was intact (2.62 MB, valid gzip). Re-running with the file cached
  succeeded twice (direct + wrapper) with identical, exact-match results. Not a data or
  metric defect; a native-layer flake correlated with doing an in-process HTTPS download
  immediately before heavy numpy/pandas work. **Mitigation if it recurs (e.g. MACE):**
  pre-download the CSV in a separate step, then run the compute (the file-exists check in
  `ensure_preds` makes the compute run skip the download).

- **[interp] Ground-truth e_above_hull is not pymatgen-version-independent.**
  (Found 2026-07-02, Layer C ground-truth audit.) Recomputing
  `e_above_hull_mp2020_corrected_ppd_mp` from the published CSEs + MP2020
  compatibility + the published 2023 `PatchedPhaseDiagram` pickle reproduces
  **497/500** subset values to ≤0.001 meV/atom under pymatgen 2026.5 — but 3/500
  shift by 119–217 meV/atom and **2/500 stability labels flip**. Diagnosis
  (`layer_c_gt_diagnose.py`): the e_form delta accounts for the entire e_hull delta,
  i.e. the discrepancy is in the **MP2020 anion-correction assignment**, which hinges
  on oxidation-state guessing heuristics that drift across pymatgen versions
  (SrBrN3: nitride-vs-Br ambiguity; PaIO: explicit "failed to guess oxidation states"
  fallback; NdH4Pt: hydride correction applied by us, not upstream). Bit-exact ground
  truth requires the 2022/2023-era pymatgen behavior — unstated upstream. Side result:
  the 2023 phase-diagram *pickle* unpickles cleanly under pymatgen 2026.5.
  See `layer_c_gt_hull_check.md`.

- **[data] Stale md5 in `data-files.yml` for `wbm_initial_structures` — and upstream
  never checks it.** (Found 2026-07-02, Layer B preflight.) The registry at the pinned
  commit declares `md5: ff2c40a3a7bf65468852b67f0dbc67df` for
  `wbm/2022-10-19-wbm-init-structs.jsonl.gz` (Figshare file `53161835`), but the
  Figshare API reports `computed_md5: b809f101dd42a745ec2baabe7eb16f11` (size
  49,537,334 B) for that file id — our download matched Figshare exactly. The declared
  md5 actually belongs to a *different, older* artifact in the same Figshare article:
  `2022-10-19-wbm-init-structs.json.bz2` (file id `40344466`). Root cause is upstream:
  the download path (`remote/fetch.py::download_file`) performs **no md5 verification**,
  so the stale value can never trip their own pipeline — only independent auditors who
  trust the YAML. **Mitigation:** `download_datafile.py --expect-md5 <figshare
  computed_md5>` (override logged in `run_log.md`). Report-worthy: checksum metadata
  that is published but unverified drifts silently.

- **[env] `ruamel.yaml` 0.19.1 breaks `pymatgen` config loading (via `monty.loadfn`).**
  (Found 2026-07-02, Layer B scoring.) `import pymatgen.entries.computed_entries`
  cascades into `pymatgen.io.vasp.sets`, which loads YAML configs through
  `monty.serialization.loadfn` → ruamel; with ruamel.yaml 0.19.1 + monty 2026.5.18 +
  pymatgen 2026.5.4 this dies with `AttributeError: 'YAML' object has no attribute
  'check_token'`. Layer A never imported pymatgen, so the venv looked healthy until
  Layer B. **Mitigation:** pin `ruamel.yaml<0.19` (installed 0.18.17); import then
  succeeds. Another instance of silent dependency drift breaking a published pipeline.

- **[env] `run_command.py` needs an absolute path to the child interpreter on Windows.**
  Invoking the wrapper with a *relative* `.venv/Scripts/python.exe` as the wrapped
  command fails before logging (`WinError 2`, `CreateProcess` does not resolve
  forward-slash relative executables). Not an upstream issue; re-run with the absolute
  venv path (as the README commands now do). Noted 2026-07-02 during the ORB run.

## Open discrepancies
**None (4 of 4 models).** Layer A reproduced the official YAML exactly for **CHGNet**,
**SevenNet-0**, **MACE-MP-0**, and **ORB v2** on both `unique_prototypes` and
`full_test_set` — every fraction to 3 dp and every integer confusion count (TP/FP/TN/FN)
identical, via both an independent re-implementation and the upstream `stable_metrics`.
The pipeline matches `missing_preds` in both regimes: outlier-filter-driven (CHGNet 2,
SevenNet 3, ORB v2 2) and genuine-NaN-driven (MACE 38 full / 34 uniq, filter dropped 0).
The ORB v2 run (pre-download + compute split) completed with no new blockers. See
`metric_check.md`, `metric_check-sevennet.md`, `metric_check-mace-mp-0.md`,
`metric_check-orb-v2.md`.



## 6. Run log (tail)

$ C:\Users\07013\Desktop\0702fable\reprolab\.venv\Scripts\python.exe scripts/download_datafile.py --name mp_patched_phase_diagram
```

- exit code: **0**  | duration: 113.3s  | raw log: `logs/cmd-20260702-080239.log`

output tail:
```
downloading mp_patched_phase_diagram: https://api.figshare.com/v2/file/download/48241624 -> C:\Users\07013\Desktop\0702fable\reprolab\vendor\matbench-discovery\data\mp\2023-02-07-ppd-mp.pkl.gz
downloaded 220.0 MB
md5 OK (60d19d691fa1d338aa496a40a9641bef): C:\Users\07013\Desktop\0702fable\reprolab\vendor\matbench-discovery\data\mp\2023-02-07-ppd-mp.pkl.gz
```

### 2026-07-02 08:04 UTC — layerC-GT download wbm CSEs (87MB, figshare computed_md5 - YAML md5 stale, see failure_notes)

```
$ C:\Users\07013\Desktop\0702fable\reprolab\.venv\Scripts\python.exe scripts/download_datafile.py --name wbm_computed_structure_entries --expect-md5 655b7a9c368e136dd8747f1ef8002e7a
```

- exit code: **0**  | duration: 27.9s  | raw log: `logs/cmd-20260702-080433.log`

output tail:
```
downloading wbm_computed_structure_entries: https://api.figshare.com/v2/file/download/53161832 -> C:\Users\07013\Desktop\0702fable\reprolab\vendor\matbench-discovery\data\wbm\2022-10-19-wbm-computed-structure-entries.jsonl.gz
downloaded 86.5 MB
md5 OK (655b7a9c368e136dd8747f1ef8002e7a): C:\Users\07013\Desktop\0702fable\reprolab\vendor\matbench-discovery\data\wbm\2022-10-19-wbm-computed-structure-entries.jsonl.gz
```

### 2026-07-02 08:05 UTC — layerC-GT recompute e_above_hull from ppd-mp for 500 subset

```
$ C:\Users\07013\Desktop\0702fable\reprolab\.venv\Scripts\python.exe scripts/layer_c_gt_hull.py
```

- exit code: **0**  | duration: 40.9s  | raw log: `logs/cmd-20260702-080524.log`

output tail:
```
  decomp = self.get_decomposition(comp)
C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\pymatgen\analysis\phase_diagram.py:774: UserWarning: No suitable PhaseDiagrams found for Hg1 Ir2 Sm3. Using SLSQP to find decomposition
  decomp = self.get_decomposition(comp)
C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\pymatgen\analysis\phase_diagram.py:774: UserWarning: No suitable PhaseDiagrams found for Bi2 U6 Pt1. Using SLSQP to find decomposition
  decomp = self.get_decomposition(comp)
C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\pymatgen\analysis\phase_diagram.py:774: UserWarning: No suitable PhaseDiagrams found for Hg4 Dy2 Pd2. Using SLSQP to find decomposition
  decomp = self.get_decomposition(comp)
C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\pymatgen\analysis\phase_diagram.py:774: UserWarning: No suitable PhaseDiagrams found for Ca6 Bi2 Os1. Using SLSQP to find decomposition
  decomp = self.get_decomposition(comp)
C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\pymatgen\analysis\phase_diagram.py:774: UserWarning: No suitable PhaseDiagrams found for Cd1 Tl1 Pt2. Using SLSQP to find decomposition
  decomp = self.get_decomposition(comp)
C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\pymatgen\analysis\phase_diagram.py:774: UserWarning: No suitable PhaseDiagrams found for Ge2 Al3 Zn1 V3. Using SLSQP to find decomposition
  decomp = self.get_decomposition(comp)
C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\pymatgen\analysis\phase_diagram.py:774: UserWarning: No suitable PhaseDiagrams found for Ni1 Rh2 V2. Using SLSQP to find decomposition
  decomp = self.get_decomposition(comp)
```

### 2026-07-02 08:07 UTC — layerC-GT diagnose 3 outliers (corrections vs hull lookup)

```
$ C:\Users\07013\Desktop\0702fable\reprolab\.venv\Scripts\python.exe scripts/layer_c_gt_diagnose.py --ids wbm-2-28782 wbm-4-28450 wbm-4-15908
```

- exit code: **0**  | duration: 6.4s  | raw log: `logs/cmd-20260702-080759.log`

output tail:
```
  our adjustments: [('MP2020 anion correction (Br)', -1.068)]
wbm-4-28450 PaIO        
  e_form summary=-2.574240 ours=-2.447933 delta=+126.307 meV/atom
  our adjustments: [('MP2020 anion correction (oxide)', -1.374)]
wbm-4-15908 NdH4Pt      
  e_form summary=-0.466418 ours=-0.585721 delta=-119.303 meV/atom
  our adjustments: [('MP2020 anion correction (H)', -1.432)]
C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.11_3.11.2544.0_x64__qbz5n2kfra8p0\Lib\functools.py:1001: UserWarning: No Pauling electronegativity for Ne. Setting to NaN. This has no physical meaning, and is mainly done to avoid errors caused by the code expecting a float.
  val = self.func(instance)
C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.11_3.11.2544.0_x64__qbz5n2kfra8p0\Lib\functools.py:1001: UserWarning: No Pauling electronegativity for He. Setting to NaN. This has no physical meaning, and is mainly done to avoid errors caused by the code expecting a float.
  val = self.func(instance)
C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.11_3.11.2544.0_x64__qbz5n2kfra8p0\Lib\functools.py:1001: UserWarning: No Pauling electronegativity for Ar. Setting to NaN. This has no physical meaning, and is mainly done to avoid errors caused by the code expecting a float.
  val = self.func(instance)
C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\pymatgen\analysis\compatibility\__init__.py:631: UserWarning: Failed to guess oxidation states for Entry wbm-4-28450 (PaIO). Assigning anion correction to only the most electronegative atom.
  adjustments: list[EnergyAdjustment] = self.get_adjustments(entry)
```

