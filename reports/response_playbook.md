# Response playbook

Date: 2026-07-04

## Matbench issue #137

Comment posted:
https://github.com/materialsproject/matbench/issues/137#issuecomment-4882357351

Posted at approximately 2026-07-04 14:13 UTC / 2026-07-04 23:13 JST.

## If maintainers confirm the ROC-AUC behavior

Reply briefly:

> Thanks for confirming. I will keep the audit wording scoped to historical
> Matbench v0.1 classification artifacts and describe `rocauc` as thresholded-label
> AUC / balanced accuracy for the affected float-prediction submissions.

Then update:

- `reports/paper-003-external_release_packet.md`
- `papers/matbench/summary.md`
- `reports/paper-003-matbench-audit.md` via `python scripts/make_matbench_report.py`

## If maintainers say the behavior is intended

Reply briefly:

> Understood. I will frame this as an interpretation/documentation finding rather
> than a scoring bug, and note that Matbench v0.1 historical classification
> `rocauc` should not be read as probability-score ROC-AUC for the affected
> submissions.

Then keep the current audit conclusion, but soften "appears to be computed after"
to "historically behaves as".

## If maintainers point to a different code path

Reply briefly:

> Thanks, I will check that path against the released artifacts and update the
> audit notes if it explains the stored values.

Then rerun only the classification probes before changing conclusions.

## If maintainers ask for a PR

Do not immediately edit scoring behavior without clarifying historical handling.
Ask whether they prefer:

1. docs-only note for Matbench v0.1 historical artifacts,
2. code fix for future submissions,
3. both.

## GN-OA MAPE follow-up timing

Do not post immediately after the ROC-AUC comment.

- Earliest quiet-period follow-up: 2026-07-05 23:13 JST
- Preferred quiet-period follow-up: 2026-07-06 23:13 JST

Use `reports/paper-003_gn_oa_mape_issue_body.md` as a separate issue. Keep it
narrow: one submission, one task, one metric.
