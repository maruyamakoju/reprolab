"""Independent reproduction of Matbench Discovery *discovery-task* metrics.

For a given model it:
  1. loads the WBM ground truth (bundled in the clone),
  2. loads the model's published prediction CSV (downloading from Figshare if absent),
  3. derives energy-above-hull predictions exactly as the upstream pipeline does,
  4. recomputes F1/Precision/Recall/Accuracy/MAE/RMSE/R2 TWO ways:
        (a) upstream `matbench_discovery.metrics.discovery.stable_metrics` (if importable)
        (b) an independent re-implementation in this file,
  5. reads the OFFICIAL values committed in the model YAML,
  6. writes a diff table (markdown) and prints it.

This does NOT overwrite any upstream file. Layer A of the audit — CPU only.

Usage:
    python scripts/compare_metrics.py --repo vendor/matbench-discovery \
        --model chgnet-0.3.0 --subsets unique_prototypes full_test_set \
        --out papers/matbench-discovery/metric_check.md
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
import requests
import yaml

STABILITY_THRESHOLD = 0.0
MAX_ERROR_THRESHOLD = 5.0  # eV/atom
EACH_TRUE = "e_above_hull_mp2020_corrected_ppd_mp"
E_FORM_DFT = "e_form_per_atom_mp2020_corrected"
UNIQ_PROTO = "unique_prototype"
ID_COL = "material_id"


def independent_metrics(each_true: pd.Series, each_pred: pd.Series) -> dict:
    """Re-implement stable_metrics from scratch to cross-check the upstream function."""
    et = pd.to_numeric(each_true, errors="coerce")
    ep = pd.to_numeric(each_pred, errors="coerce")
    # NaN predictions count as "predicted unstable" (fillna=True upstream)
    pred_stable = (ep <= STABILITY_THRESHOLD).fillna(False)
    true_stable = et <= STABILITY_THRESHOLD
    true_unstable = et > STABILITY_THRESHOLD

    tp = int((true_stable & pred_stable).sum())
    fp = int((true_unstable & pred_stable).sum())
    fn = int((true_stable & ~pred_stable).sum())
    tn = int((true_unstable & ~pred_stable).sum())

    precision = tp / (tp + fp) if (tp + fp) else float("nan")
    recall = tp / (tp + fn) if (tp + fn) else float("nan")
    f1 = (2 * precision * recall / (precision + recall)
          if precision + recall else float("nan"))
    accuracy = (tp + tn) / (tp + fp + tn + fn)

    mask = et.notna() & ep.notna()
    et_r, ep_r = et[mask].to_numpy(), ep[mask].to_numpy()
    mae = abs(et_r - ep_r).mean()
    rmse = ((et_r - ep_r) ** 2).mean() ** 0.5
    ss_res = ((et_r - ep_r) ** 2).sum()
    ss_tot = ((et_r - et_r.mean()) ** 2).sum()
    r2 = 1 - ss_res / ss_tot if ss_tot else float("nan")

    return dict(F1=f1, Precision=precision, Recall=recall, Accuracy=accuracy,
                MAE=mae, RMSE=rmse, R2=r2, TP=tp, FP=fp, TN=tn, FN=fn)


def load_ground_truth(repo: Path) -> pd.DataFrame:
    path = repo / "data" / "wbm" / "2023-12-13-wbm-summary.csv.gz"
    df = pd.read_csv(path)
    df.index = df[ID_COL]
    return df


def load_model_yaml(repo: Path, model_key: str) -> tuple[dict, dict]:
    """Return (full yaml dict, discovery metrics dict) for a model key."""
    matches = list(repo.glob(f"models/**/{model_key}.yml"))
    if not matches:
        raise FileNotFoundError(f"no YAML for {model_key} under {repo}/models")
    data = yaml.safe_load(matches[0].read_text(encoding="utf-8"))
    return data, data.get("metrics", {}).get("discovery", {})


def _figshare_download_url(url: str) -> str:
    """Rewrite a Figshare landing URL to the API download endpoint (avoids the WAF
    that returns an empty/HTML body). Mirrors matbench_discovery.remote.fetch."""
    if "figshare.com" in url and "/files/" in url:
        file_id = url.rsplit("/files/", maxsplit=1)[-1].split("?", maxsplit=1)[0]
        return f"https://api.figshare.com/v2/file/download/{file_id}"
    return url


def ensure_preds(repo: Path, disc: dict) -> Path:
    rel = disc["pred_file"]
    url = disc.get("pred_file_url")
    path = repo / rel
    if path.is_file() and path.stat().st_size > 0:
        return path
    if not url:
        raise FileNotFoundError(f"{path} missing and no pred_file_url to download")
    dl_url = _figshare_download_url(url)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.parent / (path.name + ".part")
    print(f"downloading predictions: {dl_url} -> {path}")
    resp = requests.get(dl_url, timeout=600, stream=True,
                        headers={"User-Agent": "reprolab-audit"})
    resp.raise_for_status()
    with tmp.open("wb") as fh:
        for chunk in resp.iter_content(chunk_size=8192):
            fh.write(chunk)
    # fail loudly if we got HTML/empty instead of a gzip stream
    with tmp.open("rb") as fh:
        magic = fh.read(2)
    if magic != b"\x1f\x8b":
        size = tmp.stat().st_size
        tmp.unlink(missing_ok=True)
        raise RuntimeError(
            f"download from {dl_url} is not gzip (magic={magic!r}, {size} bytes)"
        )
    tmp.replace(path)
    return path


def build_each_pred(gt: pd.DataFrame, preds: pd.DataFrame, pred_col: str) -> pd.DataFrame:
    df = gt[[EACH_TRUE, E_FORM_DFT, UNIQ_PROTO]].copy()
    df["e_form_pred"] = preds.set_index(ID_COL)[pred_col]
    # upstream filter: unrealistic preds -> NaN (data.py:291-305)
    bad = (df["e_form_pred"] - df[E_FORM_DFT]).abs() > MAX_ERROR_THRESHOLD
    df.loc[bad, "e_form_pred"] = pd.NA
    n_bad = int(bad.sum())
    # upstream rounds the merged frame to 3 decimals (preds/discovery.py:28)
    for col in (EACH_TRUE, E_FORM_DFT, "e_form_pred"):
        df[col] = pd.to_numeric(df[col], errors="coerce").round(3)
    # fixed DFT hull => each_pred = each_true + e_form_pred - e_form_dft
    df["each_pred"] = df[EACH_TRUE] + df["e_form_pred"] - df[E_FORM_DFT]
    df.attrs["n_filtered"] = n_bad
    df.attrs["missing_preds"] = int(df["e_form_pred"].isna().sum())
    return df


def subset_rows(df: pd.DataFrame, subset: str) -> pd.DataFrame:
    if subset == "full_test_set":
        return df
    if subset == "unique_prototypes":
        return df[df[UNIQ_PROTO]]
    raise ValueError(f"subset {subset!r} not implemented (see reproduction_plan.md §6)")


def try_upstream_metrics(each_true, each_pred) -> dict | None:
    """Import the audited repo's own stable_metrics (clone is put first on sys.path
    in main()). Handles both the repo layout (metrics/discovery.py) and the older
    flat PyPI-wheel layout (metrics.py)."""
    stable_metrics = None
    for mod in ("matbench_discovery.metrics.discovery", "matbench_discovery.metrics"):
        try:
            stable_metrics = __import__(mod, fromlist=["stable_metrics"]).stable_metrics
            break
        except Exception:  # noqa: BLE001, S112
            continue
    if stable_metrics is None:
        print("(upstream stable_metrics unavailable; using independent recompute only)")
        return None
    return stable_metrics(each_true, each_pred, stability_threshold=STABILITY_THRESHOLD)


def fmt(val: object) -> str:
    if isinstance(val, float):
        return f"{val:.3f}"
    return str(val)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default="vendor/matbench-discovery")
    ap.add_argument("--model", default="chgnet-0.3.0")
    ap.add_argument("--subsets", nargs="+",
                    default=["unique_prototypes", "full_test_set"])
    ap.add_argument("--out", default="papers/matbench-discovery/metric_check.md")
    ap.add_argument("--download-only", action="store_true",
                    help="download+validate the prediction CSV, then exit (no compute)")
    args = ap.parse_args()

    repo = Path(args.repo).resolve()
    # Audit the CLONED repo's code (leaderboard source), not the PyPI wheel, which
    # ships a different module layout under the same version string. pip only provides
    # dependencies. Putting the clone first on sys.path makes `import matbench_discovery`
    # resolve to the pinned commit.
    import sys
    sys.path.insert(0, str(repo))
    ydata, disc = load_model_yaml(repo, args.model)

    # --download-only: fetch + validate the prediction CSV, then stop. Keeps the network
    # download in a separate process from the heavy numpy/pandas compute (see the
    # transient 0xC0000005 crash on the combined path in failure_notes.md).
    if args.download_only:
        path = ensure_preds(repo, disc)
        print(f"downloaded {args.model}: {path} ({path.stat().st_size / 1e6:.2f} MB)")
        return

    pred_col = disc["pred_col"]
    pred_path = ensure_preds(repo, disc)  # already cached if pre-downloaded
    gt = load_ground_truth(repo)
    preds = pd.read_csv(pred_path)
    df = build_each_pred(gt, preds, pred_col)

    report_metrics = ("F1", "Precision", "Recall", "Accuracy", "MAE", "RMSE", "R2",
                      "TP", "FP", "TN", "FN")
    lines = [f"# Metric Check — {ydata.get('model_name', args.model)}\n",
             f"repo commit: `{args.repo}` | pred_col: `{pred_col}` | "
             f"filtered(|Δ|>5): {df.attrs['n_filtered']} | "
             f"missing_preds: {df.attrs['missing_preds']}\n"]

    for subset in args.subsets:
        rows = subset_rows(df, subset)
        official = disc.get(subset, {})
        repro = independent_metrics(rows[EACH_TRUE], rows["each_pred"])
        upstream = try_upstream_metrics(rows[EACH_TRUE], rows["each_pred"])

        lines.append(f"\n## {subset}  (n={len(rows):,})\n")
        lines.append("| metric | official | reproduced | upstream_fn | Δ(off−repro) | pass |")
        lines.append("|---|---|---|---|---|---|")
        for m in report_metrics:
            off = official.get(m)
            rep = repro.get(m)
            ups = upstream.get(m) if upstream else None
            if isinstance(off, (int, float)) and isinstance(rep, (int, float)):
                delta = off - rep
                tol = 0.0011 if m not in ("TP", "FP", "TN", "FN") else 0.5
                ok = "✓" if abs(delta) <= tol else "✗"
                d = fmt(delta)
            else:
                d, ok = "—", "?"
            lines.append(
                f"| {m} | {fmt(off)} | {fmt(rep)} | {fmt(ups)} | {d} | {ok} |"
            )

    out = Path(args.out)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    print(f"\nwrote {out}")


if __name__ == "__main__":
    main()
