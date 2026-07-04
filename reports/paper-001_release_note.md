# Release note - Paper-001 Matbench Discovery audit

Date: 2026-07-04

## Headline

ReproLab's first audit independently reproduced the Matbench Discovery
discovery-task leaderboard for the audited paths and produced an upstream-merged
fix for data-file checksum verification.

## Short version

I ran an independent reproducibility audit of the Matbench Discovery discovery
task. The result is largely positive: released metrics reproduce exactly for four
models, and predictions regenerate from model execution for three models on a
deterministic 500-structure WBM subset. The audit also found practical issues in
data-file metadata, protocol clarity, leaderboard uncertainty, and WBM
ground-truth provenance. The checksum/provenance fix was merged upstream in
janosh/matbench-discovery#359 on 2026-07-04.

## Key results

- Layer A: CHGNet, SevenNet-0, MACE-MP-0, and ORB v2 reproduce the official YAML
  metrics exactly across both audited subsets, including integer confusion counts.
- Layer B: CHGNet, MACE-MP-0, and ORB v2 regenerate on the same deterministic
  500-structure WBM subset and pass the pre-registered smoke criteria.
- Layer C: the audited four-model ranking is statistically solid, but 43/59
  adjacent pairs on the full 60-model leaderboard are separated by less than one
  measured CI width.
- Ground-truth audit: 497/500 WBM subset hull values reproduce to <=0.001
  meV/atom under current pymatgen, while 3 correction-drift structures shift by
  119-217 meV/atom and 2 stability labels flip.
- Upstream impact: stale/missing md5 metadata and download-time checksum
  verification were fixed in merged PR #359.

## Links

- Repo: https://github.com/maruyamakoju/reprolab
- GitHub release: https://github.com/maruyamakoju/reprolab/releases/tag/v0.4-external-handoff
- Current status: https://github.com/maruyamakoju/reprolab/blob/master/reports/current_status.md
- External handoff tracker: https://github.com/maruyamakoju/reprolab/issues/1
- Full report: `reports/paper-001-matbench-discovery-audit.md`
- External packet: `reports/external_release_packet.md`
- Upstream PR: https://github.com/janosh/matbench-discovery/pull/359

## Suggested post

I published the first ReproLab audit: an independent, command-level
reproducibility check of the Matbench Discovery discovery-task leaderboard.

The main result is positive. Published metrics for CHGNet, SevenNet-0, MACE-MP-0,
and ORB v2 reproduce exactly from released prediction files, and three models
regenerate from model execution on a deterministic 500-structure WBM subset.

The audit also found concrete reproducibility gaps: stale/missing checksum
metadata, missing download-time verification, ORB v2 protocol ambiguity,
leaderboard ranks without reported uncertainty, and pymatgen-version-dependent WBM
hull labels. The checksum/provenance fix from the audit has now been merged
upstream in janosh/matbench-discovery#359.

This is the kind of audit I want ReproLab to do: verify public AI-for-science
benchmarks from code, data, and model execution; report positive results when
things work; and turn small reproducibility failures into upstream fixes.
