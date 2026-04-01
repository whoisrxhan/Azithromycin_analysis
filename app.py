"""Serve a minimal UI for the fixed azithromycin analysis script."""
from __future__ import annotations

from flask import Flask, render_template

from analysis_runner import run_analysis

app = Flask(__name__)


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
