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
