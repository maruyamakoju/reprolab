# Next execution plan

Date: 2026-07-04

## Priority order

1. Paper-001 external validation
   - Use `reports/paper-001_release_note.md` as the public summary.
   - Use `reports/paper-001_external_email.md` for direct outreach.
   - Lead with the upstream-merged #359 outcome.

2. Paper-003 upstream contact
   - Post/share `reports/paper-003_rocauc_issue_body.md` first.
   - Keep `reports/paper-003_gn_oa_mape_issue_body.md` as a separate follow-up.
   - Do not bundle the two issues; the first is metric semantics, the second is a
     narrow stored-score exception.

3. Paper-002 supporting outreach
   - Use `reports/paper-002-external_release_packet.md` only after Paper-001 has
     been shared, as supporting evidence that the audit template generalizes.
   - Keep the JARVIS framing positive: 101/101 checked artifacts reproduce.

## Suggested same-day sequence

1. Send Paper-001 email to the five tracked external contacts.
2. Post the Matbench classification `rocauc` issue.
3. Wait for any first response before posting the GN-OA MAPE issue.
4. If there is no response after 24-48h, post the GN-OA MAPE issue as a separate,
   narrow follow-up.

## Guardrails

- Do not claim full model regeneration for any paper.
- Do not imply Matbench Discovery, JARVIS, or Matbench broadly failed.
- Keep positive artifact-reproducibility results first.
- Treat uncertainty and metric-semantics findings as interpretation/provenance
  issues unless maintainers confirm otherwise.
