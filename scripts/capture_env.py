"""Snapshot the runtime environment for reproducibility.

Writes a timestamped JSON to logs/ and refreshes papers/matbench-discovery/environment.md.
Stdlib only, so it runs under any Python (system or venv).

Usage:
    python scripts/capture_env.py
"""

from __future__ import annotations

import json
import platform
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LOGS = ROOT / "logs"
ENV_MD = ROOT / "papers" / "matbench-discovery" / "environment.md"


def _run(cmd: list[str]) -> str:
    exe = shutil.which(cmd[0])
    if exe is None:
        return f"(not found: {cmd[0]})"
    try:
        out = subprocess.run(
            cmd, capture_output=True, text=True, timeout=120, check=False
        )
        return (out.stdout + out.stderr).strip()
    except Exception as exc:  # noqa: BLE001
        return f"(error running {' '.join(cmd)}: {exc!r})"


def collect() -> dict:
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    info: dict = {
        "timestamp_utc": now,
        "platform": platform.platform(),
        "python_version": sys.version.replace("\n", " "),
        "python_executable": sys.executable,
        "nvidia_smi": _run(
            ["nvidia-smi", "--query-gpu=name,memory.total,driver_version",
             "--format=csv,noheader"]
        ),
        "git_vendor_commit": _run(
            ["git", "-C", str(ROOT / "vendor" / "matbench-discovery"),
             "rev-parse", "HEAD"]
        ),
        "pip_freeze": _run([sys.executable, "-m", "pip", "freeze"]),
    }
    return info


def to_markdown(info: dict) -> str:
    frozen = info.pop("pip_freeze", "")
    lines = ["# Environment\n", f"_Captured: {info['timestamp_utc']}_\n"]
    for key, val in info.items():
        lines.append(f"- **{key}**: `{val}`")
    lines.append("\n## pip freeze\n\n```\n" + frozen + "\n```\n")
    return "\n".join(lines)


def main() -> None:
    LOGS.mkdir(exist_ok=True)
    info = collect()
    stamp = datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")
    json_path = LOGS / f"env-{stamp}.json"
    json_path.write_text(json.dumps(info, indent=2), encoding="utf-8")
    ENV_MD.parent.mkdir(parents=True, exist_ok=True)
    ENV_MD.write_text(to_markdown(dict(info)), encoding="utf-8")
    print(f"wrote {json_path}")
    print(f"wrote {ENV_MD}")


if __name__ == "__main__":
    main()
