# Run Log — Paper-001

Every command executed for this audit is appended here by `scripts/run_command.py`
(exit code, duration, output tail, pointer to the raw log in `logs/`).

Manual entries below; automated entries follow.

### 2026-07-02 — setup (manual)
- Cloned upstream: `git clone --depth 1 https://github.com/janosh/matbench-discovery vendor/matbench-discovery` → OK (118.6 MB, commit `eaa7550`).
- Inspected evaluation code; confirmed metric path (see `reproduction_plan.md`).
- Confirmed ground-truth file present in clone: `data/wbm/2023-12-13-wbm-summary.csv.gz`.

### 2026-07-02 — environment + install (manual)
- Store Python 3.11.9 used (Anaconda base install is misconfigured: its `sys.prefix`
  resolves to the CWD, so `-m venv` crashes with `ModuleNotFoundError: encodings`).
- Created venv `reprolab/.venv` from Store Python 3.11.9 → OK.
- `pip install matbench-discovery` → **exit 0**. Installed matbench-discovery 1.3.1
  with numpy 2.4.6, pandas 3.0.3, pymatgen 2026.5.4, pymatviz 0.18.0,
  scikit-learn 1.9.0, ase 3.29.0, spglib 2.7.0. Raw log: `logs/install-matbench.log`.
- Wiring check (`scratchpad/verify_path.py`) → **PASS**:
  - `stable_metrics` imports from the CLONE and returns all 16 keys.
  - WBM summary loads: 256,963 rows = YAML full_test_set TP+FP+TN+FN total.
  - `unique_prototype==True`: 215,488 = YAML unique_prototypes TP+FP+TN+FN total.
  - all 4 required columns present.
- `capture_env.py` → env snapshot saved. GPU visible: **RTX 4090 (24 GB)**, driver 596.36.

<!-- automated run_command.py entries appended below this line -->

### 2026-07-02 03:59 UTC — layerA chgnet

```
$ C:\Users\07013\Desktop\0702fable\reprolab\.venv\Scripts\python.exe C:\Users\07013\Desktop\0702fable\reprolab\scripts\compare_metrics.py --repo C:\Users\07013\Desktop\0702fable\reprolab\vendor\matbench-discovery --model chgnet-0.3.0 --subsets unique_prototypes full_test_set --out C:\Users\07013\Desktop\0702fable\reprolab\papers\matbench-discovery\metric_check.md
```

- exit code: **1**  | duration: 6.2s  | raw log: `logs/cmd-20260702-035928.log`

output tail:
```
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\pandas\io\parsers\readers.py", line 300, in _read
    parser = TextFileReader(filepath_or_buffer, **kwds)
             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\pandas\io\parsers\readers.py", line 1645, in __init__
    self._engine = self._make_engine(f, self.engine)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\pandas\io\parsers\readers.py", line 1922, in _make_engine
    return mapping[engine](f, **self.options)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\pandas\io\parsers\c_parser_wrapper.py", line 95, in __init__
    self._reader = parsers.TextReader(src, **kwds)
                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "pandas/_libs/parsers.pyx", line 575, in pandas._libs.parsers.TextReader.__cinit__
pandas.errors.EmptyDataError: No columns to parse from file
```

### 2026-07-02 04:01 UTC — layerA chgnet (retry)

```
$ C:\Users\07013\Desktop\0702fable\reprolab\.venv\Scripts\python.exe C:\Users\07013\Desktop\0702fable\reprolab\scripts\compare_metrics.py --repo C:\Users\07013\Desktop\0702fable\reprolab\vendor\matbench-discovery --model chgnet-0.3.0 --subsets unique_prototypes full_test_set --out C:\Users\07013\Desktop\0702fable\reprolab\papers\matbench-discovery\metric_check.md
```

- exit code: **0**  | duration: 30.4s  | raw log: `logs/cmd-20260702-040101.log`

output tail:
```
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

wrote C:\Users\07013\Desktop\0702fable\reprolab\papers\matbench-discovery\metric_check.md
```

### 2026-07-02 — Layer A result (manual summary)
Layer A CHGNet completed. Published prediction CSV downloaded successfully
(`2023-12-21-wbm-IS2RE.csv.gz`, 2.3 MB, valid gzip) after switching to the Figshare
API download endpoint. Independent re-implementation and upstream `stable_metrics`
**agree with each other and with the official YAML on every metric**, both subsets:
`unique_prototypes` (F1 0.613, MAE 0.063) and `full_test_set` (F1 0.612, MAE 0.061).
Integer confusion-matrix counts match **exactly** (e.g. uniq_protos TP 25313 / FP 23955
/ TN 158159 / FN 8061). The 5 eV/atom filter drops exactly 2 predictions, matching the
YAML `full_test_set: missing_preds: 2` (0 in uniq_protos). Official YAML values
reproduced within rounding tolerance — no discrepancies.

