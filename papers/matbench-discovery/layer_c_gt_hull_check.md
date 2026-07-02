# Layer C (ground truth) — e_above_hull recomputed from the MP phase diagram

Subset: the committed Layer B ids (n=500); CSE source `data/wbm/2022-10-19-wbm-computed-structure-entries.jsonl.gz`; hull source `data/mp/2023-02-07-ppd-mp.pkl.gz` (2023 pickle) unpickled under pymatgen 2026.5.18. Corrections: entries shipped with adjustments for 0/500; MP2020 applied by us to the rest; 0 dropped by compatibility processing; 0 hull lookups failed.

## Result

- compared: **500/500** subset structures
- median |Δ| = **0.0003 meV/atom** | p95 = 0.0005 | max = 216.5996 meV/atom
- within 0.1 meV/atom: 99.4% | within 1 meV/atom: 99.4%
- stable/unstable label (<=0) agreement with published column: 99.6%

| material_id | published | recomputed | Δ meV/atom |
|---|---|---|---|
| wbm-2-28782 | 0.024147 | 0.240747 | +216.5996 |
| wbm-4-28450 | -0.028060 | 0.098273 | +126.3330 |
| wbm-4-15908 | 0.032848 | -0.086485 | -119.3332 |
| wbm-1-57937 | 0.024024 | 0.024024 | +0.0005 |
| wbm-3-53078 | -0.120219 | -0.120219 | -0.0005 |
| wbm-1-57885 | 0.191865 | 0.191865 | -0.0005 |
| wbm-4-12603 | 0.041207 | 0.041207 | -0.0005 |
| wbm-1-1604 | 0.368311 | 0.368311 | -0.0005 |
| wbm-1-37417 | 0.666768 | 0.666768 | +0.0005 |
| wbm-3-4711 | 0.204088 | 0.204088 | -0.0005 |

## Diagnosis of the 3 outliers (`layer_c_gt_diagnose.py`, logged in run_log)

For all three, the e_above_hull delta equals the **e_form delta to <0.001 meV/atom**
(+216.601, +126.307, −119.303), so the phase-diagram lookup is not implicated — the
entire discrepancy is in the **MP2020 energy-correction assignment**, and all three
are cases where that assignment hinges on pymatgen's oxidation-state guessing:

| id | formula | our correction | interpretation |
|---|---|---|---|
| wbm-2-28782 | SrBrN3 | Br anion only (−1.068 eV) | upstream value implies an additional/different anion (nitride) correction |
| wbm-4-28450 | PaIO | oxide (−1.374 eV) after explicit pymatgen warning "Failed to guess oxidation states… assigning anion correction to only the most electronegative atom" | heuristic fallback, version-dependent |
| wbm-4-15908 | NdH4Pt | hydride H (−1.432 eV) | upstream value implies no hydride correction was applied |

## Control experiment: pymatgen 2023.5.10 reproduces all three (run_log)

Rerunning the identical diagnosis in a clean venv with **pymatgen 2023.5.10** (the
version upstream's own `data-files.yml` `_links` reference) reproduces the published
values for all three outliers:

| id | formula | Δ under pymatgen 2026.5 | Δ under 2023.5.10 | corrections 2023.5.10 | corrections 2026.5 |
|---|---|---|---|---|---|
| wbm-2-28782 | SrBrN3 | +216.601 | **+0.001** | Br **and** N | Br only |
| wbm-4-28450 | PaIO | +126.307 | **−0.027** | oxide **and** I | oxide only (guess-failure fallback) |
| wbm-4-15908 | NdH4Pt | −119.303 | **+0.031** | **none** | hydride H |

(Δ in meV/atom vs the published `e_form_per_atom_mp2020_corrected`.)

**Finding (demonstrated bidirectionally):** the benchmark's ground-truth column
embeds MP2020 anion-correction assignment decisions (oxidation-state guessing) that
changed between pymatgen 2023.5.10 and 2026.5. The 2023 version reproduces the
published column exactly (500/500 within 0.031 meV/atom); the 2026 version diverges
by 119–217 meV/atom on 3/500 structures (0.6%) and flips 2/500 stability labels.
Which correction assignment is chemically preferable is out of scope for this audit —
the reproducibility point is that the ground truth depends on unstated library-version
behavior. 497/500 values reproduce to ≤0.001 meV/atom under either version, and the
2023 `PatchedPhaseDiagram` pickle unpickles cleanly under pymatgen 2026. At
leaderboard scale, ~0.4–0.6% label ambiguity is material when adjacent models are
separated by ΔF1 of 0.001–0.003 (see the statistical audit).
