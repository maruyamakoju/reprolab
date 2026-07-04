# Paper-002 JARVIS Outreach Draft

Status: queued as supporting outreach after Paper-001 external validation.
Repo: https://github.com/maruyamakoju/reprolab
Short packet: `reports/paper-002-external_release_packet.md`
Full report: `reports/paper-002-jarvis-leaderboard-audit.md`

## Suggested recipients

- JARVIS-Leaderboard / NIST maintainer or contributor
- Materials-ML researcher who uses JARVIS or ALIGNN
- Scientific-ML benchmark reviewer interested in leaderboard uncertainty

## Subject options

1. Independent reproducibility audit of JARVIS-Leaderboard public artifacts
2. JARVIS-Leaderboard audit: 101/101 metrics reproduce; adjacent-rank bootstrap note
3. Request for sanity check on a JARVIS-Leaderboard reproducibility audit

## Short email

Hi [Name],

I ran an independent ReproLab audit of JARVIS-Leaderboard and wanted to ask whether
you would be willing to sanity-check the framing before I share it more broadly.

The main result is positive for artifact integrity: across 14 JARVIS-Leaderboard AI
pages, 101/101 checked submissions reproduce the official MAE/ACC/MULTIMAE values
from the public CSV and JSON zip artifacts, with exact test-id agreement.

The main interpretation finding is about adjacent ranks rather than correctness.
Across the checked pages, 29/87 adjacent official point gaps are <=0.005 and 38/87
are <=0.010 in metric units. For the 20 closest adjacent pairs, a paired bootstrap
over the fixed public test rows gives 17/20 95% CIs crossing zero.

I also verified a bounded Layer B execution path in an isolated JARVIS environment:
a `matminer_rf`-style CPU smoke on a deterministic 2048 train / 512 test dft_3d
formation-energy slice completed with 273 Matminer features, 0 all-NaN feature
rows, and subset MAE 0.24470625. This is explicitly not a full leaderboard
regeneration and not a claim to reproduce the official `matminer_rf` MAE.

Short packet:
https://github.com/maruyamakoju/reprolab/blob/master/reports/paper-002-external_release_packet.md

Full report:
https://github.com/maruyamakoju/reprolab/blob/master/reports/paper-002-jarvis-leaderboard-audit.md

The specific feedback I am looking for is:

1. Does the Layer A metric-recomputation framing match how JARVIS-Leaderboard should
   be interpreted?
2. Is the fixed-test-set bootstrap wording fair, or should it be narrowed further?
3. Are there any JARVIS-specific caveats I should add before publicizing this?

Thanks,
[Name]

## Short social / DM version

I ran a ReproLab audit of JARVIS-Leaderboard. Positive artifact result: 101/101
checked submissions across 14 pages reproduce official MAE/ACC/MULTIMAE from public
CSV+JSON zips with exact test-id agreement. Interpretation note: among the 20
closest adjacent pairs, fixed-test-set paired bootstrap gives 17/20 95% CIs crossing
zero. Short packet:
https://github.com/maruyamakoju/reprolab/blob/master/reports/paper-002-external_release_packet.md

## Guardrails

- Do not say JARVIS-Leaderboard is wrong; Layer A is positive.
- Do not say the bootstrap is training or split uncertainty; it is fixed-test-set
  resampling.
- Do not say Layer B regenerated a full leaderboard submission; it is a bounded
  execution-path smoke.
- Lead with artifact reproducibility, then adjacent-rank interpretability.
