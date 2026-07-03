# Outreach tracker

Purpose: track every external contact for ReproLab so outreach actually closes the
loop (sent → response → next step). Update the row when anything changes.

| Date | Person / org | Channel | Sent | Response | Requested next step |
|---|---|---|---|---|---|
| 2026-07-02 | janosh/matbench-discovery (upstream) | GitHub issue [#357](https://github.com/janosh/matbench-discovery/issues/357) — stale md5 + unverified checksum | yes | pending | maintainer preference: fix md5 / add verification / document API checksum as authoritative (PR offered) |
| 2026-07-02 | janosh/matbench-discovery (upstream) | [Follow-up comment](https://github.com/janosh/matbench-discovery/issues/357#issuecomment-4863387819): registry-wide check → 3 stale + 2 empty md5s; patch branch ready on fork (PR not opened) | yes | pending | maintainer OK → open PR from `fix-wbm-initial-structures-md5`; no response in 24–48h → open PR politely |
| 2026-07-02 | janosh/matbench-discovery (upstream) | GitHub issue [#358](https://github.com/janosh/matbench-discovery/issues/358) — ground truth depends on pymatgen version (MP2020 anion-correction drift, demonstrated bidirectionally with a 2023.5.10 control) | yes | pending | docs/provenance PR offered (3 options) |
| 2026-07-03 | janosh/matbench-discovery (upstream) | PR [#359](https://github.com/janosh/matbench-discovery/pull/359) — fixes 3 stale + 2 missing md5s, adds checksum verification on download; CodeRabbit feedback addressed in follow-up commits (`b50b67b`, `0c753e0`) | yes | pending | review / merge, or trim to metadata-only (option A) |
| 2026-07-03 | janosh/matbench-discovery (upstream) | PR [#360](https://github.com/janosh/matbench-discovery/pull/360) — docs-only WBM ground-truth provenance note for pymatgen MP2020 anion-correction version dependence (follow-up to #358) | yes | pending | review / merge, or reword/move note |
| 2026-07-03 | (1) Matbench Discovery / materials-ML maintainer or contributor | Email | yes | pending | feedback |
| 2026-07-03 | (2) MIT materials-ML / scientific-ML PhD or postdoc | Email | yes | pending | feedback |
| 2026-07-03 | (3) AI-for-science professor or lab | Email | yes | pending | feedback |
| 2026-07-03 | (4) materials-AI startup founder / engineer | Email | yes | pending | feedback |
| 2026-07-03 | (5) VC / technical-diligence AI-science contact | Email | yes | pending | feedback |

Email template: see `one_page_summary.md` (paste-ready) or the short version in the
project notes. Repo link to include: <https://github.com/maruyamakoju/reprolab>