### 2026-07-02 04:06 UTC — layerA sevennet

```
$ C:\Users\07013\Desktop\0702fable\reprolab\.venv\Scripts\python.exe C:\Users\07013\Desktop\0702fable\reprolab\scripts\compare_metrics.py --repo C:\Users\07013\Desktop\0702fable\reprolab\vendor\matbench-discovery --model sevennet-0 --subsets unique_prototypes full_test_set --out C:\Users\07013\Desktop\0702fable\reprolab\papers\matbench-discovery\metric_check-sevennet.md
```

- exit code: **3221225477**  | duration: 9.0s  | raw log: `logs/cmd-20260702-040654.log`

output tail:
```

```

### 2026-07-02 04:08 UTC — layerA sevennet (cached, rerun)

```
$ C:\Users\07013\Desktop\0702fable\reprolab\.venv\Scripts\python.exe C:\Users\07013\Desktop\0702fable\reprolab\scripts\compare_metrics.py --repo C:\Users\07013\Desktop\0702fable\reprolab\vendor\matbench-discovery --model sevennet-0 --subsets unique_prototypes full_test_set --out C:\Users\07013\Desktop\0702fable\reprolab\papers\matbench-discovery\metric_check-sevennet.md
```

- exit code: **0**  | duration: 3.9s  | raw log: `logs/cmd-20260702-040847.log`

output tail:
```
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

### 2026-07-02 04:39 UTC — predownload orb-v2

```
$ C:\Users\07013\Desktop\0702fable\reprolab\.venv\Scripts\python.exe scripts/compare_metrics.py --model orb-v2 --download-only
```

- exit code: **0**  | duration: 6.0s  | raw log: `logs/cmd-20260702-043930.log`

output tail:
```
downloading predictions: https://api.figshare.com/v2/file/download/52057562 -> C:\Users\07013\Desktop\0702fable\reprolab\vendor\matbench-discovery\models\orb\orbff-v2\2024-10-11-wbm-IS2RE.csv.gz
downloaded orb-v2: C:\Users\07013\Desktop\0702fable\reprolab\vendor\matbench-discovery\models\orb\orbff-v2\2024-10-11-wbm-IS2RE.csv.gz (2.39 MB)
```

### 2026-07-02 04:39 UTC — layerA orb-v2

```
$ C:\Users\07013\Desktop\0702fable\reprolab\.venv\Scripts\python.exe scripts/compare_metrics.py --model orb-v2 --subsets unique_prototypes full_test_set --out papers/matbench-discovery/metric_check-orb-v2.md
```

- exit code: **0**  | duration: 4.2s  | raw log: `logs/cmd-20260702-043954.log`

output tail:
```
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

wrote papers\matbench-discovery\metric_check-orb-v2.md
```

### 2026-07-02 04:58 UTC — layerB make subset (500, seed 42)

```
$ C:\Users\07013\Desktop\0702fable\reprolab\.venv\Scripts\python.exe scripts/layer_b_subset.py
```

- exit code: **0**  | duration: 1.0s  | raw log: `logs/cmd-20260702-045822.log`

output tail:
```
universe: 215,488 unique_prototypes rows (of 256,963 total)
sampled: n=500 seed=42 -> papers\matbench-discovery\layer_b_subset.csv
stable fraction: subset 0.132 vs universe 0.153
pre-smoke (first 20 ids): ['wbm-3-33636', 'wbm-3-24460', 'wbm-2-29187', 'wbm-3-24851', 'wbm-1-49596', 'wbm-1-38260', 'wbm-3-20857', 'wbm-2-36510', 'wbm-2-31866', 'wbm-5-3711', 'wbm-4-16455', 'wbm-4-4335', 'wbm-3-11637', 'wbm-4-32299', 'wbm-2-24011', 'wbm-4-28433', 'wbm-5-10472', 'wbm-2-30414', 'wbm-2-17117', 'wbm-1-39713']
```

### 2026-07-02 04:58 UTC — layerB download wbm initial structures (md5-checked)

```
$ C:\Users\07013\Desktop\0702fable\reprolab\.venv\Scripts\python.exe scripts/download_datafile.py --name wbm_initial_structures
```

- exit code: **1**  | duration: 25.1s  | raw log: `logs/cmd-20260702-045858.log`

output tail:
```
downloading wbm_initial_structures: https://api.figshare.com/v2/file/download/53161835 -> C:\Users\07013\Desktop\0702fable\reprolab\vendor\matbench-discovery\data\wbm\2022-10-19-wbm-init-structs.jsonl.gz
downloaded 49.5 MB
Traceback (most recent call last):
  File "C:\Users\07013\Desktop\0702fable\reprolab\scripts\download_datafile.py", line 77, in <module>
    main()
  File "C:\Users\07013\Desktop\0702fable\reprolab\scripts\download_datafile.py", line 71, in main
    raise RuntimeError(f"md5 mismatch: got {got_md5}, want {want_md5}")
