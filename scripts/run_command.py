"""Run a command, capture stdout/stderr/exit code/timing, and append to run_log.md.

Everything the audit executes should go through this wrapper so the log is complete
and re-runnable. Stdlib only.

Usage:
    python scripts/run_command.py -- <command> [args...]
    python scripts/run_command.py --note "install attempt" -- pip install matbench-discovery
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RUN_LOG = ROOT / "papers" / "matbench-discovery" / "run_log.md"
RAW_LOGS = ROOT / "logs"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--note", default="", help="short label for this command")
    parser.add_argument("cmd", nargs=argparse.REMAINDER,
                        help="command after `--`")
    args = parser.parse_args()

    cmd = args.cmd
    if cmd and cmd[0] == "--":
        cmd = cmd[1:]
    if not cmd:
        print("no command given (use: run_command.py -- <cmd>)", file=sys.stderr)
        return 2

    RAW_LOGS.mkdir(exist_ok=True)
    RUN_LOG.parent.mkdir(parents=True, exist_ok=True)
    started = datetime.now(timezone.utc)
    stamp = started.strftime("%Y%m%d-%H%M%S")
    raw_path = RAW_LOGS / f"cmd-{stamp}.log"

    t0 = time.time()
    proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
    dt = time.time() - t0

    raw_path.write_text(
        f"$ {' '.join(cmd)}\n\n=== STDOUT ===\n{proc.stdout}\n"
        f"=== STDERR ===\n{proc.stderr}\n",
        encoding="utf-8",
    )

    tail = "\n".join((proc.stdout + proc.stderr).splitlines()[-15:])
    entry = (
        f"\n### {started:%Y-%m-%d %H:%M UTC} — {args.note or cmd[0]}\n\n"
        f"```\n$ {' '.join(cmd)}\n```\n\n"
        f"- exit code: **{proc.returncode}**  | duration: {dt:.1f}s  "
        f"| raw log: `logs/{raw_path.name}`\n\n"
        f"output tail:\n```\n{tail}\n```\n"
    )
    with RUN_LOG.open("a", encoding="utf-8") as fh:
        fh.write(entry)

    print(f"exit={proc.returncode} ({dt:.1f}s) -> logged to {RUN_LOG.name}")
    return proc.returncode


if __name__ == "__main__":
    raise SystemExit(main())
