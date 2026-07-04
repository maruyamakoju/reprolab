# Current status

Date: 2026-07-05 (updated 00:xx JST)

## Public state

- Repo: https://github.com/maruyamakoju/reprolab
- Latest pushed commit: see `git log -1 --oneline`
- Paper-001 release: https://github.com/maruyamakoju/reprolab/releases/tag/v0.4-external-handoff
- External handoff tracker: https://github.com/maruyamakoju/reprolab/issues/1
- Matbench Discovery upstream fix: https://github.com/janosh/matbench-discovery/pull/359
- Matbench v0.1 ROC-AUC evidence comment:
  https://github.com/materialsproject/matbench/issues/137#issuecomment-4882357351

## Main message

ReproLab has a flagship result: Paper-001 independently reproduced the audited
Matbench Discovery paths and produced an upstream-merged fix. Paper-002 and
Paper-003 now serve as supporting evidence that the audit template generalizes:
metric recomputation first, bounded execution-path replay where feasible, then
uncertainty/provenance checks.

## What is done

- Paper-001 Matbench Discovery audit packaged and released.
- Upstream PR #359 merged, closing the stale/missing checksum and WBM provenance
  loop.
- Paper-002 JARVIS audit packaged as supporting material.
- Paper-003 Matbench audit packaged; classification ROC-AUC evidence added to
  existing upstream issue #137.

## Waiting

- Matbench issue #137 maintainer response.
- External feedback from the five tracked contacts.
- ReproLab tracking issue #1 checklist completion.
- GN-OA MAPE follow-up quiet-period window:
  earliest 2026-07-05 23:13 JST, preferred 2026-07-06 23:13 JST.

## Next action

**Do NOT send another email round now.** The five tracked contacts were already
emailed on Fri 2026-07-03 (see `outreach_tracker.md` rows 1–5). Sending the new
Paper-001 templates now would be a second contact within 48h with no reply to
the first. Instead:

1. **Public post** (`reports/public_post_draft.md`) — the one outward action
   that duplicates nothing. Post 2026-07-05.
2. **Preprint v0 is drafted**: `preprint/main.tex` (compiles warning-free,
   ~7 pages). Main work line 07-05→07-08: review text, confirm author line,
   start arXiv endorsement process. See `preprint/README.md` checklist.
3. **Email follow-up**: Tue 07-07 / Wed 07-08 JST, short 2–3 line update
   leading with "the fix was merged upstream (#359)" — news, not a nag. Use
   `paper-001_external_email.md` content trimmed to follow-up length.
4. GN-OA MAPE issue: unchanged rule — after a #137 response, or quiet period
   (earliest 2026-07-05 23:13 JST, preferred 2026-07-06 23:13 JST).

Use `reports/response_playbook.md` when maintainers respond. Check GitHub
responses every 2–3 days (next: 2026-07-06), not daily — Fri-evening emails +
weekend silence carry no signal.
