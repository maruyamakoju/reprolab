# Project: ReproLab

## Goal
Perform independent **reproducibility audits** of AI-for-science papers and benchmarks.
Deliverable per paper: a report answering "can the code run, are the metrics
reproducible, are leaderboard values independently verifiable, what compute is
required, what fails?"

## Paper-001
Matbench Discovery reproducibility audit.
Riebesell et al., *A framework to evaluate machine learning crystal stability
predictions*, Nature Machine Intelligence 7, 836-847 (2025).
Upstream: https://github.com/janosh/matbench-discovery (MIT).

## Rules
- This is not a toy demo. External reproducibility is the point.
- Every command must be logged (use `scripts/run_command.py`, append to `run_log.md`).
- Every metric must trace back to specific code + data (file path + line).
- Do NOT do wet-lab protocol design.
- Do NOT generate new materials as the primary task (generation is out of scope for
  Paper-001; we only re-score existing published predictions).
- Do NOT touch secrets: no `.env`, SSH keys, browser cookies, or credential files.
- Do NOT run with "bypass permissions" mode. Approve tool calls explicitly.
- Cloned upstream code lives only in `vendor/` (git-ignored).
- Experiments run inside a venv/conda env, never against system Python.
- Prefer small, inspectable scripts over large opaque ones.
- If a result cannot be reproduced, document the *exact* blocker in `failure_notes.md`.

## Layout
```
reprolab/
  README.md                 # how to re-run everything
  CLAUDE.md                 # this file
  papers/matbench-discovery/
    metadata.yaml           # paper + benchmark facts, target metrics
    reproduction_plan.md    # metric -> code -> data -> command -> expected -> compare
    environment.md          # captured env (filled by capture_env.py)
    run_log.md              # every command + outcome
    metric_check.md         # official vs reproduced metric table
    failure_notes.md        # classified blockers
  reports/
    paper-001-matbench-discovery-audit.md   # final report (written later)
  scripts/
    capture_env.py          # snapshot OS/py/GPU/deps -> logs + environment.md
    run_command.py          # run + timestamp + log a command to run_log.md
    compare_metrics.py      # recompute discovery metrics, diff vs official YAML
    make_report.py          # assemble report from artifacts
  experiments/              # run outputs (git-ignored)
  logs/                     # env snapshots, raw command logs (git-ignored bulk)
  vendor/matbench-discovery # upstream clone (git-ignored)
```
