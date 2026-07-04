# Paper-001 recipient-specific outreach

Base link:
https://github.com/maruyamakoju/reprolab/releases/tag/v0.4-external-handoff

Repo:
https://github.com/maruyamakoju/reprolab

Current status:
https://github.com/maruyamakoju/reprolab/blob/master/reports/current_status.md

## 1. Matbench Discovery / materials-ML maintainer

Subject: Independent Matbench Discovery reproducibility audit

Hi [Name],

I wanted to share the completed ReproLab audit of the Matbench Discovery
discovery-task leaderboard. The main result is positive: the audited released
metrics reproduce exactly for four models, and three model-execution replays pass
on a deterministic 500-structure WBM subset.

The audit also produced a concrete upstream outcome: the stale/missing checksum
metadata and download-time verification fix was merged in
janosh/matbench-discovery#359.

Release:
https://github.com/maruyamakoju/reprolab/releases/tag/v0.4-external-handoff

I would value your read on whether this audit format is useful from a maintainer
perspective: metric recomputation first, bounded model-execution replay second,
then uncertainty/provenance checks.

Best,
[Your name]

## 2. Scientific-ML / materials-ML researcher

Subject: Reproducibility audit of a materials-ML benchmark

Hi [Name],

I wanted to share a concrete ReproLab result. I audited the Matbench Discovery
discovery-task leaderboard from public code, data, prediction files, and bounded
model execution.

The main result is encouraging: audited metrics reproduce exactly for four models,
and three models regenerate on a deterministic 500-structure WBM slice. The audit
also found practical issues around checksum metadata, protocol clarity, leaderboard
uncertainty, and WBM ground-truth provenance. One fix has already been merged
upstream.

Release:
https://github.com/maruyamakoju/reprolab/releases/tag/v0.4-external-handoff

I would appreciate feedback on whether this kind of independent audit would be
useful for papers or benchmarks in your area.

Best,
[Your name]

## 3. AI-for-science professor / lab lead

Subject: Independent AI-for-science benchmark audit

Hi [Name],

I am building ReproLab as a small independent audit workflow for AI-for-science
benchmarks. The first completed audit is Matbench Discovery.

The audit result is mostly positive: published metrics reproduce exactly for four
models, bounded model-execution replays pass for three models, and the main
metadata/provenance finding produced an upstream-merged fix. The broader point is
to make benchmark claims checkable from public artifacts, not only to find errors.

Release:
https://github.com/maruyamakoju/reprolab/releases/tag/v0.4-external-handoff

I would value any feedback on whether this audit structure is rigorous enough to
be useful to benchmark authors, reviewers, or labs relying on these leaderboards.

Best,
[Your name]

## 4. Materials-AI startup founder / engineer

Subject: Practical reproducibility audit of Matbench Discovery

Hi [Name],

I wanted to share a practical benchmark-audit result from ReproLab. I audited the
Matbench Discovery discovery-task leaderboard with a focus on whether a technical
team could independently reproduce the numbers and rerun a bounded slice of the
model-execution path.

The good news is that the audited metrics reproduce exactly and three model
execution replays pass. The useful engineering findings are around data-file
checksums, download verification, protocol ambiguity, and leaderboard uncertainty.
One metadata/download-verification fix has already been merged upstream.

Release:
https://github.com/maruyamakoju/reprolab/releases/tag/v0.4-external-handoff

I would appreciate a quick read on whether this is the kind of diligence artifact
that would be useful before relying on a public AI-for-science benchmark.

Best,
[Your name]

## 5. VC / technical-diligence contact

Subject: Example AI-for-science benchmark diligence artifact

Hi [Name],

I wanted to share a concrete example of the kind of technical-diligence artifact
ReproLab can produce for AI-for-science benchmarks.

The first audit checks Matbench Discovery. It reproduced the audited leaderboard
metrics exactly, regenerated three model-execution slices, quantified leaderboard
uncertainty, and found metadata/provenance issues that led to an upstream-merged
fix.

Release:
https://github.com/maruyamakoju/reprolab/releases/tag/v0.4-external-handoff

The point is not that the benchmark failed; the opposite is mostly true. The value
is that the benchmark's claims became externally checkable, and the audit produced
specific fixes and risk notes.

Best,
[Your name]
