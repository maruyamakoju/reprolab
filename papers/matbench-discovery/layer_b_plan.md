# Layer B Plan — regenerate predictions

Status: **PRE-SMOKE PASSED** (2026-07-02, branch `layer-b-chgnet-smoke`; results in
`metric_check-layer-b-chgnet-presmoke.md`). 20/20 structures relaxed on RTX 4090,
0 failures, all converged, mean 1.26 s/structure; regenerated e_form matches the
published values within 0.1 meV/atom (the published CSV's rounding precision),
100% classification agreement; run-to-run GPU variance ≤0.232 meV/atom.
Scaling to the 500-structure smoke is justified (est. ~10–15 min GPU) and awaits
go-decision. The design below is unchanged; §5 estimates were conservative.

Layer A closed at 4/4 (`v0.1-layer-a`); this plan defines the smallest vertical
slice of Layer B:

> model relaxation/inference → prediction CSV → the *same* Layer A metric path.

Goal is NOT to regenerate the leaderboard. It is to test, on a small traceable
subset, whether the *published predictions themselves* can be regenerated from
the published model + published initial structures.

## 1. Model: CHGNet (`chgnet-0.3.0`)

Chosen over the other three audited models because:

- **No separate checkpoint download.** The 0.3.0 pretrained weights ship inside the
  `chgnet` PyPI package (loaded by `StructOptimizer()` as the default model);
  MACE/SevenNet/ORB require fetching external checkpoint files.
- **It is the Layer A primary model** (`metric_check.md`), so the scoring path and
  official targets are already pinned in `metadata.yaml`.
- **The exact generation protocol is in the audited clone**:
  `models/chgnet/test_chgnet_discovery.py` — ASE FIRE relaxation via
  `chgnet.model.StructOptimizer`, `max_steps=500`, `fmax=0.05`,
  `relax_cell=True`, `cell_filter="FrechetCellFilter"`, final trajectory energy
  taken as the predicted energy.
- Pure PyTorch → runs on Windows + CUDA (RTX 4090/5090) without exotic deps.

Verify at runtime and log: the loaded model reports version 0.3.0
(`chgnet` prints the loaded weights version; record it in `run_log.md`).

## 2. Subset definition (traceable, committed)

- Universe: WBM `unique_prototypes` rows (the leaderboard's default subset),
  from the bundled ground truth `data/wbm/2023-12-13-wbm-summary.csv.gz`.
- Selection: sort by `material_id`, then `df.sample(n=500, random_state=42)`
  (pandas, fixed seed). Deterministic given the sorted frame.
- **Commit the resulting `material_id` list** as
  `papers/matbench-discovery/layer_b_subset.csv` together with its summary stats
  (n, % stable by DFT — expect ≈15.5%, the uniq-protos base rate).
- Pre-smoke: the **first 20 ids** of that list, used to (a) verify wiring,
  (b) measure per-structure runtime, (c) bound run-to-run variance (run twice).

## 3. Required data + weights

| Item | Source | Integrity |
|---|---|---|
| WBM initial structures | `wbm/2022-10-19-wbm-init-structs.jsonl.gz`, Figshare file `53161835` (use the `api.figshare.com/v2/file/download/` rewrite — landing URL is WAF-blocked, see failure_notes) | md5 `ff2c40a3a7bf65468852b67f0dbc67df` (from `matbench_discovery/data-files.yml`); large file — download in a separate logged step |
| CHGNet 0.3.0 weights | inside `pip install chgnet` | log package version + reported weights version |
| Elemental references for e_form | `data/mp/2023-02-07-mp-elemental-reference-entries.json.gz` (bundled in clone), applied via `matbench_discovery.energy.get_e_form_per_atom` — same call as upstream `models/chgnet/join_chgnet_preds.py` | in pinned clone `eaa7550` |

Upstream YAML pins old versions (torch 1.11, ase 3.22.0, pymatgen 2022.10.22).
We will NOT try to rebuild that 2023 environment; we run current versions,
snapshot them with `capture_env.py`, and treat version drift as a candidate
explanation for any disagreement (that asymmetry is itself a finding).

## 4. Commands (all via `run_command.py`, absolute venv python)

New scripts to be written at execution time (small, inspectable, like Layer A):

- `scripts/layer_b_relax.py` — load subset ids + initial structures, relax each
  with the upstream protocol (§1), write
  `experiments/layer-b/chgnet/<date>-smoke-relaxed.jsonl.gz`
  (`material_id`, final energy, n_steps, converged flag, wall time; per-structure
  try/except like upstream). `--ids`, `--limit`, `--device {cuda,cpu}` flags.
- `scripts/layer_b_score.py` — convert energies → `e_form_per_atom_chgnet` via
  `get_e_form_per_atom`, then score through the **same** Layer A path
  (reuse `compare_metrics.py` functions; do not fork the metric logic) against
  (a) DFT ground truth and (b) the published CHGNet prediction CSV restricted to
  the same ids. Output: `papers/matbench-discovery/metric_check-layer-b-chgnet.md`.

```text
1. <venv python abs path> scripts/run_command.py --note "layerB download init structs" -- ...
   (download + md5 check, separate process from compute — Layer A crash lesson)
2. ... --note "layerB make subset" -- python scripts/layer_b_subset.py   (writes layer_b_subset.csv)
3. ... --note "layerB pre-smoke 20 run1" -- python scripts/layer_b_relax.py --limit 20
4. ... --note "layerB pre-smoke 20 run2" -- python scripts/layer_b_relax.py --limit 20  (variance bound)
5. ... --note "layerB smoke 500" -- python scripts/layer_b_relax.py
6. ... --note "layerB score" -- python scripts/layer_b_score.py
```

## 5. Expected runtime (planning estimates — measuring them IS the pre-smoke)

WBM relaxations with CHGNet typically converge well under `max_steps=500`;
per-structure cost is dominated by graph construction + FIRE steps.

| Stage | RTX 4090 | RTX 5090 |
|---|---|---|
| Pre-smoke (20 structs) | ~1–3 min | ~1–2 min |
| Smoke (500 structs) | ~20–50 min (est. 2–6 s/struct) | ~15–35 min (~25–40% faster; workload is partly Python-overhead-bound) |
| Download init structs | bandwidth-bound (file is several hundred MB) | same |

If measured per-structure time exceeds ~30 s on GPU, shrink the subset to 100
(stopping criterion below) rather than letting the run sprawl.

## 6. Expected outputs

Committed (small, traceable):
- `papers/matbench-discovery/layer_b_subset.csv` — the 500 ids + stats
- `papers/matbench-discovery/metric_check-layer-b-chgnet.md` — regenerated vs
  published vs official, on the subset
- `run_log.md` entries for every command; `failure_notes.md` updates

Git-ignored (bulk): `experiments/layer-b/chgnet/*` relaxation outputs,
downloaded `wbm-init-structs.jsonl.gz`.

## 7. Comparison criteria (decided BEFORE running)

Bit-exact reproduction is **not** expected (GPU nondeterminism, torch/ase/pymatgen
drift since 2023). Pre-registered interpretation of per-structure
Δ = |e_form_regenerated − e_form_published| on the 500 ids:

- **Reproduces**: median Δ ≤ 10 meV/atom AND ≥ 95% stable/unstable classification
  agreement vs the published predictions.
- **Partial / investigate**: median Δ in 10–50 meV/atom — check convergence flags,
  version drift, run-to-run variance from the pre-smoke pair.
- **Finding**: median Δ > 50 meV/atom or systematic bias — document, do not tune
  until it matches.

Run-to-run variance from steps 3–4 must be ≪ the reproduce-threshold (10 meV/atom),
otherwise the threshold is not interpretable and that itself gets recorded.

## 8. Risks and stopping criteria

Risks: (a) dependency drift changes relaxation trajectories (most likely source of
Δ); (b) Windows CUDA torch install friction — pre-smoke has a `--device cpu`
fallback; (c) large download / WAF (use API rewrite + md5); (d) some WBM cells are
large → per-structure OOM/failures — catch and record like upstream does;
(e) native-crash flake seen in Layer A — keep download and compute in separate
processes.

Stop and reassess (do not push through) if:
- pre-smoke relaxation failure rate > 20%, or
- download md5 mismatches twice, or
- per-structure GPU time > 30 s (→ shrink subset to 100), or
- total GPU wall time would exceed **2 h** for the smoke run.

Hard non-goals for v0.2: no full-WBM (257k) relaxation, no leaderboard
regeneration, no model training, no metric-logic changes.
