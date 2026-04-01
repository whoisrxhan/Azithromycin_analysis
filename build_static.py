#!/usr/bin/env python3
"""Generate public/index.html + public/analysis.json from test.py (run with RDKit locally/CI)."""
from __future__ import annotations

import html
import json
import shutil
from pathlib import Path

from analysis_runner import run_analysis

ROOT = Path(__file__).resolve().parent
PUBLIC = ROOT / "public"
TEMPLATE = ROOT / "templates" / "static_site.html"
IMAGE_SRC = ROOT / "static" / "azithromycin.png"


def main() -> None:
    output, exit_code = run_analysis()
    escaped = html.escape(output, quote=False)

    tpl = TEMPLATE.read_text(encoding="utf-8")
    if exit_code == 0:
        foot = (
            '<p class="badge ok">Run completed successfully '
            f"(build exit code {exit_code})</p>"
        )
    else:
        foot = f'<p class="badge err">Exit code {exit_code}</p>'

    html_out = (
        tpl.replace("@@ANALYSIS_OUTPUT@@", escaped)
        .replace("@@PANEL_FOOT@@", foot)
    )

    PUBLIC.mkdir(parents=True, exist_ok=True)
    (PUBLIC / "index.html").write_text(html_out, encoding="utf-8")

    (PUBLIC / "analysis.json").write_text(
        json.dumps(
            {
                "exitCode": exit_code,
                "text": output,
            },
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )

    if IMAGE_SRC.is_file():
        shutil.copy(IMAGE_SRC, PUBLIC / "azithromycin.png")
    else:
        raise FileNotFoundError(
            f"Missing {IMAGE_SRC}; add the structure image to static/ before building."
        )

    print(f"Wrote {PUBLIC / 'index.html'} and analysis.json (exit_code={exit_code})")


if __name__ == "__main__":
    main()
