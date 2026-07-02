"""Diagnose the Layer C ground-truth outliers: corrections drift vs hull lookup.

For each outlier id: recompute the MP2020-corrected formation energy from the shipped
CSE and compare to the summary's `e_form_per_atom_mp2020_corrected`. If the e_form
delta equals the e_above_hull delta, the discrepancy is entirely in the *correction
assignment* (pymatgen oxidation-state heuristics), not in the phase-diagram lookup.

Usage:
    python scripts/layer_c_gt_diagnose.py --ids wbm-2-28782 wbm-4-28450 wbm-4-15908
"""

from __future__ import annotations

import argparse
import gzip
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import compare_metrics as cm  # noqa: E402
from layer_b_score import load_ref_energies  # noqa: E402

CSE_FILE = "data/wbm/2022-10-19-wbm-computed-structure-entries.jsonl.gz"
E_FORM_COL = "e_form_per_atom_mp2020_corrected"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default="vendor/matbench-discovery")
    ap.add_argument("--ids", nargs="+", required=True)
    args = ap.parse_args()

    from pymatgen.entries.compatibility import MaterialsProject2020Compatibility
    from pymatgen.entries.computed_entries import ComputedStructureEntry

    repo = (ROOT / args.repo).resolve()
    gt = cm.load_ground_truth(repo)
    wanted = set(args.ids)

    found: dict[str, dict] = {}
    with gzip.open(repo / CSE_FILE, "rt", encoding="utf-8") as fh:
        for line in fh:
            rec = json.loads(line)
            if rec.get("material_id") in wanted:
                found[rec["material_id"]] = rec.get("computed_structure_entry") or rec
                if len(found) == len(wanted):
                    break

    refs = load_ref_energies(repo)
    compat = MaterialsProject2020Compatibility()
    for mid in args.ids:
        entry = ComputedStructureEntry.from_dict(found[mid])
        row = gt.loc[mid]
        proc = compat.process_entries([entry], verbose=False, clean=True)[0]
        e_ref = sum(refs[str(el)] * amt for el, amt in entry.composition.items())
        e_form_ours = (proc.energy - e_ref) / entry.composition.num_atoms
        d_meV = (e_form_ours - row[E_FORM_COL]) * 1e3
        print(f"{mid} {entry.composition.reduced_formula:12s}")
        print(f"  e_form summary={row[E_FORM_COL]:+.6f} ours={e_form_ours:+.6f} "
              f"delta={d_meV:+.3f} meV/atom")
        print(f"  our adjustments: "
              f"{[(a.name, round(a.value, 4)) for a in proc.energy_adjustments]}")


if __name__ == "__main__":
    main()
