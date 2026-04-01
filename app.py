"""Serve a minimal UI for the fixed azithromycin analysis script."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

from flask import Flask, render_template

ROOT = Path(__file__).resolve().parent

app = Flask(__name__)


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


@app.route("/")
def index():
    output, code = run_analysis()
    return render_template(
        "index.html",
        analysis_output=output,
        exit_code=code,
    )


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
