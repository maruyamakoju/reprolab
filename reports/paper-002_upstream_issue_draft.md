# Paper-002 JARVIS Upstream Issue Draft

Status: draft only; not posted.
Target repo: https://github.com/usnistgov/jarvis_leaderboard
Short packet: `reports/paper-002-external_release_packet.md`
Full report: `reports/paper-002-jarvis-leaderboard-audit.md`

## Suggested title

Independent artifact audit: 101/101 checked submissions reproduce; adjacent-rank
bootstrap note

## Body

Hi JARVIS-Leaderboard maintainers,

I ran an independent ReproLab audit of public JARVIS-Leaderboard artifacts and
wanted to share the result for maintainer review.

The main artifact-integrity result is positive:

- 14 JARVIS-Leaderboard AI pages checked across regression, classification, and
  spectra tasks.
- 101/101 checked submissions reproduce the official MAE/ACC/MULTIMAE values from
  the public submission CSV zips and benchmark JSON zips, within displayed rounding.
- Every checked submission CSV id set exactly matches the corresponding JSON `test`
  split.

The main interpretation note is about adjacent ranks, not metric correctness:

- Across the 14 checked pages, 29/87 adjacent official point gaps are <=0.005 and
  38/87 are <=0.010 in metric units.
- For the 20 closest adjacent pairs, a paired nonparametric bootstrap over the
  fixed public test rows gives 17/20 95% CIs crossing zero.
- Closest example: on dft_3d formation energy, `kgcnn_coNGN` over `potnet` has
  official MAE gap 0.0002, paired advantage 0.00016852, 95% CI
  [-0.00160975, 0.00156560], P(tie/reversal)=0.4030.

I also ran a bounded Layer B execution-path smoke in an isolated JARVIS environment:

- `matminer_rf`-style CPU path on a deterministic 2048 train / 512 test dft_3d
  formation-energy slice.
- 273 Matminer feature columns, 0 all-NaN feature rows, 100-tree RF.
- Subset MAE 0.24470625.

Important scope notes:

- I am not claiming a full JARVIS model-regeneration audit.
- The bounded `matminer_rf` smoke is not a claim to reproduce the official
  `matminer_rf` leaderboard MAE.
- The bootstrap is not retraining uncertainty and does not sample alternate splits;
  it resamples fixed public test rows only.
- I am not claiming the leaderboard point estimates are wrong. The main Layer A
  result is that the checked point estimates are recoverable from public artifacts.

Evidence:

- Short packet:
  https://github.com/maruyamakoju/reprolab/blob/master/reports/paper-002-external_release_packet.md
- Full report:
  https://github.com/maruyamakoju/reprolab/blob/master/reports/paper-002-jarvis-leaderboard-audit.md
- Layer A metric reports:
  https://github.com/maruyamakoju/reprolab/tree/master/papers/jarvis-leaderboard

Two small packaging notes surfaced:

1. Some classification contribution archives are named `test-acc.csv.zip`, but the
   single CSV inside is named `test-mae.csv`. The current upstream code reads the
   zip directly and is unaffected; this only matters for independent tooling that
   assumes the internal filename matches the outer archive.
2. The public contribution run scripts are useful but heterogeneous: for example,
   `matminer_rf` and `matminer_xgboost` are hardcoded to `snumat`,
   `matminer_xgboost` defaults to `gpu_hist`, and CFID scripts assume a different
   benchmark path convention. I treated this as a documentation/protocol caveat,
   not as a failure.

The feedback I would appreciate:

- Is the Layer A recomputation path consistent with how you expect external users
  to validate leaderboard submissions?
- Is the fixed-test-row bootstrap interpretation fair, or should it be narrowed
  further?
- Would you prefer this as a docs note, a discussion item, or no upstream issue at
  all?

Thanks for maintaining the benchmark.

## Posting checklist

- Confirm the repo's preferred venue: issue vs discussion.
- Link directly to the current commit if a frozen URL is preferred.
- Keep the title positive: artifact reproducibility first, adjacent-rank note
  second.
- Do not post until the user explicitly asks to send or approves a recipient.
