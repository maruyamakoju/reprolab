# Next execution plan

Date: 2026-07-04

## Priority order

1. Paper-001 external validation
   - Use `reports/paper-001_release_note.md` as the public summary.
   - Use `reports/paper-001_external_email.md` for direct outreach.
   - Lead with the upstream-merged #359 outcome.
   - Track remaining handoff work in
     https://github.com/maruyamakoju/reprolab/issues/1

2. Paper-003 upstream contact
   - Done: added `reports/paper-003_rocauc_issue_137_comment.md` to existing
     upstream issue #137:
     https://github.com/materialsproject/matbench/issues/137#issuecomment-4882357351
   - Keep `reports/paper-003_gn_oa_mape_issue_body.md` as a separate follow-up.
   - Do not open a duplicate `rocauc` issue; #137 already captures the code-level
     concern. The audit contribution is artifact-level evidence and impact size.

3. Paper-002 supporting outreach
   - Use `reports/paper-002-external_release_packet.md` only after Paper-001 has
     been shared, as supporting evidence that the audit template generalizes.
   - Keep the JARVIS framing positive: 101/101 checked artifacts reproduce.

## Suggested same-day sequence

1. Send Paper-001 email to the five tracked external contacts.
2. Done: comment on Matbench issue #137 with the classification `rocauc` audit
   evidence.
3. Wait for any first response before posting the GN-OA MAPE issue.
4. If there is no response after 24-48h, post the GN-OA MAPE issue as a separate,
   narrow follow-up.

## Guardrails

- Do not claim full model regeneration for any paper.
- Do not imply Matbench Discovery, JARVIS, or Matbench broadly failed.
- Keep positive artifact-reproducibility results first.
- Treat uncertainty and metric-semantics findings as interpretation/provenance
  issues unless maintainers confirm otherwise.
