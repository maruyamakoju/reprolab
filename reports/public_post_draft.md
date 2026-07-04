# Public post draft

I published the first ReproLab audit: an independent, command-level
reproducibility check of the Matbench Discovery discovery-task leaderboard.

The main result is positive. Published metrics for CHGNet, SevenNet-0, MACE-MP-0,
and ORB v2 reproduce exactly from released prediction files. Three model-execution
replays also pass on a deterministic 500-structure WBM subset.

The audit surfaced practical reproducibility issues around checksum metadata,
download verification, protocol clarity, leaderboard uncertainty, and WBM
ground-truth provenance. One outcome is already upstream: the checksum/provenance
fix was merged in janosh/matbench-discovery#359.

Release:
https://github.com/maruyamakoju/reprolab/releases/tag/v0.4-external-handoff

This is the kind of work I want ReproLab to do: verify AI-for-science benchmark
claims from public code, data, and model execution; report positive results when
things work; and turn reproducibility gaps into concrete fixes.

## Short version

I published ReproLab's first audit, focused on Matbench Discovery. The audited
leaderboard metrics reproduce exactly for four models, three bounded
model-execution replays pass, and one metadata/download-verification fix was
merged upstream.

Release:
https://github.com/maruyamakoju/reprolab/releases/tag/v0.4-external-handoff
