"""Download a data file declared in the clone's matbench_discovery/data-files.yml,
using the Figshare API endpoint (landing URLs are WAF-blocked, see failure_notes.md),
and verify its md5 against the declared value.

Usage:
    python scripts/download_datafile.py --name wbm_initial_structures
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

import requests
import yaml

ROOT = Path(__file__).resolve().parent.parent


def figshare_api_url(url: str) -> str:
    if "figshare.com" in url and "/files/" in url:
        file_id = url.rsplit("/files/", maxsplit=1)[-1].split("?", maxsplit=1)[0]
        return f"https://api.figshare.com/v2/file/download/{file_id}"
    return url


def md5_of(path: Path) -> str:
    h = hashlib.md5()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default="vendor/matbench-discovery")
    ap.add_argument("--name", required=True, help="key in data-files.yml")
    ap.add_argument("--expect-md5", default=None,
                    help="override the (unverified-by-upstream) md5 in data-files.yml; "
                         "e.g. the Figshare API computed_md5 when the YAML value is "
                         "stale (see failure_notes.md)")
    args = ap.parse_args()

    repo = ROOT / args.repo
    registry = yaml.safe_load(
        (repo / "matbench_discovery" / "data-files.yml").read_text(encoding="utf-8")
    )
    entry = registry[args.name]
    dest = repo / "data" / entry["path"]
    want_md5 = args.expect_md5 or entry.get("md5")

    if dest.is_file() and want_md5 and md5_of(dest) == want_md5:
        print(f"already present + md5 OK: {dest} ({dest.stat().st_size / 1e6:.1f} MB)")
        return

    url = figshare_api_url(entry["url"])
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.parent / (dest.name + ".part")
    print(f"downloading {args.name}: {url} -> {dest}")
    resp = requests.get(url, timeout=3600, stream=True,
                        headers={"User-Agent": "reprolab-audit"})
    resp.raise_for_status()
    n = 0
    with tmp.open("wb") as fh:
        for chunk in resp.iter_content(chunk_size=1 << 20):
            fh.write(chunk)
            n += len(chunk)
    print(f"downloaded {n / 1e6:.1f} MB")

    got_md5 = md5_of(tmp)
    if want_md5 and got_md5 != want_md5:
        tmp.unlink(missing_ok=True)
        raise RuntimeError(f"md5 mismatch: got {got_md5}, want {want_md5}")
    tmp.replace(dest)
    print(f"md5 OK ({got_md5}): {dest}")


if __name__ == "__main__":
    main()
