# Current status

Date: 2026-07-04

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

## Next action

Send Paper-001-centered outreach using `reports/paper-001_external_email.md` or
the recipient-specific variants in `reports/paper-001_recipient_outreach.md`.

Do not post the GN-OA MAPE issue immediately. Keep it as a separate follow-up
after either a maintainer response on #137 or a 24-48h quiet period.
