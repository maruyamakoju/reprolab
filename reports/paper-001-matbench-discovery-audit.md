# ReproLab Paper-001 — Independent Reproducibility Audit of Matbench Discovery

_Generated: 2026-07-02 04:30 UTC_

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

**3 of 3 models reproduce exactly** — every reported fraction to 3 decimals and every
integer confusion-matrix count (TP/FP/TN/FN) identical, on both audited subsets. The
outlier/missing-prediction accounting also matches in two distinct regimes: filter-driven
(CHGNet 2, SevenNet 3 dropped by the 5 eV/atom rule) and genuine-NaN-driven (MACE 38
full / 34 uniq, filter dropped 0).

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

_Captured: 2026-07-02 03:55:09 UTC_

- **timestamp_utc**: `2026-07-02 03:55:09 UTC`
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
click==8.4.2
colorama==0.4.6
comm==0.2.3
contourpy==1.3.3
cycler==0.12.1
decorator==5.3.1
executing==2.2.1
fonttools==4.63.0
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
ruamel.yaml==0.19.1
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

## Open discrepancies
**None (3 of 3 models).** Layer A reproduced the official YAML exactly for **CHGNet**,
**SevenNet-0**, and **MACE-MP-0** on both `unique_prototypes` and `full_test_set` —
every fraction to 3 dp and every integer confusion count (TP/FP/TN/FN) identical, via
both an independent re-implementation and the upstream `stable_metrics`. The pipeline
matches `missing_preds` in both regimes: outlier-filter-driven (CHGNet 2, SevenNet 3)
and genuine-NaN-driven (MACE 38 full / 34 uniq, filter dropped 0). See
`metric_check.md`, `metric_check-sevennet.md`, `metric_check-mace-mp-0.md`.



## 6. Run log (tail)

| FP | 18765.000 | 18765 | 18765 | 0.000 | ✓ |
| TN | 194106.000 | 194106 | 194106 | 0.000 | ✓ |
| FN | 8833.000 | 8833 | 8833 | 0.000 | ✓ |

wrote C:\Users\07013\Desktop\0702fable\reprolab\papers\matbench-discovery\metric_check-sevennet.md
```

### 2026-07-02 — Layer A SevenNet result (manual summary)
Layer A SevenNet-0 completed. Prediction CSV `2024-07-11-wbm-IS2RE.csv.gz` (2.62 MB,
valid gzip) from Figshare API endpoint. Independent re-implementation and upstream
`stable_metrics` **agree with each other and with the official YAML on every metric**,
both subsets: `unique_prototypes` (F1 0.724, MAE 0.048, TP 27304 / FP 14703 / TN 167411
/ FN 6070) and `full_test_set` (F1 0.719, MAE 0.046, TP 35259 / FP 18765 / TN 194106 /
FN 8833). The 5 eV/atom filter drops exactly 3 predictions = YAML `missing_preds: 3`.
No discrepancies — second model reproduced exactly.

**Note on the first attempt (exit 3221225477 = 0xC0000005):** the *first* SevenNet run
(which had to download the CSV) hard-crashed with a native access violation and no
Python traceback. Re-running with the file cached (both directly and through the
wrapper) succeeded with identical results. Classified as a transient native crash on
the download+compute-in-one-process path, not a data or metric issue (see
`failure_notes.md`). Metrics above are from the reproducible cached runs.

### 2026-07-02 04:26 UTC — predownload mace-mp-0

```
$ C:\Users\07013\Desktop\0702fable\reprolab\.venv\Scripts\python.exe C:\Users\07013\Desktop\0702fable\reprolab\scripts\compare_metrics.py --repo C:\Users\07013\Desktop\0702fable\reprolab\vendor\matbench-discovery --model mace-mp-0 --download-only
```

- exit code: **0**  | duration: 6.4s  | raw log: `logs/cmd-20260702-042641.log`

output tail:
```
downloading predictions: https://api.figshare.com/v2/file/download/52057538 -> C:\Users\07013\Desktop\0702fable\reprolab\vendor\matbench-discovery\models\mace\mace-mp-0\2023-12-11-wbm-IS2RE-FIRE.csv.gz
downloaded mace-mp-0: C:\Users\07013\Desktop\0702fable\reprolab\vendor\matbench-discovery\models\mace\mace-mp-0\2023-12-11-wbm-IS2RE-FIRE.csv.gz (2.38 MB)
```

### 2026-07-02 04:26 UTC — layerA mace-mp-0

```
$ C:\Users\07013\Desktop\0702fable\reprolab\.venv\Scripts\python.exe C:\Users\07013\Desktop\0702fable\reprolab\scripts\compare_metrics.py --repo C:\Users\07013\Desktop\0702fable\reprolab\vendor\matbench-discovery --model mace-mp-0 --subsets unique_prototypes full_test_set --out C:\Users\07013\Desktop\0702fable\reprolab\papers\matbench-discovery\metric_check-mace-mp-0.md
```

- exit code: **0**  | duration: 3.9s  | raw log: `logs/cmd-20260702-042656.log`

output tail:
```
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

wrote C:\Users\07013\Desktop\0702fable\reprolab\papers\matbench-discovery\metric_check-mace-mp-0.md
```

### 2026-07-02 — Layer A MACE-MP-0 result (manual summary)
Layer A MACE-MP-0 completed. Prediction CSV downloaded **separately** (via the new
`--download-only` mode, 2.38 MB) and cached before metric computation — the
download+compute split avoided the transient native crash seen once for SevenNet; this
run completed cleanly (exit 0, no crash). Independent re-implementation and upstream
`stable_metrics` agree with each other and with the official YAML on **every** metric
for both `unique_prototypes` (F1 0.669, MAE 0.057, TP 26582 / FP 19457 / TN 162657 /
FN 6792) and `full_test_set` (F1 0.668, MAE 0.055, TP 34420 / FP 24576 / TN 188295 /
FN 9672).

Notable: MACE's `missing_preds` (38 full / 34 uniq) are **genuine NaNs in the published
CSV** — the 5 eV/atom outlier filter dropped 0 — whereas CHGNet (2) and SevenNet (3)
missing came entirely from that filter. The pipeline reproduces the exact confusion
counts in both regimes, validating the missing/outlier handling.

Result: MATCH. No discrepancies (3/3 models).

