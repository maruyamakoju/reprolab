# Paper-003 candidate screen - Matbench v0.1

Status: selected as the next audit target on 2026-07-03.

## Why this candidate

Matbench v0.1 is a strong Paper-003 candidate because the official repository
commits the exact leaderboard submission artifacts needed for a CPU-first audit:
`results.json.gz`, `info.json`, and source code or notebooks under
`benchmarks/matbench_v0.1_*`.

The official submission docs require those three artifacts for leaderboard
submissions. The repository also includes the benchmark metadata JSON and
validation split JSON, while the targets are loadable through Matminer datasets.
That gives the same first move used in Paper-001 and Paper-002: recompute published
scores from released predictions before attempting model execution.

## Initial slice

Seed submission: `matbench_v0.1_rf` (RF-SCM/Magpie reference baseline).

Seed tasks:

| task | type | rows | reason |
|---|---|---:|---|
| `matbench_steels` | regression | 312 | small composition task; fast target load |
| `matbench_expt_is_metal` | classification | 4,921 | small classification task; checks non-regression metrics |

Result: `scripts/matbench_score.py` recomputed 10 fold scores from
`results.json.gz`, official split IDs, and Matminer targets. The max absolute
stored-vs-recomputed score delta is `1.1102230246251565e-16`.

Report: `layer_a_score_recompute.md`.

## Candidate comparison

| candidate | disposition | reason |
|---|---|---|
| Matbench v0.1 | selected | public prediction artifacts and source files are committed per submission |
| Open Catalyst Project | defer | scientifically strong but larger data/model path and less direct for a quick prediction-artifact audit |
| Open MatSci ML Toolkit | defer | useful framework, but less direct as a single leaderboard-with-predictions target |
| matbench-genmetrics | defer | relevant to generative materials evaluation, but the current audit line is property-prediction leaderboard reproducibility |

## Risks and notes

- Full all-task score recomputation can become heavy because the structure tasks
  include large pymatgen object datasets.
- The shared `.venv` lacks `matminer`; the current seed uses the already available
  isolated `env/jarvis`. A dedicated `env/matbench` can be created if this audit
  grows.
- `scripts/run_command.py` originally used second-level raw-log names; two parallel
  commands collided while scouting. It now uses microsecond-level names.
- The first runnable source-code candidate is `matbench_v0.1_TPOT`. Its notebook
  path can be replayed for `matbench_steels`, but it refits stochastic estimators
  without a submitted random seed, so public-source execution does not regenerate
  the committed predictions exactly.
- `source_artifact_inventory.md` records the broader source-artifact scan: 28
  submission directories, 11 direct `run.py` files, 14 notebooks, and one
  pickle/joblib model artifact.
