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

### 2026-07-02 06:19 UTC — layerB smoke 500 run1 (GPU)

```
$ C:\Users\07013\Desktop\0702fable\reprolab\.venv\Scripts\python.exe scripts/layer_b_relax.py --out experiments/layer-b/chgnet/smoke500-run1.jsonl.gz
```

- exit code: **0**  | duration: 556.1s  | raw log: `logs/cmd-20260702-061926.log`

output tail:
```
  return f(*arrays, *other_args, **kwargs)
C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\scipy\_lib\_util.py:1181: RuntimeWarning: logm result may be inaccurate, approximate err = 2.8950528433502876e-13
  return f(*arrays, *other_args, **kwargs)
C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\scipy\_lib\_util.py:1181: RuntimeWarning: logm result may be inaccurate, approximate err = 2.8898301709961935e-13
  return f(*arrays, *other_args, **kwargs)
C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\scipy\_lib\_util.py:1181: RuntimeWarning: logm result may be inaccurate, approximate err = 2.895197489755525e-13
  return f(*arrays, *other_args, **kwargs)
C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\scipy\_lib\_util.py:1181: RuntimeWarning: logm result may be inaccurate, approximate err = 2.84166155036159e-13
  return f(*arrays, *other_args, **kwargs)
C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\scipy\_lib\_util.py:1181: RuntimeWarning: logm result may be inaccurate, approximate err = 2.917325198573279e-13
  return f(*arrays, *other_args, **kwargs)
C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\scipy\_lib\_util.py:1181: RuntimeWarning: logm result may be inaccurate, approximate err = 2.8708189922621193e-13
  return f(*arrays, *other_args, **kwargs)
C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\scipy\_lib\_util.py:1181: RuntimeWarning: logm result may be inaccurate, approximate err = 2.891320154424595e-13
  return f(*arrays, *other_args, **kwargs)
```

### 2026-07-02 06:29 UTC — layerB score smoke500 vs published (Layer A path)

```
$ C:\Users\07013\Desktop\0702fable\reprolab\.venv\Scripts\python.exe scripts/layer_b_score.py --preds experiments/layer-b/chgnet/smoke500-run1.jsonl.gz --out papers/matbench-discovery/metric_check-layer-b-chgnet-smoke500.md
```

- exit code: **0**  | duration: 13.9s  | raw log: `logs/cmd-20260702-062921.log`

output tail:
```
| Accuracy | 0.866 | 0.866 | 0.866 | 0.866 |
| MAE | 0.067 | 0.067 | 0.067 | 0.067 |
| RMSE | 0.104 | 0.104 | 0.104 | 0.104 |
| TP | 47 | 47 | 47 | 47 |
| FP | 47 | 47 | 47 | 47 |
| TN | 386 | 386 | 386 | 386 |
| FN | 20 | 20 | 20 | 20 |

wrote C:\Users\07013\Desktop\0702fable\reprolab\papers\matbench-discovery\metric_check-layer-b-chgnet-smoke500.md
C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.11_3.11.2544.0_x64__qbz5n2kfra8p0\Lib\functools.py:1001: UserWarning: No Pauling electronegativity for Ne. Setting to NaN. This has no physical meaning, and is mainly done to avoid errors caused by the code expecting a float.
  val = self.func(instance)
C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.11_3.11.2544.0_x64__qbz5n2kfra8p0\Lib\functools.py:1001: UserWarning: No Pauling electronegativity for He. Setting to NaN. This has no physical meaning, and is mainly done to avoid errors caused by the code expecting a float.
  val = self.func(instance)
C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.11_3.11.2544.0_x64__qbz5n2kfra8p0\Lib\functools.py:1001: UserWarning: No Pauling electronegativity for Ar. Setting to NaN. This has no physical meaning, and is mainly done to avoid errors caused by the code expecting a float.
  val = self.func(instance)
```

### 2026-07-02 — external-path self-audit (fresh clone of the PUBLIC repo)

Followed README "Reproduce it yourself" verbatim in a throwaway directory:
fresh `git clone https://github.com/maruyamakoju/reprolab`, fresh upstream clone
(HEAD = `eaa7550`, identical to our pinned audit commit — no drift), fresh venv
(`pip install matbench-discovery` 1.3.1), Figshare API download (2.38 MB), then
`compare_metrics.py --model chgnet-0.3.0` on both subsets.

- result: **22/22 metric checks pass, 0 mismatches** (F1 0.613/0.612,
  MAE 0.063/0.061, integer confusion counts exact)
- compute step: exit 0, 24.4 s
- conclusion: the published instructions reproduce Layer A end-to-end from a
  clean machine state.

### 2026-07-02 07:59 UTC — layerC statistical audit (bootstrap B=2000, threshold sweep, error correlation)

```
$ C:\Users\07013\Desktop\0702fable\reprolab\.venv\Scripts\python.exe scripts/layer_c_stats.py --n-boot 2000
```

- exit code: **0**  | duration: 11.5s  | raw log: `logs/cmd-20260702-075923.log`

output tail:
```
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

wrote C:\Users\07013\Desktop\0702fable\reprolab\papers\matbench-discovery\layer_c_statistical_audit.md
```

### 2026-07-02 08:00 UTC — layerC rerun with leaderboard-resolution scan

```
$ C:\Users\07013\Desktop\0702fable\reprolab\.venv\Scripts\python.exe scripts/layer_c_stats.py --n-boot 2000
```

- exit code: **0**  | duration: 11.7s  | raw log: `logs/cmd-20260702-080038.log`

