# External Release Packet - Paper-001 Matbench Discovery Audit

Date: 2026-07-03
Repo: https://github.com/maruyamakoju/reprolab
Audit target: https://github.com/janosh/matbench-discovery at commit `eaa7550`

This packet is the short handoff for maintainers, reviewers, or collaborators who
need the result without reading the full assembled report first.

## Bottom line

The Matbench Discovery discovery-task leaderboard is reproducible in the audited
paths.

- Layer A recomputed the released leaderboard metrics for CHGNet, SevenNet-0,
  MACE-MP-0, and ORB v2 from the published prediction CSVs. All 4/4 models match
  the official YAML exactly on both audited subsets, including every integer
  confusion-matrix count.
- Layer B regenerated predictions from model execution for CHGNet, MACE-MP-0, and
  ORB v2 on the same deterministic 500-structure WBM subset. All three pass the
  pre-registered smoke criteria.
- Layer C found two issues that matter for interpretation, not broad failures of
  the benchmark: adjacent leaderboard ranks often lack uncertainty separation, and
  a small fraction of WBM ground-truth `e_above_hull` labels is pymatgen-version
  dependent through MP2020 correction assignment.

## Key numbers

| Check | Scope | Result |
|---|---:|---|
| Layer A metric recomputation | 4 models x 2 subsets | 8/8 exact matches |
| CHGNet Layer B | 500 structures | median abs delta e_form = 0.03 meV/atom; 100.0% classification agreement |
| MACE-MP-0 Layer B | 500 structures | median abs delta e_form = 0.03 meV/atom; 99.6% classification agreement |
| ORB v2 Layer B | 500 structures | median abs delta e_form = 0.05 meV/atom; 100.0% classification agreement |
| Ground-truth hull recomputation | 500 structures | 497/500 match to <=0.001 meV/atom; 3 correction-drift outliers |
| Leaderboard uncertainty audit | 60-model board | 43/59 adjacent F1 gaps smaller than one measured CI width |

## Evidence map

- Full assembled report: `reports/paper-001-matbench-discovery-audit.md`
- One-page summary: `reports/one_page_summary.md`
- Main README / reproduction commands: `README.md`
- Layer A per-model metric checks:
  - `papers/matbench-discovery/metric_check.md`
  - `papers/matbench-discovery/metric_check-sevennet.md`
  - `papers/matbench-discovery/metric_check-mace-mp-0.md`
  - `papers/matbench-discovery/metric_check-orb-v2.md`
- Layer B regeneration checks:
  - `papers/matbench-discovery/metric_check-layer-b-chgnet-smoke500.md`
  - `papers/matbench-discovery/metric_check-layer-b-mace-mp-0-smoke500.md`
  - `papers/matbench-discovery/metric_check-layer-b-orb-v2-smoke500-fmax002.md`
- Statistical audit: `papers/matbench-discovery/layer_c_statistical_audit.md`
- Ground-truth hull audit: `papers/matbench-discovery/layer_c_gt_hull_check.md`
- Failure and protocol notes: `papers/matbench-discovery/failure_notes.md`
- Command log: `papers/matbench-discovery/run_log.md`
- Frozen environment: `papers/matbench-discovery/requirements-frozen.txt`

## Upstream status

- Issue #357 reported stale/missing md5 metadata and missing checksum verification.
- PR #359 implements md5 metadata fixes plus download-time verification.
- Issue #358 reported pymatgen-version-dependent WBM ground-truth hull labels.
- PR #360 adds a docs-only WBM provenance note for the correction-version
  dependence.

## Public wording

Suggested short wording:

> I ran an independent reproducibility audit of the Matbench Discovery discovery
> task. The result is mostly positive: published metrics reproduce exactly for four
> released models, and predictions regenerate from model execution for three models
> on a deterministic 500-structure WBM subset. The audit also surfaced practical
> reproducibility issues around Figshare URLs, stale md5 metadata, ORB v2 protocol
> ambiguity, leaderboard uncertainty, and pymatgen-version-dependent WBM hull labels.

## Claims to avoid

- Do not claim a full 257k-structure regeneration; Layer B is a deterministic
  500-structure vertical slice.
- Do not describe MACE-MP-0 large outliers as relaxation failures; the large cases
  coincide with the MP2020 correction-version drift isolated in Layer C.
- Do not compare subset-level Layer B metrics as leaderboard metrics; they are
  smoke-test diagnostics on the committed subset.
- Do not imply that Matbench Discovery broadly failed; the main reproducibility
  result is positive, with bounded metadata/protocol/statistical-interpretation
  findings.

## Next useful moves

1. Wait for upstream responses on PR #359 and PR #360.
2. If maintainers ask for a narrower patch, trim PR #359 to metadata-only and keep
   checksum verification as a follow-up.
3. Start Paper-002 with the same two-layer template: metric recomputation first,
   then a small model-execution slice only if Layer A is clean.
