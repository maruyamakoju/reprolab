# External handoff next steps

Paper-001 is now released and has an upstream-merged fix. Paper-003 ROC-AUC
evidence has been added to the existing Matbench issue #137. This issue tracks the
remaining external handoff steps.

## Links

- Paper-001 release: https://github.com/maruyamakoju/reprolab/releases/tag/v0.4-external-handoff
- Matbench Discovery upstream fix: https://github.com/janosh/matbench-discovery/pull/359
- Matbench ROC-AUC evidence comment: https://github.com/materialsproject/matbench/issues/137#issuecomment-4882357351
- Current status: https://github.com/maruyamakoju/reprolab/blob/master/reports/current_status.md

## Checklist

- [x] Publish Paper-001 release and update release body with current-status links.
- [ ] Send Paper-001-centered outreach using `reports/paper-001_recipient_outreach.md`.
- [ ] Monitor materialsproject/matbench#137 for maintainer response.
- [ ] If #137 is quiet for 24-48h, post the GN-OA MAPE follow-up separately using
      `reports/paper-003_gn_oa_mape_issue_body.md`.
      Earliest: 2026-07-05 23:13 JST. Preferred: 2026-07-06 23:13 JST.
- [ ] Use Paper-002 JARVIS as supporting evidence after Paper-001 has been shared.
- [ ] Update `reports/outreach_tracker.md` after each external response.

## Guardrails

- Lead with positive artifact reproducibility.
- Do not claim full model regeneration.
- Do not bundle the GN-OA MAPE issue with the ROC-AUC thread.
- Treat leaderboard uncertainty and metric semantics as interpretation/provenance
  findings unless maintainers confirm otherwise.
