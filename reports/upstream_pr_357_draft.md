# PR draft — upstream fix for janosh/matbench-discovery#357

**SUBMITTED 2026-07-03 as [PR #359](https://github.com/janosh/matbench-discovery/pull/359)**
(24–48h rule: no maintainer response on #357 since 2026-07-02, opened politely per
the decision table). Body below is what was submitted, plus a short courtesy preamble.

Branch: `maruyamakoju/matbench-discovery:fix-wbm-initial-structures-md5`
(tip `0c753e0`, based on upstream `eaa7550`; lint-clean under upstream's pinned
ruff 0.15.20 check+format).

Post-submission updates:

- `b50b67b`: addressed CodeRabbit's I/O nit by hashing chunks while streaming
  downloads instead of re-reading the completed `.part` file.
- `0c753e0`: addressed CodeRabbit's caller-surfacing concern by making
  `DataFiles.path` raise `FileNotFoundError` if an attempted download/verification
  still leaves no local file; added a regression test.
- PR body edited to follow the upstream PR template explicitly, marking
  model-submission checklist items as N/A because this is a data-integrity fix.
- Local verification after both updates:
  `ruff check matbench_discovery/remote/fetch.py matbench_discovery/enums.py tests/remote/test_fetch.py tests/test_enums.py`,
  `ruff format --check ...`, and
  `pytest tests/remote/test_fetch.py tests/test_enums.py` -> 57 passed.

---

## Title

Fix stale/missing md5s in data-files.yml, verify checksums on download

## PR body

### Summary

Fixes the stale md5 metadata reported in #357 and makes the declared checksums
actually enforced, so future metadata drift is caught at download time instead of
silently ignored.

- `data-files.yml`: corrected **3 stale** md5 values and filled **2 missing** ones.
  Cross-checking every entry against the Figshare API (articles 22715158 / 23713842)
  found the drift is broader than the single file reported in #357:
  - `wbm_initial_structures` and `wbm_computed_structure_entries` still carried the
    md5s of the older `.json.bz2` artifacts their current `.jsonl.gz` files replaced
    (Figshare file ids `40344466` / `40344463`)
  - `phonondb_pbe_103_structures` matched no file currently in the article
  - `wbm_dft_geo_opt_symprec_1e_2` / `_1e_5` had empty `md5:` fields
  - all other declared md5s (incl. `aimd_reference_md_trajectories`) verified OK
- `remote/fetch.py::download_file` gains an optional `md5` argument: the download is
  hashed before it replaces the destination; on mismatch it is discarded, any
  previously cached file is left unchanged, and an error is printed (keeping this
  module's print-not-raise convention — happy to switch to raising if preferred).
- `maybe_auto_download_file` forwards the new argument; `DataFiles.path` passes the
  registry value, so `data-files.yml` checksums are enforced from now on.

### Motivation

Found during an independent reproducibility audit of Matbench Discovery
(https://github.com/maruyamakoju/reprolab). A fresh download of
`wbm_initial_structures` that was verified against the registry md5 appeared
corrupted, when in fact the file was intact and the registry value referred to a
superseded artifact. Because the downloader never verified checksums, this could not
surface inside the normal pipeline — only for independent users treating the
registry as authoritative.

### Reproduction

```python
# at eaa7550, for each data-files.yml entry with a figshare URL:
# GET https://api.figshare.com/v2/articles/22715158/files (and 23713842)
# compare entry's declared md5 to the API computed_md5 for its file id
# -> 3 stale, 2 missing, rest OK (details in the summary above)
```

### Test plan

- `tests/remote/test_fetch.py`: two new tests —
  `test_download_file_md5_match` (verified download is kept) and
  `test_download_file_md5_mismatch_discards_download` (mismatch is discarded, a
  previously cached file survives, no `.part` debris). Full file: **22/22 pass**.
- `tests/test_enums.py`: **34/34 pass** (covers the `DataFiles.path` change).
- Real-network check: `download_file` with the correct md5 for
  `mp_elemental_ref_entries` (Figshare file 40387775) keeps the file; with a wrong
  md5 it discards the download and prints the mismatch.

### Relation to #357

Implements "option B" from the issue: update the stale metadata **and** add
verification so the next drift is detected. If you'd rather take the metadata-only
fix (option A), I can trim the patch to the `data-files.yml` changes.
