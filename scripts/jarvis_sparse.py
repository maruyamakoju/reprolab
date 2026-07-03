"""Sparse-checkout helper for JARVIS-Leaderboard benchmark artifacts.

Given one or more benchmark names, add the docs page, ground-truth JSON zip, all
matching contribution CSV zips, and their metadata files to the vendor checkout.
"""

from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

from jarvis_score import parse_benchmark_name


def git_lines(vendor: Path, *args: str) -> list[str]:
    out = subprocess.check_output(["git", "-C", str(vendor), *args], text=True)
    return [line.strip() for line in out.splitlines() if line.strip()]


def paths_for_benchmark(vendor: Path, benchmark: str) -> list[str]:
    bench = parse_benchmark_name(benchmark)
    csv_name = f"{benchmark}.csv.zip"
    paths = {
        "README.md",
        "setup.py",
        "jarvis_leaderboard/rebuild.py",
        "jarvis_leaderboard/benchmarks/descriptions.csv",
        f"docs/{bench.category}/{bench.subcategory}/{bench.dataset}_{bench.prop}.md",
        (
            f"jarvis_leaderboard/benchmarks/{bench.category}/{bench.subcategory}/"
            f"{bench.dataset}_{bench.prop}.json.zip"
        ),
    }
    contrib_paths = git_lines(
        vendor, "ls-tree", "-r", "--name-only", "HEAD", "jarvis_leaderboard/contributions"
    )
    for path in contrib_paths:
        if path.endswith(f"/{csv_name}"):
            paths.add(path)
            paths.add(str(Path(path).with_name("metadata.json")).replace("\\", "/"))
    return sorted(paths)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vendor", default="vendor/jarvis_leaderboard")
    parser.add_argument("--benchmarks", nargs="+", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    vendor = Path(args.vendor)
    all_paths: set[str] = set()
    for benchmark in args.benchmarks:
        paths = paths_for_benchmark(vendor, benchmark)
        n_csv = sum(path.endswith(".csv.zip") for path in paths)
        print(f"{benchmark}: {len(paths)} paths ({n_csv} contribution CSVs)")
        all_paths.update(paths)

    paths = sorted(all_paths)
    if args.dry_run:
        print("\n".join(paths))
        return 0

    cmd = ["git", "-C", str(vendor), "sparse-checkout", "add", "--skip-checks", *paths]
    subprocess.run(cmd, check=True)
    print(f"added {len(paths)} sparse-checkout paths")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
