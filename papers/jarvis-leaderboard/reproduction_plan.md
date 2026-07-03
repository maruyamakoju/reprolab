# Reproduction Plan - JARVIS-Leaderboard (Paper-002 candidate)

Status: Layer A for the selected benchmark passed for all 15 submissions listed in
the pinned docs page on 2026-07-03.

## 0. Why this candidate

JARVIS-Leaderboard is a strong Paper-002 candidate because its official benchmark
pages expose the exact artifacts needed for a CPU-only metric audit: submission CSV
zip, benchmark JSON zip, run script, and metadata for each contribution. That makes
it possible to repeat the same first move as Paper-001: recompute metrics from
published predictions before attempting any model execution.

## 1. Initial target

Benchmark:
`AI-SinglePropertyPrediction-formation_energy_peratom-dft_3d-test-mae`

Official page:
https://pages.nist.gov/jarvis_leaderboard/AI/SinglePropertyPrediction/dft_3d_formation_energy_peratom/

Seed submissions:

| model | official MAE | reason |
|---|---:|---|
| kgcnn_coGN | 0.0271 | top listed score for this page |
| alignn_model | 0.0331 | JARVIS/NIST baseline family |
| matminer_rf | 0.096 | simpler classical baseline |

## 2. Metric path

Upstream path in the pinned clone:
`vendor/jarvis_leaderboard/jarvis_leaderboard/rebuild.py::get_metric_value`.

For MAE tasks the upstream function:

1. reads the contribution CSV zip with `id,prediction`;
2. opens the benchmark JSON zip named `{dataset}_{property}.json.zip`;
3. selects the requested split (`test`);
4. merges on `id`;
5. computes `mean_absolute_error(actual, prediction)`;
6. rounds the displayed score to 4 decimals, except pages may show fewer trailing
   digits for some submissions.

`scripts/jarvis_score.py` mirrors this path with stdlib-only parsing.

## 3. Command

```bash
python scripts/run_command.py --paper jarvis-leaderboard \
  --note "paper002 layerA JARVIS formation energy seed models" -- \
  .venv/Scripts/python.exe scripts/jarvis_score.py \
    --vendor vendor/jarvis_leaderboard \
    --out papers/jarvis-leaderboard/metric_check.md
```

## 4. Pass criteria

- All selected CSV ids exactly match the JSON `test` split ids.
- Recomputed MAE matches the official page within the page's displayed rounding.
- Any mismatch becomes a blocker note before broadening to all submissions.

## 5. Current result

`scripts/jarvis_score.py --models all` recomputed MAE for all 15 listed submissions.
Every submission matched the official page within displayed rounding, and every CSV
id set exactly matched the JSON `test` split (5,572 rows).

Closest adjacent official gaps in the selected leaderboard are small:

- `kgcnn_coNGN` vs `potnet`: 0.0002 MAE
- `matformer_256` vs `alignn_model`: 0.0009 MAE
- `kgcnn_coGN` vs `kgcnn_coNGN`: 0.0020 MAE

The page reports point estimates only; uncertainty or split-sensitivity checks would
be the natural Layer C analogue.

## 6. Next

1. Decide whether to broaden Layer A across more JARVIS tasks.
2. Check whether a Layer B model-execution smoke is practical for one tractable
   baseline.
3. Add a small leaderboard-resolution analysis if this becomes the main Paper-002
   target rather than a candidate.
