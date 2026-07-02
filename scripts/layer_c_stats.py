"""Layer C: statistical audit of the Matbench Discovery leaderboard itself.

Layers A/B verified that the published numbers are *correctly computed* and
*regenerable*. Layer C asks whether they are *statistically meaningful*:

  Q1  How wide are the confidence intervals on the leaderboard's F1/MAE, and are
      the model rankings statistically significant? (The model YAMLs report no
      uncertainty at all.)
  Q2  How sensitive are F1 and the ranking to the 0 eV/atom stability threshold —
      an analysis choice — within a band comparable to DFT hull uncertainty?
  Q3  Are the models' errors independent? All four are trained on MPtrj-derived
      data; correlated errors mean "several models agree" carries less evidence
      than it appears, and joint blind spots bound what any ensemble can fix.

Design notes (deliberate choices):
- Paired bootstrap: every replicate resamples *structures*, not per-model rows, so
  pairwise metric deltas are estimated on the same resample. For classification
  metrics this is done exactly and cheaply by observing that each structure falls
  into one of 32 joint categories (true stable/unstable x 4 binary predictions);
  a bootstrap replicate is then a single multinomial draw over the 32 category
  counts. MAE uses chunked index resampling on the common non-NaN rows.
- No metric logic is forked: each_pred columns come from compare_metrics.build_each_pred
  (identical rounding, 5 eV outlier filter, NaN->unstable convention as Layer A).
- These analyses are *exploratory* (designed after seeing Layer A/B results),
  unlike the pre-registered Layer B thresholds. Stated as such in the report.

Usage:
    python scripts/layer_c_stats.py --n-boot 2000 \
        --out papers/matbench-discovery/layer_c_statistical_audit.md
"""

from __future__ import annotations

import argparse
import itertools
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
import compare_metrics as cm  # noqa: E402  (Layer A logic, reused not forked)

MODELS = ["chgnet-0.3.0", "sevennet-0", "mace-mp-0", "orb-v2"]
NEAR_HULL_BAND = 0.05  # eV/atom, |each_true| band that decides classification
TAUS_MEV = [-100, -75, -50, -40, -30, -20, -10, -5, 0, 5, 10, 20, 30, 40, 50, 75, 100]


def load_matrix(repo: Path) -> tuple[pd.Series, pd.DataFrame, list[str]]:
    """each_true (uniq protos) + aligned each_pred matrix for all models."""
    gt = cm.load_ground_truth(repo)
    preds, labels = {}, []
    each_true = None
    for key in MODELS:
        ydata, disc = cm.load_model_yaml(repo, key)
        label = ydata.get("model_name", key)
        labels.append(label)
        df = cm.build_each_pred(gt, pd.read_csv(cm.ensure_preds(repo, disc)),
                                disc["pred_col"])
        sub = df[df[cm.UNIQ_PROTO]]
        preds[label] = sub["each_pred"]
        each_true = sub[cm.EACH_TRUE]  # identical across models (same gt + rounding)
    return each_true, pd.DataFrame(preds), labels


def f1_from_counts(tp: np.ndarray, fp: np.ndarray, fn: np.ndarray) -> np.ndarray:
    return 2 * tp / (2 * tp + fp + fn)


def paired_bootstrap_f1(true_stable: np.ndarray, pred_stable: np.ndarray,
                        n_boot: int, rng: np.random.Generator) -> np.ndarray:
    """Exact paired bootstrap of F1 via multinomial over 32 joint categories.

    Returns array (n_boot, n_models) of F1 replicates. Category id encodes the
    shared true label (bit 4) and each model's binary prediction (bits 0..3), so
    one multinomial draw per replicate preserves the pairing across models.
    """
    n, n_models = pred_stable.shape
    cat = true_stable.astype(np.int64) << n_models
    for m in range(n_models):
        cat |= pred_stable[:, m].astype(np.int64) << m
    n_cats = 1 << (n_models + 1)
    counts = np.bincount(cat, minlength=n_cats)

    cat_ids = np.arange(n_cats)
    cat_true = (cat_ids >> n_models) & 1
    reps = rng.multinomial(n, counts / n, size=n_boot)  # (n_boot, 32)

    f1s = np.empty((n_boot, n_models))
    for m in range(n_models):
        cat_pred = (cat_ids >> m) & 1
        tp = reps[:, (cat_true == 1) & (cat_pred == 1)].sum(axis=1)
        fp = reps[:, (cat_true == 0) & (cat_pred == 1)].sum(axis=1)
        fn = reps[:, (cat_true == 1) & (cat_pred == 0)].sum(axis=1)
        f1s[:, m] = f1_from_counts(tp, fp, fn)
    return f1s