output tail:
```
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

wrote C:\Users\07013\Desktop\0702fable\reprolab\papers\matbench-discovery\layer_c_statistical_audit.md
```

### 2026-07-02 08:02 UTC — layerC-GT download ppd-mp (220MB)

```
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

### 2026-07-02 08:18 UTC — layerC-GT control: rerun outlier diagnosis under pymatgen 2023.5.10

```
$ C:\Users\07013\AppData\Local\Temp\claude\C--Users-07013-Desktop-0702fable\cfdd1078-4d5a-454d-b4bd-b545a23fd95e\scratchpad\oldpmg\Scripts\python.exe scripts/layer_c_gt_diagnose.py --ids wbm-2-28782 wbm-4-28450 wbm-4-15908
```

- exit code: **0**  | duration: 8.9s  | raw log: `logs/cmd-20260702-081826.log`

output tail:
```
  our adjustments: [('MP2020 anion correction (oxide)', -1.374), ('MP2020 anion correction (I)', -0.758)]
wbm-4-15908 NdH4Pt      
  e_form summary=-0.466418 ours=-0.466387 delta=+0.031 meV/atom
  our adjustments: []
C:\Users\07013\AppData\Local\Temp\claude\C--Users-07013-Desktop-0702fable\cfdd1078-4d5a-454d-b4bd-b545a23fd95e\scratchpad\oldpmg\Lib\site-packages\pymatgen\core\periodic_table.py:209: UserWarning: No electronegativity for Ne. Setting to NaN. This has no physical meaning, and is mainly done to avoid errors caused by the code expecting a float.
  warnings.warn(
C:\Users\07013\AppData\Local\Temp\claude\C--Users-07013-Desktop-0702fable\cfdd1078-4d5a-454d-b4bd-b545a23fd95e\scratchpad\oldpmg\Lib\site-packages\pymatgen\core\composition.py:1217: FutureWarning: gcd is deprecated, and will be removed on 2028-01-01
Use math.gcd instead.
  factor = abs(gcd(*(int(i) for i in sym_amt.values())))
C:\Users\07013\AppData\Local\Temp\claude\C--Users-07013-Desktop-0702fable\cfdd1078-4d5a-454d-b4bd-b545a23fd95e\scratchpad\oldpmg\Lib\site-packages\uncertainties\core.py:1024: UserWarning: Using UFloat objects with std_dev==0 may give unexpected results.
  warn("Using UFloat objects with std_dev==0 may give unexpected results.")
C:\Users\07013\AppData\Local\Temp\claude\C--Users-07013-Desktop-0702fable\cfdd1078-4d5a-454d-b4bd-b545a23fd95e\scratchpad\oldpmg\Lib\site-packages\pymatgen\core\periodic_table.py:209: UserWarning: No electronegativity for He. Setting to NaN. This has no physical meaning, and is mainly done to avoid errors caused by the code expecting a float.
  warnings.warn(
C:\Users\07013\AppData\Local\Temp\claude\C--Users-07013-Desktop-0702fable\cfdd1078-4d5a-454d-b4bd-b545a23fd95e\scratchpad\oldpmg\Lib\site-packages\pymatgen\core\periodic_table.py:209: UserWarning: No electronegativity for Ar. Setting to NaN. This has no physical meaning, and is mainly done to avoid errors caused by the code expecting a float.
  warnings.warn(
```

### 2026-07-03 04:52 UTC — layerB mace install mace-torch

```
$ C:\Users\07013\Desktop\0702fable\reprolab\.venv\Scripts\python.exe -m pip install mace-torch>=0.3.15
```

- exit code: **0**  | duration: 14.1s  | raw log: `logs/cmd-20260703-045221.log`

output tail:
```
Using cached mace_torch-0.3.16-py3-none-any.whl (316 kB)
Using cached e3nn-0.4.4-py3-none-any.whl (387 kB)
Using cached opt_einsum_fx-0.1.4-py3-none-any.whl (13 kB)
Using cached configargparse-1.7.5-py3-none-any.whl (27 kB)
Using cached h5py-3.16.0-cp311-cp311-win_amd64.whl (3.2 MB)
Downloading lmdb-2.2.1-cp311-cp311-win_amd64.whl (113 kB)
Using cached matscipy-1.2.0-cp311-cp311-win_amd64.whl (573 kB)
Using cached opt_einsum-3.4.0-py3-none-any.whl (71 kB)
Downloading prettytable-3.18.0-py3-none-any.whl (37 kB)
Using cached torch_ema-0.3-py3-none-any.whl (5.5 kB)
Using cached torchmetrics-1.9.0-py3-none-any.whl (983 kB)
Using cached lightning_utilities-0.15.3-py3-none-any.whl (31 kB)
Installing collected packages: python-hostlist, prettytable, opt_einsum, lmdb, lightning-utilities, h5py, configargparse, torchmetrics, torch-ema, opt-einsum-fx, matscipy, e3nn, mace-torch

Successfully installed configargparse-1.7.5 e3nn-0.4.4 h5py-3.16.0 lightning-utilities-0.15.3 lmdb-2.2.1 mace-torch-0.3.16 matscipy-1.2.0 opt-einsum-fx-0.1.4 opt_einsum-3.4.0 prettytable-3.18.0 python-hostlist-2.3.0 torch-ema-0.3 torchmetrics-1.9.0
```

### 2026-07-03 04:52 UTC — layerB mace preflight import cuda checkpoint

```
$ C:\Users\07013\Desktop\0702fable\reprolab\.venv\Scripts\python.exe -c import torch; from importlib.metadata import version; from mace.calculators import mace_mp; print('torch', version('torch'), 'cuda', torch.cuda.is_available(), torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'cpu'); print('mace-torch', version('mace-torch')); calc=mace_mp(model='https://github.com/ACEsuit/mace-foundations/releases/download/mace_mp_0/2023-12-03-mace-128-L1_epoch-199.model', device='cuda' if torch.cuda.is_available() else 'cpu', default_dtype='float64', enable_cueq=False); print(type(calc).__name__)
```

- exit code: **0**  | duration: 21.6s  | raw log: `logs/cmd-20260703-045243.log`

output tail:
```
cuequivariance or cuequivariance_torch is not available. Cuequivariance acceleration will be disabled.
torch 2.11.0+cu128 cuda True NVIDIA GeForce RTX 4090
mace-torch 0.3.16
Using Materials Project MACE for MACECalculator with C:\Users\07013\.cache\mace/20231203mace128L1_epoch199model
Using float64 for MACECalculator, which is slower but more accurate. Recommended for geometry optimization.
MACECalculator
C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\e3nn\o3\_wigner.py:10: UserWarning: Environment variable TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD detected, since the`weights_only` argument was not explicitly passed to `torch.load`, forcing weights_only=False.
  _Jd, _W3j_flat, _W3j_indices = torch.load(os.path.join(os.path.dirname(__file__), 'constants.pt'))
C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\mace\calculators\mace.py:226: UserWarning: Environment variable TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD detected, since the`weights_only` argument was not explicitly passed to `torch.load`, forcing weights_only=False.
  torch.load(f=model_path, map_location=device)
```

### 2026-07-03 04:54 UTC — layerB mace pre-smoke 2 run1

```
$ C:\Users\07013\Desktop\0702fable\reprolab\.venv\Scripts\python.exe scripts\layer_b_mace_relax.py --limit 2 --out experiments/layer-b/mace-mp-0/presmoke2-run1.jsonl.gz
```

- exit code: **0**  | duration: 11.9s  | raw log: `logs/cmd-20260703-045450.log`

output tail:
```
cuequivariance or cuequivariance_torch is not available. Cuequivariance acceleration will be disabled.
loaded 2 initial structures in 2.2s
Using Materials Project MACE for MACECalculator with C:\Users\07013\.cache\mace/20231203mace128L1_epoch199model
Using float64 for MACECalculator, which is slower but more accurate. Recommended for geometry optimization.
this run: 2 new, 0 resumed, 0 failed
versions: mace-torch 0.3.16 | torch 2.11.0+cu128 | numpy 2.4.6 | device cuda (NVIDIA GeForce RTX 4090)
protocol: MACE-MP-0 FIRE steps<=500 fmax=0.05 FrechetCellFilter float64 enable_cueq=False
relaxed 2/2 | failures 0
s/structure: mean 2.52 | median 2.52 | max 3.88
converged: 2/2
wrote C:\Users\07013\Desktop\0702fable\reprolab\experiments\layer-b\mace-mp-0\presmoke2-run1.jsonl.gz
C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\e3nn\o3\_wigner.py:10: UserWarning: Environment variable TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD detected, since the`weights_only` argument was not explicitly passed to `torch.load`, forcing weights_only=False.
  _Jd, _W3j_flat, _W3j_indices = torch.load(os.path.join(os.path.dirname(__file__), 'constants.pt'))
C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\mace\calculators\mace.py:226: UserWarning: Environment variable TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD detected, since the`weights_only` argument was not explicitly passed to `torch.load`, forcing weights_only=False.
  torch.load(f=model_path, map_location=device)
```

### 2026-07-03 04:55 UTC — layerB mace score pre-smoke 2

```
$ C:\Users\07013\Desktop\0702fable\reprolab\.venv\Scripts\python.exe scripts\layer_b_score.py --model mace-mp-0 --preds experiments/layer-b/mace-mp-0/presmoke2-run1.jsonl.gz --out papers/matbench-discovery/metric_check-layer-b-mace-mp-0-presmoke2.md
```

- exit code: **0**  | duration: 4.2s  | raw log: `logs/cmd-20260703-045508.log`

output tail:
```
| Accuracy | 0.500 | 0.500 | 1.000 | 1.000 |
| MAE | 0.045 | 0.045 | 0.112 | 0.112 |
| RMSE | 0.053 | 0.053 | 0.149 | 0.149 |
| TP | 0 | 0 | 1 | 1 |
| FP | 0 | 0 | 0 | 0 |
| TN | 1 | 1 | 1 | 1 |
| FN | 1 | 1 | 0 | 0 |

wrote C:\Users\07013\Desktop\0702fable\reprolab\papers\matbench-discovery\metric_check-layer-b-mace-mp-0-presmoke2.md
C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.11_3.11.2544.0_x64__qbz5n2kfra8p0\Lib\functools.py:1001: UserWarning: No Pauling electronegativity for Ne. Setting to NaN. This has no physical meaning, and is mainly done to avoid errors caused by the code expecting a float.
  val = self.func(instance)
C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.11_3.11.2544.0_x64__qbz5n2kfra8p0\Lib\functools.py:1001: UserWarning: No Pauling electronegativity for He. Setting to NaN. This has no physical meaning, and is mainly done to avoid errors caused by the code expecting a float.
  val = self.func(instance)
C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.11_3.11.2544.0_x64__qbz5n2kfra8p0\Lib\functools.py:1001: UserWarning: No Pauling electronegativity for Ar. Setting to NaN. This has no physical meaning, and is mainly done to avoid errors caused by the code expecting a float.
  val = self.func(instance)
```

### 2026-07-03 04:56 UTC — layerB mace pre-smoke 2 run2 with structures

```
$ C:\Users\07013\Desktop\0702fable\reprolab\.venv\Scripts\python.exe scripts\layer_b_mace_relax.py --limit 2 --out experiments/layer-b/mace-mp-0/presmoke2-run2.jsonl.gz
```

- exit code: **0**  | duration: 11.2s  | raw log: `logs/cmd-20260703-045633.log`

output tail:
```
cuequivariance or cuequivariance_torch is not available. Cuequivariance acceleration will be disabled.
loaded 2 initial structures in 2.2s
Using Materials Project MACE for MACECalculator with C:\Users\07013\.cache\mace/20231203mace128L1_epoch199model
Using float64 for MACECalculator, which is slower but more accurate. Recommended for geometry optimization.
this run: 2 new, 0 resumed, 0 failed
versions: mace-torch 0.3.16 | torch 2.11.0+cu128 | numpy 2.4.6 | device cuda (NVIDIA GeForce RTX 4090)
protocol: MACE-MP-0 FIRE steps<=500 fmax=0.05 FrechetCellFilter float64 enable_cueq=False
relaxed 2/2 | failures 0
s/structure: mean 2.19 | median 2.19 | max 3.26
converged: 2/2
wrote C:\Users\07013\Desktop\0702fable\reprolab\experiments\layer-b\mace-mp-0\presmoke2-run2.jsonl.gz
C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\e3nn\o3\_wigner.py:10: UserWarning: Environment variable TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD detected, since the`weights_only` argument was not explicitly passed to `torch.load`, forcing weights_only=False.
  _Jd, _W3j_flat, _W3j_indices = torch.load(os.path.join(os.path.dirname(__file__), 'constants.pt'))
C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\mace\calculators\mace.py:226: UserWarning: Environment variable TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD detected, since the`weights_only` argument was not explicitly passed to `torch.load`, forcing weights_only=False.
  torch.load(f=model_path, map_location=device)
```

### 2026-07-03 04:56 UTC — layerB mace score pre-smoke 2 with MP2020 correction

```
$ C:\Users\07013\Desktop\0702fable\reprolab\.venv\Scripts\python.exe scripts\layer_b_score.py --model mace-mp-0 --preds experiments/layer-b/mace-mp-0/presmoke2-run2.jsonl.gz --out papers/matbench-discovery/metric_check-layer-b-mace-mp-0-presmoke2.md
```

- exit code: **0**  | duration: 23.7s  | raw log: `logs/cmd-20260703-045650.log`

output tail:
```
wrote C:\Users\07013\Desktop\0702fable\reprolab\papers\matbench-discovery\metric_check-layer-b-mace-mp-0-presmoke2.md
C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.11_3.11.2544.0_x64__qbz5n2kfra8p0\Lib\functools.py:1001: UserWarning: No Pauling electronegativity for Ne. Setting to NaN. This has no physical meaning, and is mainly done to avoid errors caused by the code expecting a float.
  val = self.func(instance)
C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.11_3.11.2544.0_x64__qbz5n2kfra8p0\Lib\functools.py:1001: UserWarning: No Pauling electronegativity for He. Setting to NaN. This has no physical meaning, and is mainly done to avoid errors caused by the code expecting a float.
  val = self.func(instance)
C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.11_3.11.2544.0_x64__qbz5n2kfra8p0\Lib\functools.py:1001: UserWarning: No Pauling electronegativity for Ar. Setting to NaN. This has no physical meaning, and is mainly done to avoid errors caused by the code expecting a float.
  val = self.func(instance)

  0%|          | 0/2 [00:00<?, ?it/s]C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\pymatgen\analysis\compatibility\__init__.py:631: UserWarning: Failed to guess oxidation states for Entry wbm-3-33636 (BaI3). Assigning anion correction to only the most electronegative atom.
  adjustments: list[EnergyAdjustment] = self.get_adjustments(entry)

 50%|█████     | 1/2 [00:00<00:00,  7.06it/s]C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\pymatgen\analysis\compatibility\__init__.py:631: UserWarning: Failed to guess oxidation states for Entry wbm-3-24460 (Er4In5Fe2). Assigning anion correction to only the most electronegative atom.
  adjustments: list[EnergyAdjustment] = self.get_adjustments(entry)

100%|██████████| 2/2 [00:00<00:00, 14.02it/s]
```

### 2026-07-03 04:57 UTC — layerB mace pre-smoke 20 run1

```
$ C:\Users\07013\Desktop\0702fable\reprolab\.venv\Scripts\python.exe scripts\layer_b_mace_relax.py --limit 20 --out experiments/layer-b/mace-mp-0/presmoke20-run1.jsonl.gz
```

- exit code: **0**  | duration: 42.9s  | raw log: `logs/cmd-20260703-045726.log`

output tail:
```
cuequivariance or cuequivariance_torch is not available. Cuequivariance acceleration will be disabled.
loaded 20 initial structures in 3.8s
Using Materials Project MACE for MACECalculator with C:\Users\07013\.cache\mace/20231203mace128L1_epoch199model
Using float64 for MACECalculator, which is slower but more accurate. Recommended for geometry optimization.
this run: 20 new, 0 resumed, 0 failed
versions: mace-torch 0.3.16 | torch 2.11.0+cu128 | numpy 2.4.6 | device cuda (NVIDIA GeForce RTX 4090)
protocol: MACE-MP-0 FIRE steps<=500 fmax=0.05 FrechetCellFilter float64 enable_cueq=False
relaxed 20/20 | failures 0
s/structure: mean 1.69 | median 1.39 | max 4.71
converged: 20/20
wrote C:\Users\07013\Desktop\0702fable\reprolab\experiments\layer-b\mace-mp-0\presmoke20-run1.jsonl.gz
C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\e3nn\o3\_wigner.py:10: UserWarning: Environment variable TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD detected, since the`weights_only` argument was not explicitly passed to `torch.load`, forcing weights_only=False.
  _Jd, _W3j_flat, _W3j_indices = torch.load(os.path.join(os.path.dirname(__file__), 'constants.pt'))
C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\mace\calculators\mace.py:226: UserWarning: Environment variable TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD detected, since the`weights_only` argument was not explicitly passed to `torch.load`, forcing weights_only=False.
  torch.load(f=model_path, map_location=device)
```

### 2026-07-03 04:58 UTC — layerB mace score pre-smoke 20 run1

```
$ C:\Users\07013\Desktop\0702fable\reprolab\.venv\Scripts\python.exe scripts\layer_b_score.py --model mace-mp-0 --preds experiments/layer-b/mace-mp-0/presmoke20-run1.jsonl.gz --out papers/matbench-discovery/metric_check-layer-b-mace-mp-0-presmoke20.md
```

- exit code: **0**  | duration: 24.7s  | raw log: `logs/cmd-20260703-045820.log`

output tail:
```
  adjustments: list[EnergyAdjustment] = self.get_adjustments(entry)
C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\pymatgen\analysis\compatibility\__init__.py:631: UserWarning: Failed to guess oxidation states for Entry wbm-4-32299 (OsAuS2). Assigning anion correction to only the most electronegative atom.
  adjustments: list[EnergyAdjustment] = self.get_adjustments(entry)
C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\pymatgen\analysis\compatibility\__init__.py:631: UserWarning: Failed to guess oxidation states for Entry wbm-2-24011 (Li4InO5). Assigning anion correction to only the most electronegative atom.
  adjustments: list[EnergyAdjustment] = self.get_adjustments(entry)
C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\pymatgen\analysis\compatibility\__init__.py:631: UserWarning: Failed to guess oxidation states for Entry wbm-4-28433 (Hf3GaO). Assigning anion correction to only the most electronegative atom.
  adjustments: list[EnergyAdjustment] = self.get_adjustments(entry)
C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\pymatgen\analysis\compatibility\__init__.py:631: UserWarning: Failed to guess oxidation states for Entry wbm-5-10472 (PaInRe). Assigning anion correction to only the most electronegative atom.
  adjustments: list[EnergyAdjustment] = self.get_adjustments(entry)
C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\pymatgen\analysis\compatibility\__init__.py:631: UserWarning: Failed to guess oxidation states for Entry wbm-2-30414 (NaAu). Assigning anion correction to only the most electronegative atom.
  adjustments: list[EnergyAdjustment] = self.get_adjustments(entry)
C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\pymatgen\analysis\compatibility\__init__.py:631: UserWarning: Failed to guess oxidation states for Entry wbm-2-17117 (In2Fe3Ru). Assigning anion correction to only the most electronegative atom.
  adjustments: list[EnergyAdjustment] = self.get_adjustments(entry)

100%|██████████| 20/20 [00:00<00:00, 105.30it/s]
```

### 2026-07-03 04:58 UTC — layerB mace pre-smoke 20 run2 variance bound

```
$ C:\Users\07013\Desktop\0702fable\reprolab\.venv\Scripts\python.exe scripts\layer_b_mace_relax.py --limit 20 --out experiments/layer-b/mace-mp-0/presmoke20-run2.jsonl.gz
```

- exit code: **0**  | duration: 47.0s  | raw log: `logs/cmd-20260703-045859.log`

output tail:
```
cuequivariance or cuequivariance_torch is not available. Cuequivariance acceleration will be disabled.
loaded 20 initial structures in 4.1s
Using Materials Project MACE for MACECalculator with C:\Users\07013\.cache\mace/20231203mace128L1_epoch199model
Using float64 for MACECalculator, which is slower but more accurate. Recommended for geometry optimization.
this run: 20 new, 0 resumed, 0 failed
versions: mace-torch 0.3.16 | torch 2.11.0+cu128 | numpy 2.4.6 | device cuda (NVIDIA GeForce RTX 4090)
protocol: MACE-MP-0 FIRE steps<=500 fmax=0.05 FrechetCellFilter float64 enable_cueq=False
relaxed 20/20 | failures 0
s/structure: mean 1.73 | median 1.36 | max 5.37
converged: 20/20
wrote C:\Users\07013\Desktop\0702fable\reprolab\experiments\layer-b\mace-mp-0\presmoke20-run2.jsonl.gz
C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\e3nn\o3\_wigner.py:10: UserWarning: Environment variable TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD detected, since the`weights_only` argument was not explicitly passed to `torch.load`, forcing weights_only=False.
  _Jd, _W3j_flat, _W3j_indices = torch.load(os.path.join(os.path.dirname(__file__), 'constants.pt'))
C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\mace\calculators\mace.py:226: UserWarning: Environment variable TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD detected, since the`weights_only` argument was not explicitly passed to `torch.load`, forcing weights_only=False.
  torch.load(f=model_path, map_location=device)
```

### 2026-07-03 04:59 UTC — layerB mace score pre-smoke 20 with variance

```
$ C:\Users\07013\Desktop\0702fable\reprolab\.venv\Scripts\python.exe scripts\layer_b_score.py --model mace-mp-0 --preds experiments/layer-b/mace-mp-0/presmoke20-run1.jsonl.gz experiments/layer-b/mace-mp-0/presmoke20-run2.jsonl.gz --out papers/matbench-discovery/metric_check-layer-b-mace-mp-0-presmoke20.md
```

- exit code: **0**  | duration: 22.2s  | raw log: `logs/cmd-20260703-045951.log`

output tail:
```
  adjustments: list[EnergyAdjustment] = self.get_adjustments(entry)
C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\pymatgen\analysis\compatibility\__init__.py:631: UserWarning: Failed to guess oxidation states for Entry wbm-4-32299 (OsAuS2). Assigning anion correction to only the most electronegative atom.
  adjustments: list[EnergyAdjustment] = self.get_adjustments(entry)
C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\pymatgen\analysis\compatibility\__init__.py:631: UserWarning: Failed to guess oxidation states for Entry wbm-2-24011 (Li4InO5). Assigning anion correction to only the most electronegative atom.
  adjustments: list[EnergyAdjustment] = self.get_adjustments(entry)
C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\pymatgen\analysis\compatibility\__init__.py:631: UserWarning: Failed to guess oxidation states for Entry wbm-4-28433 (Hf3GaO). Assigning anion correction to only the most electronegative atom.
  adjustments: list[EnergyAdjustment] = self.get_adjustments(entry)
C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\pymatgen\analysis\compatibility\__init__.py:631: UserWarning: Failed to guess oxidation states for Entry wbm-5-10472 (PaInRe). Assigning anion correction to only the most electronegative atom.
  adjustments: list[EnergyAdjustment] = self.get_adjustments(entry)
C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\pymatgen\analysis\compatibility\__init__.py:631: UserWarning: Failed to guess oxidation states for Entry wbm-2-30414 (NaAu). Assigning anion correction to only the most electronegative atom.
  adjustments: list[EnergyAdjustment] = self.get_adjustments(entry)
C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\pymatgen\analysis\compatibility\__init__.py:631: UserWarning: Failed to guess oxidation states for Entry wbm-2-17117 (In2Fe3Ru). Assigning anion correction to only the most electronegative atom.
  adjustments: list[EnergyAdjustment] = self.get_adjustments(entry)

100%|██████████| 20/20 [00:00<00:00, 126.71it/s]
```

### 2026-07-03 05:01 UTC — layerB mace smoke 500 run1

```
$ C:\Users\07013\Desktop\0702fable\reprolab\.venv\Scripts\python.exe scripts\layer_b_mace_relax.py --out experiments/layer-b/mace-mp-0/smoke500-run1.jsonl.gz
```

- exit code: **0**  | duration: 604.9s  | raw log: `logs/cmd-20260703-050107.log`

output tail:
```
  return f(*arrays, *other_args, **kwargs)
C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\scipy\_lib\_util.py:1181: RuntimeWarning: logm result may be inaccurate, approximate err = 2.95666454440985e-13
  return f(*arrays, *other_args, **kwargs)
C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\scipy\_lib\_util.py:1181: RuntimeWarning: logm result may be inaccurate, approximate err = 2.914837108413709e-13
  return f(*arrays, *other_args, **kwargs)
C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\scipy\_lib\_util.py:1181: RuntimeWarning: logm result may be inaccurate, approximate err = 2.9766483352909804e-13
  return f(*arrays, *other_args, **kwargs)
C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\scipy\_lib\_util.py:1181: RuntimeWarning: logm result may be inaccurate, approximate err = 2.931529629691958e-13
  return f(*arrays, *other_args, **kwargs)
C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\scipy\_lib\_util.py:1181: RuntimeWarning: logm result may be inaccurate, approximate err = 2.931721265075548e-13
  return f(*arrays, *other_args, **kwargs)
C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\scipy\_lib\_util.py:1181: RuntimeWarning: logm result may be inaccurate, approximate err = 2.9516911088077894e-13
  return f(*arrays, *other_args, **kwargs)
C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\scipy\_lib\_util.py:1181: RuntimeWarning: logm result may be inaccurate, approximate err = 2.922714458308905e-13
  return f(*arrays, *other_args, **kwargs)
```

### 2026-07-03 05:11 UTC — layerB mace score smoke500 vs published

```
$ C:\Users\07013\Desktop\0702fable\reprolab\.venv\Scripts\python.exe scripts\layer_b_score.py --model mace-mp-0 --preds experiments/layer-b/mace-mp-0/smoke500-run1.jsonl.gz --out papers/matbench-discovery/metric_check-layer-b-mace-mp-0-smoke500.md
```

- exit code: **0**  | duration: 22.1s  | raw log: `logs/cmd-20260703-051119.log`

output tail:
```
  adjustments: list[EnergyAdjustment] = self.get_adjustments(entry)
C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\pymatgen\analysis\compatibility\__init__.py:631: UserWarning: Failed to guess oxidation states for Entry wbm-4-5675 (Ca6Bi2Os). Assigning anion correction to only the most electronegative atom.
  adjustments: list[EnergyAdjustment] = self.get_adjustments(entry)
C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\pymatgen\analysis\compatibility\__init__.py:631: UserWarning: Failed to guess oxidation states for Entry wbm-1-9501 (TlCdPt2). Assigning anion correction to only the most electronegative atom.
  adjustments: list[EnergyAdjustment] = self.get_adjustments(entry)
C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\pymatgen\analysis\compatibility\__init__.py:631: UserWarning: Failed to guess oxidation states for Entry wbm-3-2353 (Al3V3ZnGe2). Assigning anion correction to only the most electronegative atom.
  adjustments: list[EnergyAdjustment] = self.get_adjustments(entry)
C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\pymatgen\analysis\compatibility\__init__.py:631: UserWarning: Failed to guess oxidation states for Entry wbm-5-21973 (V2NiRh2). Assigning anion correction to only the most electronegative atom.
  adjustments: list[EnergyAdjustment] = self.get_adjustments(entry)
C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\pymatgen\analysis\compatibility\__init__.py:631: UserWarning: Failed to guess oxidation states for Entry wbm-2-2593 (DyAlPt). Assigning anion correction to only the most electronegative atom.
  adjustments: list[EnergyAdjustment] = self.get_adjustments(entry)
C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\pymatgen\analysis\compatibility\__init__.py:631: UserWarning: Failed to guess oxidation states for Entry wbm-4-14070 (PrGaRu). Assigning anion correction to only the most electronegative atom.
  adjustments: list[EnergyAdjustment] = self.get_adjustments(entry)

100%|██████████| 500/500 [00:00<00:00, 1222.06it/s]
```

### 2026-07-03 05:12 UTC — capture env after MACE Layer B deps

```
$ C:\Users\07013\Desktop\0702fable\reprolab\.venv\Scripts\python.exe scripts\capture_env.py
```

- exit code: **0**  | duration: 0.7s  | raw log: `logs/cmd-20260703-051222.log`

output tail:
```
wrote C:\Users\07013\Desktop\0702fable\reprolab\logs\env-20260703-051223.json
wrote C:\Users\07013\Desktop\0702fable\reprolab\papers\matbench-discovery\environment.md
```

### 2026-07-03 05:12 UTC — refresh requirements frozen after MACE deps

```
$ powershell -NoProfile -Command & 'C:\Users\07013\Desktop\0702fable\reprolab\.venv\Scripts\python.exe' -m pip freeze | Set-Content -Encoding ascii 'papers\matbench-discovery\requirements-frozen.txt'
```

- exit code: **0**  | duration: 1.2s  | raw log: `logs/cmd-20260703-051244.log`

output tail:
```

```

### 2026-07-03 05:14 UTC — assemble report after MACE Layer B smoke

```
$ C:\Users\07013\Desktop\0702fable\reprolab\.venv\Scripts\python.exe scripts\make_report.py
```

- exit code: **0**  | duration: 0.1s  | raw log: `logs/cmd-20260703-051409.log`

output tail:
```
wrote C:\Users\07013\Desktop\0702fable\reprolab\reports\paper-001-matbench-discovery-audit.md
```

### 2026-07-03 05:14 UTC — verify MACE Layer B scripts py_compile

```
$ C:\Users\07013\Desktop\0702fable\reprolab\.venv\Scripts\python.exe -m py_compile scripts\layer_b_score.py scripts\layer_b_mace_relax.py
```

- exit code: **0**  | duration: 0.1s  | raw log: `logs/cmd-20260703-051420.log`

output tail:
```

```

### 2026-07-03 05:14 UTC — verify MACE Layer B scripts ruff

```
$ C:\Users\07013\Desktop\0702fable\reprolab\.venv\Scripts\python.exe -m ruff check scripts\layer_b_score.py scripts\layer_b_mace_relax.py
```

- exit code: **0**  | duration: 0.1s  | raw log: `logs/cmd-20260703-051424.log`

output tail:
```
All checks passed!
```

### 2026-07-03 05:14 UTC — assemble report after verification logs

```
$ C:\Users\07013\Desktop\0702fable\reprolab\.venv\Scripts\python.exe scripts\make_report.py
```

- exit code: **0**  | duration: 0.1s  | raw log: `logs/cmd-20260703-051428.log`

output tail:
```
wrote C:\Users\07013\Desktop\0702fable\reprolab\reports\paper-001-matbench-discovery-audit.md
```

### 2026-07-03 05:14 UTC — verify MACE Layer B scripts py_compile after doc update

```
$ C:\Users\07013\Desktop\0702fable\reprolab\.venv\Scripts\python.exe -m py_compile scripts\layer_b_score.py scripts\layer_b_mace_relax.py
```

- exit code: **0**  | duration: 0.1s  | raw log: `logs/cmd-20260703-051459.log`

output tail:
```

```

### 2026-07-03 05:15 UTC — verify MACE Layer B scripts ruff after doc update

```
$ C:\Users\07013\Desktop\0702fable\reprolab\.venv\Scripts\python.exe -m ruff check scripts\layer_b_score.py scripts\layer_b_mace_relax.py
```

- exit code: **0**  | duration: 0.1s  | raw log: `logs/cmd-20260703-051505.log`

output tail:
```
All checks passed!
```

### 2026-07-03 05:15 UTC — assemble report after final MACE script checks

```
$ C:\Users\07013\Desktop\0702fable\reprolab\.venv\Scripts\python.exe scripts\make_report.py
```

- exit code: **0**  | duration: 0.1s  | raw log: `logs/cmd-20260703-051514.log`

output tail:
```
wrote C:\Users\07013\Desktop\0702fable\reprolab\reports\paper-001-matbench-discovery-audit.md
```

### 2026-07-03 05:15 UTC — layerB mace score smoke500 with flip table

```
$ C:\Users\07013\Desktop\0702fable\reprolab\.venv\Scripts\python.exe scripts\layer_b_score.py --model mace-mp-0 --preds experiments/layer-b/mace-mp-0/smoke500-run1.jsonl.gz --out papers/matbench-discovery/metric_check-layer-b-mace-mp-0-smoke500.md
```

- exit code: **0**  | duration: 21.3s  | raw log: `logs/cmd-20260703-051544.log`

output tail:
```
  adjustments: list[EnergyAdjustment] = self.get_adjustments(entry)
C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\pymatgen\analysis\compatibility\__init__.py:631: UserWarning: Failed to guess oxidation states for Entry wbm-4-5675 (Ca6Bi2Os). Assigning anion correction to only the most electronegative atom.
  adjustments: list[EnergyAdjustment] = self.get_adjustments(entry)
C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\pymatgen\analysis\compatibility\__init__.py:631: UserWarning: Failed to guess oxidation states for Entry wbm-1-9501 (TlCdPt2). Assigning anion correction to only the most electronegative atom.
  adjustments: list[EnergyAdjustment] = self.get_adjustments(entry)
C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\pymatgen\analysis\compatibility\__init__.py:631: UserWarning: Failed to guess oxidation states for Entry wbm-3-2353 (Al3V3ZnGe2). Assigning anion correction to only the most electronegative atom.
  adjustments: list[EnergyAdjustment] = self.get_adjustments(entry)
C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\pymatgen\analysis\compatibility\__init__.py:631: UserWarning: Failed to guess oxidation states for Entry wbm-5-21973 (V2NiRh2). Assigning anion correction to only the most electronegative atom.
  adjustments: list[EnergyAdjustment] = self.get_adjustments(entry)
C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\pymatgen\analysis\compatibility\__init__.py:631: UserWarning: Failed to guess oxidation states for Entry wbm-2-2593 (DyAlPt). Assigning anion correction to only the most electronegative atom.
  adjustments: list[EnergyAdjustment] = self.get_adjustments(entry)
C:\Users\07013\Desktop\0702fable\reprolab\.venv\Lib\site-packages\pymatgen\analysis\compatibility\__init__.py:631: UserWarning: Failed to guess oxidation states for Entry wbm-4-14070 (PrGaRu). Assigning anion correction to only the most electronegative atom.
  adjustments: list[EnergyAdjustment] = self.get_adjustments(entry)

100%|██████████| 500/500 [00:00<00:00, 1319.08it/s]
```

### 2026-07-03 05:16 UTC — verify layer_b_score chgnet compatibility after flip table

```
$ C:\Users\07013\Desktop\0702fable\reprolab\.venv\Scripts\python.exe scripts\layer_b_score.py --model chgnet-0.3.0 --preds experiments/layer-b/chgnet/smoke500-run1.jsonl.gz --out logs/chgnet-score-regression-layer_b_score.md
```

- exit code: **0**  | duration: 4.4s  | raw log: `logs/cmd-20260703-051650.log`

output tail:
```
| Accuracy | 0.866 | 0.866 | 0.866 | 0.866 |
| MAE | 0.067 | 0.067 | 0.067 | 0.067 |
| RMSE | 0.104 | 0.104 | 0.104 | 0.104 |
| TP | 47 | 47 | 47 | 47 |
| FP | 47 | 47 | 47 | 47 |
| TN | 386 | 386 | 386 | 386 |
| FN | 20 | 20 | 20 | 20 |

wrote C:\Users\07013\Desktop\0702fable\reprolab\logs\chgnet-score-regression-layer_b_score.md
C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.11_3.11.2544.0_x64__qbz5n2kfra8p0\Lib\functools.py:1001: UserWarning: No Pauling electronegativity for Ne. Setting to NaN. This has no physical meaning, and is mainly done to avoid errors caused by the code expecting a float.
  val = self.func(instance)
C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.11_3.11.2544.0_x64__qbz5n2kfra8p0\Lib\functools.py:1001: UserWarning: No Pauling electronegativity for He. Setting to NaN. This has no physical meaning, and is mainly done to avoid errors caused by the code expecting a float.
  val = self.func(instance)
C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.11_3.11.2544.0_x64__qbz5n2kfra8p0\Lib\functools.py:1001: UserWarning: No Pauling electronegativity for Ar. Setting to NaN. This has no physical meaning, and is mainly done to avoid errors caused by the code expecting a float.
  val = self.func(instance)
```

### 2026-07-03 05:16 UTC — verify final MACE scorer py_compile

```
$ C:\Users\07013\Desktop\0702fable\reprolab\.venv\Scripts\python.exe -m py_compile scripts\layer_b_score.py scripts\layer_b_mace_relax.py
```

- exit code: **0**  | duration: 0.1s  | raw log: `logs/cmd-20260703-051659.log`

output tail:
```

```

### 2026-07-03 05:17 UTC — verify final MACE scorer ruff

```
$ C:\Users\07013\Desktop\0702fable\reprolab\.venv\Scripts\python.exe -m ruff check scripts\layer_b_score.py scripts\layer_b_mace_relax.py
```

- exit code: **0**  | duration: 0.1s  | raw log: `logs/cmd-20260703-051703.log`

output tail:
```
All checks passed!
```

### 2026-07-03 05:17 UTC — assemble report after MACE flip diagnostics

```
$ C:\Users\07013\Desktop\0702fable\reprolab\.venv\Scripts\python.exe scripts\make_report.py
```

- exit code: **0**  | duration: 0.1s  | raw log: `logs/cmd-20260703-051707.log`

output tail:
```
wrote C:\Users\07013\Desktop\0702fable\reprolab\reports\paper-001-matbench-discovery-audit.md
```

### 2026-07-03 05:17 UTC — assemble report after summary date and flip wording

```
$ C:\Users\07013\Desktop\0702fable\reprolab\.venv\Scripts\python.exe scripts\make_report.py
```

- exit code: **0**  | duration: 0.1s  | raw log: `logs/cmd-20260703-051730.log`

output tail:
```
wrote C:\Users\07013\Desktop\0702fable\reprolab\reports\paper-001-matbench-discovery-audit.md
```
