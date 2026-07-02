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