def bootstrap_mae(errs: np.ndarray, n_boot: int, rng: np.random.Generator,
                  chunk: int = 100) -> np.ndarray:
    """Paired bootstrap of MAE: resample common rows, same indices for all models."""
    n = errs.shape[0]
    out = np.empty((n_boot, errs.shape[1]), dtype=np.float64)
    for start in range(0, n_boot, chunk):
        b = min(chunk, n_boot - start)
        idx = rng.integers(0, n, size=(b, n), dtype=np.int64)
        out[start:start + b] = errs[idx].mean(axis=1)
    return out


def ci(x: np.ndarray, level: float = 0.95) -> tuple[float, float]:
    lo, hi = np.quantile(x, [(1 - level) / 2, 1 - (1 - level) / 2], axis=0)
    return lo, hi


def scan_leaderboard_f1(repo: Path) -> list[tuple[str, float]]:
    """(model_name, uniq_protos F1) for every model YAML in the clone, sorted desc."""
    import yaml
    rows = []
    for path in repo.glob("models/**/*.yml"):
        try:
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
            f1 = data["metrics"]["discovery"]["unique_prototypes"]["F1"]
            rows.append((data.get("model_name", path.stem), float(f1)))
        except (KeyError, TypeError, ValueError, yaml.YAMLError):
            continue  # aux YAMLs without discovery metrics
    return sorted(rows, key=lambda r: -r[1])


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default="vendor/matbench-discovery")
    ap.add_argument("--n-boot", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--out", default="papers/matbench-discovery/layer_c_statistical_audit.md")
    args = ap.parse_args()

    repo = (ROOT / args.repo).resolve()
    rng = np.random.default_rng(args.seed)
    each_true, P, labels = load_matrix(repo)
    n = len(each_true)
    n_models = len(labels)

    true_stable = (each_true <= cm.STABILITY_THRESHOLD).to_numpy()
    pred_stable = np.column_stack(
        [(P[m] <= cm.STABILITY_THRESHOLD).fillna(False).to_numpy() for m in labels])

    # ---------- Q1: bootstrap CIs + ranking significance ----------
    f1_reps = paired_bootstrap_f1(true_stable, pred_stable, args.n_boot, rng)
    f1_point = np.array([
        f1_from_counts(*(np.array([(true_stable & pred_stable[:, m]).sum()]),
                         np.array([(~true_stable & pred_stable[:, m]).sum()]),
                         np.array([(true_stable & ~pred_stable[:, m]).sum()])))[0]
        for m in range(n_models)])
    f1_lo, f1_hi = ci(f1_reps)

    common = P.notna().all(axis=1)
    errs = np.abs(P[common].to_numpy() - each_true[common].to_numpy()[:, None])
    errs = errs.astype(np.float64)
    mae_reps = bootstrap_mae(errs, args.n_boot, rng)
    mae_point = errs.mean(axis=0)
    mae_lo, mae_hi = ci(mae_reps)

    pair_rows = []
    order = np.argsort(-f1_point)  # leaderboard order, best first
    for a, b in itertools.combinations(order, 2):
        d = f1_reps[:, a] - f1_reps[:, b]
        dlo, dhi = ci(d)
        pair_rows.append((labels[a], labels[b], f1_point[a] - f1_point[b],
                          dlo, dhi, float((d <= 0).mean())))

    # ---------- Q2: stability-threshold sweep ----------
    sweep = []
    et = each_true.to_numpy()
    for tau_mev in TAUS_MEV:
        tau = tau_mev / 1000
        ts = et <= tau
        f1s = []
        for m in labels:
            ps = (P[m] <= tau).fillna(False).to_numpy()
            tp = (ts & ps).sum(); fp = (~ts & ps).sum(); fn = (ts & ~ps).sum()
            f1s.append(2 * tp / (2 * tp + fp + fn))
        sweep.append((tau_mev, f1s, tuple(np.argsort(-np.array(f1s)))))
    base_rank = sweep[TAUS_MEV.index(0)][2]
    flips = [(t, r) for t, _, r in sweep if r != base_rank]

    # ---------- Q3: error correlation + joint blind spots ----------
    signed = P[common].to_numpy() - each_true[common].to_numpy()[:, None]
    pearson = np.corrcoef(signed, rowvar=False)
    spearman = pd.DataFrame(signed, columns=labels).corr(method="spearman").to_numpy()

    wrong = pred_stable != true_stable[:, None]  # misclassified, NaN->unstable kept
    stable_pool = true_stable
    fn_each = (~pred_stable[stable_pool]).mean(axis=0)          # P(FN_m | stable)
    fn_all = (~pred_stable[stable_pool]).all(axis=1).mean()     # P(all FN | stable)
    fn_indep = float(np.prod(fn_each))
    near = np.abs(et) <= NEAR_HULL_BAND
    wrong_near = wrong[near]
    near_each = wrong_near.mean(axis=0)
    near_all = wrong_near.all(axis=1).mean()
    near_indep = float(np.prod(near_each))
    tp_mat = pred_stable & true_stable[:, None]
    uniq_tp = [int((tp_mat[:, m] & ~np.delete(tp_mat, m, axis=1).any(axis=1)).sum())
               for m in range(n_models)]
    n_stable = int(stable_pool.sum())

    # ---------- report ----------
    fmt = lambda v: f"{v:.4f}"  # noqa: E731
    L = []
    L.append("# Layer C — Statistical audit of the Matbench Discovery leaderboard\n")
    L.append(f"Subset: `unique_prototypes` (n={n:,}); models: {', '.join(labels)}; "
             f"paired bootstrap B={args.n_boot}, seed={args.seed}; each_pred built by "
             "the exact Layer A path (`compare_metrics.build_each_pred`). "
             "**Exploratory analysis** (not pre-registered, unlike Layer B).\n")

    L.append("\n## Q1 — Uncertainty and ranking significance (not reported upstream)\n")
    L.append("| model | F1 | 95% CI | CI width | MAE eV/atom | 95% CI |")
    L.append("|---|---|---|---|---|---|")
    for m in order:
        L.append(f"| {labels[m]} | {fmt(f1_point[m])} | [{fmt(f1_lo[m])}, {fmt(f1_hi[m])}] "
                 f"| {f1_hi[m] - f1_lo[m]:.4f} | {mae_point[m]:.4f} "
                 f"| [{mae_lo[m]:.4f}, {mae_hi[m]:.4f}] |")
    L.append("\n| pair (better vs worse) | ΔF1 | 95% CI | P(flip) |")
    L.append("|---|---|---|---|")
    for la, lb, d, dlo, dhi, pflip in pair_rows:
        L.append(f"| {la} vs {lb} | {d:+.4f} | [{dlo:+.4f}, {dhi:+.4f}] | {pflip:.4g} |")

    # leaderboard-resolution context: how tight are the gaps on the FULL roster?
    board = scan_leaderboard_f1(repo)
    max_ci_w = float((f1_hi - f1_lo).max())
    close = [(a, b, fa - fb) for (a, fa), (b, fb) in itertools.pairwise(board)
             if fa - fb < max_ci_w]
    L.append(f"\nContext — leaderboard resolution: the widest 95% CI measured here is "
             f"{max_ci_w:.4f} F1. On the full leaderboard at this commit "
             f"({len(board)} models with a uniq-protos F1), "
             f"**{len(close)} of {len(board) - 1} adjacent pairs are separated by less "
             "than that CI width**, i.e. their published order is unlikely to be "
             "statistically resolvable without a paired significance test:")
    for a, b, gap in close:
        L.append(f"  - {a} vs {b}: ΔF1 = {gap:.3f}")
    L.append("\n(Caveat: CI width varies by model; a definitive statement needs the "
             "paired bootstrap on each pair's prediction files, as done above for four "
             "models. The point stands that the leaderboard reports no uncertainty at "
             "all while many gaps are of this order.)")

    L.append("\n## Q2 — Sensitivity to the 0 eV/atom stability threshold\n")
    L.append("Same threshold applied to truth and predictions (leaderboard convention "
             f"in `stable_metrics`). DFT hull energies themselves carry O(10 meV/atom) "
             "uncertainty, so ranking stability inside this band matters.\n")
    L.append("| τ (meV/atom) | " + " | ".join(labels[m] for m in order) + " | ranking |")
    L.append("|---|" + "---|" * (n_models + 1))
    for tau_mev, f1s, rank in sweep:
        rank_str = " > ".join(labels[i] for i in rank)
        L.append(f"| {tau_mev:+d} | " + " | ".join(fmt(f1s[m]) for m in order)
                 + f" | {rank_str} |")
    if flips:
        L.append(f"\nRanking differs from the τ=0 ordering at "
                 f"{len(flips)}/{len(TAUS_MEV) - 1} swept thresholds: "
                 + "; ".join(f"τ={t:+d}: " + " > ".join(labels[i] for i in r)
                             for t, r in flips))
    else:
        L.append("\nThe τ=0 ranking is unchanged at every swept threshold "
                 f"in [{TAUS_MEV[0]:+d}, {TAUS_MEV[-1]:+d}] meV/atom.")

    L.append("\n## Q3 — Error correlation and joint blind spots\n")
    L.append(f"Signed formation-energy errors (e_form_pred − e_form_dft), common "
             f"non-NaN rows (n={int(common.sum()):,}).\n")
    L.append("| Pearson | " + " | ".join(labels) + " |")
    L.append("|---|" + "---|" * n_models)
    for i, li in enumerate(labels):
        L.append(f"| {li} | " + " | ".join(f"{pearson[i, j]:.3f}"
                                           for j in range(n_models)) + " |")
    L.append("\n| Spearman | " + " | ".join(labels) + " |")
    L.append("|---|" + "---|" * n_models)
    for i, li in enumerate(labels):
        L.append(f"| {li} | " + " | ".join(f"{spearman[i, j]:.3f}"
                                           for j in range(n_models)) + " |")
    L.append(f"\n- Among the {n_stable:,} DFT-stable structures, "
             f"**{fn_all:.2%}** are missed (FN) by *all four* models simultaneously; "
             f"under error independence this would be {fn_indep:.2%} "
             f"(joint-miss lift **{fn_all / fn_indep:,.0f}x**). Per-model miss rates: "
             + ", ".join(f"{labels[m]} {fn_each[m]:.1%}" for m in range(n_models)) + ".")
    L.append(f"- In the near-hull band |E_hull| ≤ {NEAR_HULL_BAND * 1000:.0f} meV/atom "
             f"(n={int(near.sum()):,}), all four models misclassify the same structure "
             f"{near_all:.2%} of the time vs {near_indep:.2%} under independence "
             f"(lift {near_all / near_indep:,.0f}x).")
    L.append("- Unique true positives (stable materials found by that model and missed "
             "by the other three): "
             + ", ".join(f"{labels[m]} {uniq_tp[m]:,}" for m in range(n_models)) + ".")

    L.append("\n## Limitations\n")
    L.append("- Bootstrap treats WBM as an i.i.d. sample; WBM structures are generated "
             "by element substitution from shared seeds, so effective sample size is "
             "somewhat smaller than n — CIs here are, if anything, slightly narrow.")
    L.append("- Threshold sweep reuses the same data at every τ (no multiple-comparison "
             "correction); it is a sensitivity analysis, not a hypothesis test.")
    L.append("- Analyses are exploratory and were designed after Layers A/B; they should "
             "be treated as descriptive audit findings, not confirmatory statistics.")

    out = ROOT / args.out
    out.write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
