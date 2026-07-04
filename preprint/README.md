# Preprint — ReproLab Paper-001 technical note

`main.tex` — "An Independent Reproducibility Audit of the Matbench Discovery
Benchmark". v0 draft assembled 2026-07-05 from
`reports/paper-001-matbench-discovery-audit.md` and the Layer C artifacts.

## Build

```
tectonic main.tex
```

Compiles warning-free with Tectonic 0.16.9 (plain `pdflatex` also works; no
BibTeX — references are inline `thebibliography`). Output: `main.pdf` (~7 pages).

## Submission checklist (before arXiv)

- [ ] Confirm author name romanization ("Koju Maruyama") and affiliation line.
- [ ] arXiv account + **endorsement** for cond-mat.mtrl-sci (first submission in
      this archive may require an endorser — the five outreach contacts are
      natural candidates; start this early, it can take days).
      Category: cond-mat.mtrl-sci primary, cross-list cs.LG.
      Fallback if endorsement stalls: Zenodo DOI, then arXiv later.
- [ ] Decide license (arXiv default non-exclusive license is fine; CC-BY if
      preferred).
- [ ] Re-verify the four upstream link targets still resolve (PR #359,
      issues #357/#358, release v0.4-external-handoff).
- [ ] Optional for v1: one figure (leaderboard adjacent-pair ΔF1 vs. bootstrap
      CI width) from the Layer C data; not required for v0.
- [ ] Consider sending the draft to the matbench-discovery maintainers for
      comment before submission (courtesy + accuracy check on the PR/issue
      framing).

## Facts the text asserts (source of truth)

All numbers trace to `reports/paper-001-matbench-discovery-audit.md`
(assembled 2026-07-03) and the Layer C sections therein; upstream outcomes
(PR #359 merged 2026-07-04) per `reports/outreach_tracker.md`.