RuntimeError: md5 mismatch: got b809f101dd42a745ec2baabe7eb16f11, want ff2c40a3a7bf65468852b67f0dbc67df
```

### 2026-07-02 05:01 UTC — layerB download wbm init structs, retry w/ figshare computed_md5 (YAML md5 is stale, see failure_notes)

```
$ C:\Users\07013\Desktop\0702fable\reprolab\.venv\Scripts\python.exe scripts/download_datafile.py --name wbm_initial_structures --expect-md5 b809f101dd42a745ec2baabe7eb16f11
```

- exit code: **0**  | duration: 17.6s  | raw log: `logs/cmd-20260702-050152.log`

output tail:
```
downloading wbm_initial_structures: https://api.figshare.com/v2/file/download/53161835 -> C:\Users\07013\Desktop\0702fable\reprolab\vendor\matbench-discovery\data\wbm\2022-10-19-wbm-init-structs.jsonl.gz
downloaded 49.5 MB
md5 OK (b809f101dd42a745ec2baabe7eb16f11): C:\Users\07013\Desktop\0702fable\reprolab\vendor\matbench-discovery\data\wbm\2022-10-19-wbm-init-structs.jsonl.gz
```

### 2026-07-02 05:04 UTC — layerB preflight: cuda + chgnet weights check

```
$ C:\Users\07013\Desktop\0702fable\reprolab\.venv\Scripts\python.exe -c 
import torch
from chgnet.model import CHGNet
print('torch', torch.__version__, '| cuda available:', torch.cuda.is_available())
print('device:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'CPU')
model = CHGNet.load()
n = sum(p.numel() for p in model.parameters())
print('chgnet params:', n, '(YAML model_params: 412525, match:', n == 412525, ')')
print('model version attr:', getattr(model, 'version', 'n/a'))

```

- exit code: **0**  | duration: 10.5s  | raw log: `logs/cmd-20260702-050410.log`

output tail:
```
torch 2.11.0+cu128 | cuda available: True
device: NVIDIA GeForce RTX 4090
CHGNet v0.3.0 initialized with 412,525 parameters
CHGNet will run on cuda
chgnet params: 412525 (YAML model_params: 412525, match: True )
model version attr: 0.3.0
```

### 2026-07-02 05:04 UTC — layerB pre-smoke 20 run1 (GPU)

```
$ C:\Users\07013\Desktop\0702fable\reprolab\.venv\Scripts\python.exe scripts/layer_b_relax.py --limit 20 --out experiments/layer-b/chgnet/presmoke-run1.jsonl.gz
```

- exit code: **0**  | duration: 31.5s  | raw log: `logs/cmd-20260702-050450.log`

output tail:
```
loaded 20 initial structures in 3.3s
CHGNet v0.3.0 initialized with 412,525 parameters
CHGNet will run on cuda
versions: chgnet 0.4.2 | torch 2.11.0+cu128 | numpy 2.4.6 | device cuda (NVIDIA GeForce RTX 4090)
protocol: FIRE steps<=500 fmax=0.05 relax_cell=True FrechetCellFilter (ase_filter)
relaxed 20/20 | failures 0 (0%)
s/structure: mean 1.26 | median 0.94 | max 5.35
converged: 20/20
wrote C:\Users\07013\Desktop\0702fable\reprolab\experiments\layer-b\chgnet\presmoke-run1.jsonl.gz
C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\chgnet\model\model.py:898: UserWarning: Converting a tensor with requires_grad=True to a scalar may lead to unexpected behavior.
Consider using tensor.detach() first. (Triggered internally at C:\actions-runner\_work\pytorch\pytorch\pytorch\torch\csrc\autograd\generated\python_variable_methods.cpp:837.)
  volumes = torch.tensor(volumes, dtype=TORCH_DTYPE, device=atomic_numbers.device)
```

### 2026-07-02 05:05 UTC — layerB pre-smoke 20 run2 (GPU, variance bound)

```
$ C:\Users\07013\Desktop\0702fable\reprolab\.venv\Scripts\python.exe scripts/layer_b_relax.py --limit 20 --out experiments/layer-b/chgnet/presmoke-run2.jsonl.gz
```

- exit code: **0**  | duration: 31.3s  | raw log: `logs/cmd-20260702-050534.log`

output tail:
```
loaded 20 initial structures in 3.3s
CHGNet v0.3.0 initialized with 412,525 parameters
CHGNet will run on cuda
versions: chgnet 0.4.2 | torch 2.11.0+cu128 | numpy 2.4.6 | device cuda (NVIDIA GeForce RTX 4090)
protocol: FIRE steps<=500 fmax=0.05 relax_cell=True FrechetCellFilter (ase_filter)
relaxed 20/20 | failures 0 (0%)
s/structure: mean 1.26 | median 0.92 | max 5.69
converged: 20/20
wrote C:\Users\07013\Desktop\0702fable\reprolab\experiments\layer-b\chgnet\presmoke-run2.jsonl.gz
C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\chgnet\model\model.py:898: UserWarning: Converting a tensor with requires_grad=True to a scalar may lead to unexpected behavior.
Consider using tensor.detach() first. (Triggered internally at C:\actions-runner\_work\pytorch\pytorch\pytorch\torch\csrc\autograd\generated\python_variable_methods.cpp:837.)
  volumes = torch.tensor(volumes, dtype=TORCH_DTYPE, device=atomic_numbers.device)
```

### 2026-07-02 05:07 UTC — layerB score pre-smoke vs published (Layer A path)

```
$ C:\Users\07013\Desktop\0702fable\reprolab\.venv\Scripts\python.exe scripts/layer_b_score.py --preds experiments/layer-b/chgnet/presmoke-run1.jsonl.gz experiments/layer-b/chgnet/presmoke-run2.jsonl.gz --out papers/matbench-discovery/metric_check-layer-b-chgnet-presmoke.md
```

- exit code: **1**  | duration: 2.3s  | raw log: `logs/cmd-20260702-050713.log`

output tail:
```
    if self.parser.check_event(AliasEvent):
       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\ruamel\yaml\parser.py", line 141, in check_event
    self.current_event = self.state()
                         ^^^^^^^^^^^^
  File "C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\ruamel\yaml\parser.py", line 639, in parse_block_mapping_value
    return self.parse_block_node_or_indentless_sequence()
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\ruamel\yaml\parser.py", line 355, in parse_block_node_or_indentless_sequence
    return self.parse_node(block=True, indentless_sequence=True)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\ruamel\yaml\parser.py", line 437, in parse_node
    if self.scanner.check_token(ScalarToken):
       ^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'YAML' object has no attribute 'check_token'
```

### 2026-07-02 05:08 UTC — layerB score pre-smoke vs published (Layer A path), after ruamel pin

```
$ C:\Users\07013\Desktop\0702fable\reprolab\.venv\Scripts\python.exe scripts/layer_b_score.py --preds experiments/layer-b/chgnet/presmoke-run1.jsonl.gz experiments/layer-b/chgnet/presmoke-run2.jsonl.gz --out papers/matbench-discovery/metric_check-layer-b-chgnet-presmoke.md
```

- exit code: **0**  | duration: 4.0s  | raw log: `logs/cmd-20260702-050849.log`

output tail:
```
| Accuracy | 0.850 | 0.850 | 0.850 | 0.850 |
| MAE | 0.082 | 0.082 | 0.082 | 0.082 |
| RMSE | 0.104 | 0.104 | 0.104 | 0.104 |
| TP | 1 | 1 | 1 | 1 |
| FP | 2 | 2 | 2 | 2 |
| TN | 16 | 16 | 16 | 16 |
| FN | 1 | 1 | 1 | 1 |

wrote C:\Users\07013\Desktop\0702fable\reprolab\papers\matbench-discovery\metric_check-layer-b-chgnet-presmoke.md
C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.11_3.11.2544.0_x64__qbz5n2kfra8p0\Lib\functools.py:1001: UserWarning: No Pauling electronegativity for Ne. Setting to NaN. This has no physical meaning, and is mainly done to avoid errors caused by the code expecting a float.
  val = self.func(instance)
C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.11_3.11.2544.0_x64__qbz5n2kfra8p0\Lib\functools.py:1001: UserWarning: No Pauling electronegativity for He. Setting to NaN. This has no physical meaning, and is mainly done to avoid errors caused by the code expecting a float.
  val = self.func(instance)
C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.11_3.11.2544.0_x64__qbz5n2kfra8p0\Lib\functools.py:1001: UserWarning: No Pauling electronegativity for Ar. Setting to NaN. This has no physical meaning, and is mainly done to avoid errors caused by the code expecting a float.
  val = self.func(instance)
```

### 2026-07-02 05:09 UTC — capture env after layerB installs (torch/chgnet/ruamel pin)

```
$ C:\Users\07013\Desktop\0702fable\reprolab\.venv\Scripts\python.exe scripts/capture_env.py
```

- exit code: **0**  | duration: 0.5s  | raw log: `logs/cmd-20260702-050927.log`

output tail:
```
wrote C:\Users\07013\Desktop\0702fable\reprolab\logs\env-20260702-050928.json
wrote C:\Users\07013\Desktop\0702fable\reprolab\papers\matbench-discovery\environment.md
```
