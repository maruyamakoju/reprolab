# Layer B Probe - JARVIS-Leaderboard

Date: 2026-07-03

Question: can one public JARVIS-Leaderboard contribution runner be executed as a
small model-execution smoke in the current ReproLab environment?

## Result

No model-execution smoke was run in the shared Matbench audit venv. The public
JARVIS contribution scripts are available, but the tractable baseline candidates
need extra dependencies and minor protocol adaptation before they can serve as a
clean Layer B smoke.

The dependency resolver itself is not blocked: `pip install --dry-run jarvis-tools
matminer xgboost lightgbm` succeeds. The blocker is practical isolation and script
fit, not package availability.

## Environment probe

Import check in the current `.venv`:

| module | status |
|---|---|
| sklearn | present (`1.9.0`) |
| pymatgen | present |
| jarvis | missing |
| matminer | missing |
| xgboost | missing |
| lightgbm | missing |

The dry-run install would add:

`jarvis-tools-2026.6.12`, `matminer-0.10.1`, `xgboost-3.2.0`,
`lightgbm-4.6.0`, plus dependency updates/additions including `pandas-2.3.3`,
`pymongo`, `dnspython`, `toolz`, `xmltodict`, and `pytz`.

Because Paper-001 already depends on this venv for traceability, the safer next
move is a separate JARVIS-specific env rather than mutating the existing one.

## Runner inspection

| candidate | inspected files | fit for immediate smoke |
|---|---|---|
| `matminer_rf` | `contributions/matminer_rf/run.py`, `run.bash` | Not immediate. It imports `jarvis` and `matminer`, then hardcodes `task = 'SinglePropertyPrediction'` and `for db in ['snumat']`. A dft_3d formation-energy smoke needs a small wrapper or patch. |
| `matminer_xgboost` | `contributions/matminer_xgboost/run.py`, `run.bash` | Not immediate. It adds `xgboost` and hardcodes `tree_method = 'gpu_hist'` plus the same `snumat` loop. A CPU smoke would need `hist` and the target dataset/property wired explicitly. |
| `cfid` | `contributions/cfid/run.py`, `run.sh` | Not immediate. It imports `lightgbm` and `jarvis`, iterates a broad property list, and expects benchmark zips under `../../dataset/AI/...` rather than the current sparse-checkout benchmark path. |
| `cfid_chem` | `contributions/cfid_chem/run.py`, `run_chem.py` | Not immediate. It also needs `lightgbm` and JARVIS CFID descriptors, writes full POSCAR directories, and is heavier than the desired first smoke. |

## Decision and follow-up

Treat this as a completed execution-path probe, not a failed reproduction. The
next productive Layer B move was:

1. create an isolated JARVIS env;
2. install only the dependencies for `matminer_rf`;
3. patch or wrap the runner so `db='dft_3d'` and
   `prop='formation_energy_peratom'` are explicit;
4. run a bounded CPU smoke on the official train/val/test split;
5. score the generated test CSV through `scripts/jarvis_score.py`.

If that proves too slow, stop Paper-002 at the current Layer A result and use the
Layer B probe as the documented reason.

Follow-up status: a bounded `matminer_rf`-style pre-smoke passed in `env/jarvis`.
See `layer_b_matminer_rf_smoke.md`.
