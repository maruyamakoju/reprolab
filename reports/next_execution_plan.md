# Next execution plan

Date: 2026-07-05

## Priority order

1. **Preprint (main work line, 07-05 → 07-08)**
   - v0 draft done: `preprint/main.tex` + `preprint/README.md` checklist.
   - Review text, confirm author/affiliation line, start arXiv endorsement.
   - This satisfies a second stop-loss criterion without waiting on anyone.

2. Paper-001 external validation
   - Emails to the five contacts were **sent 2026-07-03** — do not re-send now.
   - Post `reports/public_post_draft.md` publicly (07-05); duplicates nothing.
   - Follow-up email Tue 07-07 / Wed 07-08 JST, leading with the merged #359.
   - Track remaining handoff work in
     https://github.com/maruyamakoju/reprolab/issues/1

3. Paper-003 upstream contact
   - Done: added `reports/paper-003_rocauc_issue_137_comment.md` to existing
     upstream issue #137:
     https://github.com/materialsproject/matbench/issues/137#issuecomment-4882357351
   - Keep `reports/paper-003_gn_oa_mape_issue_body.md` as a separate follow-up.
   - Do not open a duplicate `rocauc` issue; #137 already captures the code-level
     concern. The audit contribution is artifact-level evidence and impact size.

4. Paper-002 supporting outreach
   - Use `reports/paper-002-external_release_packet.md` only after Paper-001 has
     been shared, as supporting evidence that the audit template generalizes.
   - Keep the JARVIS framing positive: 101/101 checked artifacts reproduce.

## Suggested same-day sequence (2026-07-05)

1. Post `reports/public_post_draft.md` publicly (~30 min).
2. Review `preprint/main.tex`; confirm author line; begin arXiv
   account/endorsement steps per `preprint/README.md`.
3. Do NOT email the five contacts again today (sent 07-03); follow-up with the
   merged-#359 news on 07-07/07-08.
4. GN-OA MAPE issue unchanged: wait for a #137 response or the quiet period.
   - Earliest: 2026-07-05 23:13 JST.
   - Preferred: 2026-07-06 23:13 JST.

## Guardrails

- Do not claim full model regeneration for any paper.
- Do not imply Matbench Discovery, JARVIS, or Matbench broadly failed.
- Keep positive artifact-reproducibility results first.
- Treat uncertainty and metric-semantics findings as interpretation/provenance
  issues unless maintainers confirm otherwise.
- Use `reports/response_playbook.md` for maintainer response handling.
