# Send checklist

Use this before sending Paper-001 outreach or posting publicly.

## Paper-001 outreach

- [ ] Replace `[Name]` and `[Your name]`.
- [ ] Pick the recipient-specific variant from
      `reports/paper-001_recipient_outreach.md`.
- [ ] Keep the release URL near the top:
      https://github.com/maruyamakoju/reprolab/releases/tag/v0.4-external-handoff
- [ ] Lead with the positive result and upstream-merged fix.
- [ ] Do not lead with Paper-002 or Paper-003; mention them only if asked.
- [ ] After sending, update `reports/outreach_tracker.md` and
      https://github.com/maruyamakoju/reprolab/issues/1.

## Public post

- [ ] Use `reports/public_post_draft.md`.
- [ ] Keep the wording positive: the audit reproduced the checked paths and found
      bounded reproducibility/provenance issues.
- [ ] Include the release URL.
- [ ] Avoid claiming full 257k-structure regeneration.
- [ ] Avoid saying any benchmark broadly failed.

## Matbench follow-up

- [ ] Check materialsproject/matbench#137 before posting anything else.
- [ ] If there is a maintainer response, adapt the GN-OA MAPE wording to that
      response.
- [ ] If quiet for 24-48h, post
      `reports/paper-003_gn_oa_mape_issue_body.md` as a separate issue.
