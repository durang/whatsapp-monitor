#!/usr/bin/env python3
"""
Render ~/whatsapp-status.md → ~/whatsapp-dashboard.pdf with the v5.7 visual style.

Pipeline:
  1. Read ~/whatsapp-status.md (markdown)
  2. Convert to HTML via python-markdown (with fenced_code, tables, sane_lists)
  3. Wrap in HTML template with dark+orange CSS that mimics v5.7
  4. Render to PDF with weasyprint
  5. Output ~/whatsapp-dashboard.pdf (overwrites — single canonical name)

CLI:
  python3 render-dashboard.py [INPUT_MD] [OUTPUT_PDF]

Defaults:
  INPUT_MD  = ~/whatsapp-status.md
  OUTPUT_PDF= ~/whatsapp-dashboard.pdf
"""
from __future__ import annotations
import sys
from datetime import datetime, timezone
from pathlib import Path

import markdown  # type: ignore
from weasyprint import HTML, CSS  # type: ignore

HOME = Path.home()
DEFAULT_IN = HOME / "whatsapp-status.md"
DEFAULT_OUT = HOME / "whatsapp-dashboard.pdf"

CSS_TEXT = r"""
@page {
    size: A4;
    margin: 18mm 14mm 22mm 14mm;
    background: #0b0e17;
    @bottom-center {
        content: "WhatsApp Dual-Agent Dashboard — Página " counter(page) " de " counter(pages);
        color: #6b7a99;
        font-family: 'Helvetica', sans-serif;
        font-size: 9pt;
    }
}
body {
    background: #0b0e17;
    color: #d6deec;
    font-family: 'Helvetica', sans-serif;
    font-size: 10pt;
    line-height: 1.45;
}
/* Title block (the big orange box at top of doc, derived from H1) */
h1:first-of-type {
    color: #ff7a3d;
    font-size: 26pt;
    font-weight: 800;
    text-align: center;
    border: 2px solid #ff7a3d;
    border-radius: 14px;
    padding: 22px 16px 18px 16px;
    margin: 0 0 22px 0;
    background: #0b0e17;
    letter-spacing: 0.5px;
}
h2 {
    color: #4ea1f3;
    font-size: 15pt;
    font-weight: 700;
    border-bottom: 2px solid #ff7a3d;
    padding-bottom: 4px;
    margin-top: 22px;
    margin-bottom: 10px;
    page-break-after: avoid;
}
h3 {
    color: #87b6ff;
    font-size: 12pt;
    font-weight: 700;
    margin-top: 14px;
    margin-bottom: 6px;
    page-break-after: avoid;
}
h4 {
    color: #d6deec;
    font-size: 10.5pt;
    font-weight: 700;
    margin-top: 10px;
    margin-bottom: 4px;
}
p { margin: 6px 0; }
strong { color: #ffd9c2; }
em { color: #b8c5dc; }
ul, ol { margin: 4px 0 8px 22px; }
li { margin: 2px 0; }
a { color: #4ea1f3; text-decoration: none; }
hr { border: 0; border-top: 1px solid #2a3145; margin: 14px 0; }
/* Code blocks (the box-drawing dashboards live here — must keep monospace + spacing) */
pre {
    background: #0e1424;
    border: 1px solid #2a3145;
    border-radius: 8px;
    padding: 12px 14px;
    font-family: 'DejaVu Sans Mono', 'Menlo', monospace;
    font-size: 8.4pt;
    line-height: 1.30;
    color: #b8d8ff;
    white-space: pre;
    overflow-wrap: normal;
    page-break-inside: avoid;
}
code {
    font-family: 'DejaVu Sans Mono', 'Menlo', monospace;
    font-size: 9pt;
    color: #ffd9c2;
    background: #161c2e;
    padding: 1px 5px;
    border-radius: 3px;
}
pre code { background: transparent; padding: 0; color: inherit; font-size: inherit; }
/* Tables */
table {
    border-collapse: collapse;
    width: 100%;
    margin: 8px 0 12px 0;
    font-size: 9.4pt;
    page-break-inside: avoid;
}
th {
    background: #1a2238;
    color: #ff9466;
    text-align: left;
    padding: 6px 8px;
    border-bottom: 2px solid #ff7a3d;
}
td {
    padding: 5px 8px;
    border-bottom: 1px solid #2a3145;
    color: #d6deec;
    vertical-align: top;
}
tr:nth-child(even) td { background: #11172a; }
/* "Diff-like" prompt blocks rendered as fenced ```diff — keep ASCII art readable */
pre.language-diff, pre.diff { color: #6affc7; }
blockquote {
    border-left: 3px solid #ff7a3d;
    padding-left: 10px;
    color: #b8c5dc;
    margin: 8px 0;
}
/* Footer label injected by Python */
.dashboard-footer {
    margin-top: 24px;
    padding-top: 10px;
    border-top: 1px solid #2a3145;
    color: #6b7a99;
    font-size: 8.5pt;
    text-align: center;
}
"""


def render(md_path: Path, pdf_path: Path) -> None:
    md_text = md_path.read_text(encoding="utf-8")
    html_body = markdown.markdown(
        md_text,
        extensions=["fenced_code", "tables", "sane_lists", "attr_list"],
    )
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    full_html = f"""<!DOCTYPE html><html lang="es"><head>
<meta charset="utf-8"><title>WhatsApp Dual-Agent Dashboard</title>
</head><body>
{html_body}
<div class="dashboard-footer">Generado {now} · ~/whatsapp-monitor/bin/render-dashboard.py · weasyprint</div>
</body></html>"""
    HTML(string=full_html, base_url=str(md_path.parent)).write_pdf(
        target=str(pdf_path),
        stylesheets=[CSS(string=CSS_TEXT)],
    )
    print(f"OK {pdf_path} ({pdf_path.stat().st_size:,} bytes)")


def main(argv: list[str]) -> int:
    md_path = Path(argv[1]).expanduser() if len(argv) > 1 else DEFAULT_IN
    pdf_path = Path(argv[2]).expanduser() if len(argv) > 2 else DEFAULT_OUT
    if not md_path.is_file():
        print(f"ERROR: input not found: {md_path}", file=sys.stderr)
        return 1
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    render(md_path, pdf_path)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
