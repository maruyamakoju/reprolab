"""Layer B: score regenerated CHGNet predictions through the Layer A metric path.

Converts relaxed total energies to e_form_per_atom exactly as upstream
`models/chgnet/join_chgnet_preds.py` does (elemental-reference subtraction via the
clone's bundled `2023-02-07-mp-elemental-reference-entries.json.gz` — the same data
`matbench_discovery.energy` loads; replicated here to avoid that module's import-time
DataFiles side effects), then reuses `compare_metrics.py` functions (build_each_pred,
independent_metrics, try_upstream_metrics) unchanged. No metric logic is forked.

Usage:
    python scripts/layer_b_score.py \
        --preds experiments/layer-b/chgnet/presmoke-run1.jsonl.gz \
                experiments/layer-b/chgnet/presmoke-run2.jsonl.gz \
        --out papers/matbench-discovery/metric_check-layer-b-chgnet-presmoke.md
"""

from __future__ import annotations

import argparse
import gzip
import json
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import compare_metrics as cm  # noqa: E402  (Layer A logic, reused not forked)

REF_ENTRIES = "data/mp/2023-02-07-mp-elemental-reference-entries.json.gz"
PUBLISHED = "models/chgnet/chgnet-0.3.0/2023-12-21-wbm-IS2RE.csv.gz"
PUB_COL = "e_form_per_atom_chgnet"
REGEN_COL = "e_form_per_atom_chgnet_regen"


def load_ref_energies(repo: Path) -> dict[str, float]:
    """Element -> eV/atom of the lowest-energy elemental phase (MP refs, bundled)."""
    from pymatgen.entries.computed_entries import ComputedEntry
    series = pd.read_json(repo / REF_ENTRIES, typ="series")
    return {elem: ComputedEntry.from_dict(d).energy_per_atom
            for elem, d in series.items()}


def e_form_per_atom(energy: float, formula: str, refs: dict[str, float]) -> float:
    """(E_total - sum n_el * ref_el) / n_atoms — matches energy.calc_energy_from_e_refs."""
    from pymatgen.core import Composition
    comp = Composition(formula)
    e_ref = sum(refs[str(el)] * amt for el, amt in comp.items())
    return (energy - e_ref) / comp.num_atoms


