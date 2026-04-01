"""Run test.py and return console text + exit code (used by Flask and static build)."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def run_analysis() -> tuple[str, int]:
    proc = subprocess.run(
        [sys.executable, str(ROOT / "test.py")],
        cwd=str(ROOT),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    parts = []
    if proc.stdout:
        parts.append(proc.stdout.rstrip())
    if proc.stderr:
        parts.append(proc.stderr.rstrip())
    text = "\n\n".join(parts) if parts else "(no output)"
    if proc.returncode != 0 and (
        "rdkit" in text.lower() or "No module named" in text
    ):
        hint = (
            "\n\n---\n"
            "Hint: install RDKit in this Python environment. "
            "Example: conda env create -f environment.yml, then conda activate compound"
        )
        text = text + hint
    return text, proc.returncode
