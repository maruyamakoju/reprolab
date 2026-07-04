# External email draft - Paper-001 centered

Subject: Independent reproducibility audit of Matbench Discovery

Hi [Name],

I wanted to share a concrete result from ReproLab, a small independent
reproducibility-audit project for AI-for-science benchmarks.

The first audit checks the Matbench Discovery discovery-task leaderboard. The
result is mostly positive: published metrics for CHGNet, SevenNet-0, MACE-MP-0,
and ORB v2 reproduce exactly from released prediction files, and three models
regenerate from model execution on a deterministic 500-structure WBM subset.

The audit also surfaced practical reproducibility issues: stale/missing checksum
metadata, missing download-time verification, ORB v2 protocol ambiguity,
leaderboard ranks without uncertainty, and pymatgen-version-dependent WBM hull
labels. One concrete outcome is already upstream: the checksum/provenance fix was
merged in janosh/matbench-discovery#359 on 2026-07-04.

Repo: https://github.com/maruyamakoju/reprolab
Short release note: `reports/paper-001_release_note.md`
Full external packet: `reports/external_release_packet.md`

I would value a sanity check on whether this audit format is useful: metric
recompute first, bounded model-execution replay second, then uncertainty/provenance
checks. I am especially interested in what would make this more useful to
benchmark maintainers or technical reviewers.

Best,
[Your name]

## Optional shorter version

Hi [Name],

I published the first ReproLab audit, focused on Matbench Discovery. The main
result is positive: audited leaderboard metrics reproduce exactly for four models,
and three model-execution replays pass on a deterministic 500-structure WBM slice.
The audit also produced an upstream-merged fix for stale/missing checksum metadata
and download-time verification: janosh/matbench-discovery#359.

Repo: https://github.com/maruyamakoju/reprolab

I would appreciate a quick read on whether this audit format is useful for
AI-for-science benchmark maintainers and reviewers.

Best,
[Your name]