def read_relax(path: Path) -> pd.DataFrame:
    with gzip.open(path, "rt", encoding="utf-8") as fh:
        df = pd.DataFrame([json.loads(line) for line in fh])
    return df.set_index("material_id")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default="vendor/matbench-discovery")
    ap.add_argument("--preds", nargs="+", required=True,
                    help="relax output(s); first is scored, second bounds run variance")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    repo = (ROOT / args.repo).resolve()
    sys.path.insert(0, str(repo))  # clone-first imports, as in compare_metrics.main

    runs = [read_relax(ROOT / p) for p in args.preds]
    df_run = runs[0]
    ids = df_run.index.tolist()

    gt = cm.load_ground_truth(repo)
    refs = load_ref_energies(repo)
    formulas = gt.loc[ids, "formula"]

    df_run[REGEN_COL] = [
        e_form_per_atom(row.chgnet_energy, formulas[mat_id], refs)
        for mat_id, row in df_run.iterrows()
    ]

    pub = pd.read_csv(repo / PUBLISHED).set_index("material_id")[PUB_COL]

    # each_pred via the SAME Layer A path for both prediction sets
    gt_sub = gt.loc[ids]
    frames = {}
    for label, col, series in (("regenerated", REGEN_COL, df_run[REGEN_COL]),
                               ("published", PUB_COL, pub.loc[ids])):
        preds_df = series.rename(col).reset_index()
        frames[label] = cm.build_each_pred(gt_sub, preds_df, col)

    # per-structure comparison
    d_meV = (df_run[REGEN_COL] - pub.loc[ids]) * 1e3
    cls = {label: (frames[label]["each_pred"] <= cm.STABILITY_THRESHOLD)
           for label in frames}
    agree = (cls["regenerated"] == cls["published"])

    abs_d = d_meV.abs()
    table_ids = ids if len(ids) <= 30 else abs_d.nlargest(15).index.tolist()
    table_title = ("Per-structure: regenerated vs published e_form (eV/atom)"
                   if len(ids) <= 30
                   else "Worst 15 structures by |Δ| (full data in experiments/)")
    lines = [
        "# Metric Check — Layer B: CHGNet regenerated predictions "
        f"(n={len(ids)})\n",
        "Vertical slice: model relaxation -> prediction CSV -> Layer A metric path. "
        "Generation protocol per upstream `test_chgnet_discovery.py` "
        "(FIRE, steps<=500, fmax=0.05, relax_cell, FrechetCellFilter). "
        "Scored with `compare_metrics.py` functions unchanged.\n",
        f"published preds: `{PUBLISHED}` | regenerated: `{args.preds[0]}`\n",
        f"\n## {table_title}\n",
        "| material_id | formula | n_sites | steps | conv | published | regenerated "
        "| Δ meV/atom | stable(pub) | stable(regen) | agree |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for mat_id in table_ids:
        r = df_run.loc[mat_id]
        lines.append(
            f"| {mat_id} | {formulas[mat_id].replace(' ', '')} | {r.n_sites:.0f} "
            f"| {r.n_steps:.0f} | {'y' if r.converged else 'N'} "
            f"| {pub.loc[mat_id]:.4f} | {r[REGEN_COL]:.4f} | {d_meV[mat_id]:+.1f} "
            f"| {'S' if cls['published'][mat_id] else 'U'} "
            f"| {'S' if cls['regenerated'][mat_id] else 'U'} "
            f"| {'✓' if agree[mat_id] else '✗'} |"
        )

    flips_su = int((cls["published"] & ~cls["regenerated"]).sum())
    flips_us = int((~cls["published"] & cls["regenerated"]).sum())
    stats_header = "\n## Agreement stats (pre-registered thresholds: " \
        "median |Δ|<=10 meV/atom, classification agreement >=95%)\n"
    lines += [
        stats_header,
        f"- n scored = {len(ids)}",
        f"- median |Δ| = **{abs_d.median():.2f} meV/atom** (threshold: <=10)",
        f"- mean |Δ| = {abs_d.mean():.2f} | p95 |Δ| = {abs_d.quantile(0.95):.2f} "
        f"| max |Δ| = {abs_d.max():.2f} meV/atom",
        f"- within 10 meV/atom: {(abs_d <= 10).mean():.1%}",
        f"- classification agreement: **{agree.mean():.1%}** (threshold: >=95%)",
        f"- flips stable->unstable (pub->regen): {flips_su} "
        f"| unstable->stable: {flips_us}",
    ]

    if len(runs) > 1:
        e1, e2 = runs[0]["chgnet_energy"], runs[1]["chgnet_energy"]
        dv = ((e1 - e2) / runs[0]["n_sites"]).abs() * 1e3
        lines += [
            f"- run1-vs-run2 |ΔE|/atom: median {dv.median():.3f} / max {dv.max():.3f} "
            "meV/atom (GPU run-to-run variance bound)",
        ]

    lines.append("\n## Discovery metrics on this subset via the Layer A path "
                 f"(n={len(ids)} — subset-level, not leaderboard-comparable)\n")
    lines.append("| metric | regenerated (indep) | regenerated (upstream_fn) "
                 "| published (indep) | published (upstream_fn) |")
    lines.append("|---|---|---|---|---|")
    results = {}
    for label, frame in frames.items():
        results[label] = dict(
            indep=cm.independent_metrics(frame[cm.EACH_TRUE], frame["each_pred"]),
            upstream=cm.try_upstream_metrics(frame[cm.EACH_TRUE], frame["each_pred"]),
        )
    for metric in ("F1", "Precision", "Recall", "Accuracy", "MAE", "RMSE",
                   "TP", "FP", "TN", "FN"):
        row = [
            cm.fmt(results[label][kind].get(metric)) if results[label][kind] else "—"
            for label in ("regenerated", "published") for kind in ("indep", "upstream")
        ]
        lines.append(f"| {metric} | " + " | ".join(row) + " |")

    out = ROOT / args.out
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines[lines.index(stats_header):]))
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
