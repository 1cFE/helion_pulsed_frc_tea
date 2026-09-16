"""Render docs/writeup.md and docs/ledger.md to LaTeX and PDF.

Deterministic like make_html.py: fixed pandoc options, no timestamps
(SOURCE_DATE_EPOCH pinned for pdflatex), so two builds of the same source
give byte-identical .tex files. Dollar signs are prose (the writeup
writes $/MWh and M$/kg bare), so the tex_math_dollars extension is off
and pandoc escapes them. Implicit figures are off too: the writeup
carries its own italic caption paragraphs, so the images stay inline
and LaTeX does not add a second "Figure n" label. The SVG figures are
converted to PDF with cairosvg (the PNG copies are the fallback), and
each pipe table's separator row is re-dashed in proportion to its
content so pandoc's longtable gives wide columns to long cells. The
output directory is not tracked.
"""
import math
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "outputs"
FIG_DIR = ROOT / "docs" / "figures"
WRITEUP_MD = ROOT / "docs" / "writeup.md"
LEDGER_MD = ROOT / "docs" / "ledger.md"
TARGETS = ((WRITEUP_MD, "writeup"), (LEDGER_MD, "ledger"))

PANDOC_FROM = "markdown-tex_math_dollars-implicit_figures"
PANDOC_VARS = ("geometry:margin=1in", "fontsize=10pt", "colorlinks=true",
               "documentclass=article")
MAX_CELL_CHARS = 400
LINE_PT = 468.0          # a 6.5 in text line
COLSEP_PT = 2 * 4.0      # the two \tabcolsep gaps around each column
CHAR_PT = 5.0            # a wide-ish character at the tables' \footnotesize
HYPHEN_PIECE = 8         # the longest piece TeX leaves when it hyphenates a word
TABLE_PREAMBLE = (r"\usepackage{etoolbox}"
                  r"\AtBeginEnvironment{longtable}{\footnotesize}"
                  r"\setlength{\tabcolsep}{4pt}")
_SEP_RE = re.compile(r"^\|[-| :]+\|$")


def unbreakable_chars(cell: str) -> int:
    """Length of the longest piece of a cell that LaTeX cannot break:
    tokens split at whitespace, hyphens and underscores (the .tex gets an
    \\allowbreak after each escaped underscore); a piece of letters only
    is hyphenatable and counts at most HYPHEN_PIECE."""
    longest = 1
    for token in cell.split():
        for piece in re.split(r"[-_]", token.strip("`*")):
            n = len(piece)
            if piece.isalpha():
                n = min(n, HYPHEN_PIECE)
            longest = max(longest, n)
    return longest


def column_dashes(rows: list[list[str]]) -> list[int]:
    """Relative column widths for a pipe table's separator row. Each column
    starts at the square root of its longest cell (so paragraph columns
    dominate without swamping the rest), then any column whose longest
    unbreakable piece would not fit its share is fixed at the share that
    piece needs, and the flexible columns split the remainder."""
    ncol = max(len(r) for r in rows)
    usable_pt = LINE_PT - COLSEP_PT * ncol
    flex, need = [], []
    for k in range(ncol):
        cells = [r[k] for r in rows if k < len(r)]
        longest = max((len(c) for c in cells), default=1)
        piece = max((unbreakable_chars(c) for c in cells), default=1)
        flex.append(math.sqrt(max(1, min(longest, MAX_CELL_CHARS))))
        need.append(min(0.9, 1.05 * piece * CHAR_PT / usable_pt))
    share = [f / sum(flex) for f in flex]
    fixed = [False] * ncol
    for _ in range(ncol + 1):
        changed = False
        for k in range(ncol):
            if not fixed[k] and share[k] < need[k]:
                fixed[k], changed = True, True
        if not changed:
            break
        rest = max(0.0, 1.0 - sum(need[k] for k in range(ncol) if fixed[k]))
        flex_sum = sum(flex[k] for k in range(ncol) if not fixed[k]) or 1.0
        share = [need[k] if fixed[k] else rest * flex[k] / flex_sum for k in range(ncol)]
    return [max(3, round(1000 * s)) for s in share]


def _figure_ext(out_dir: Path) -> str:
    try:
        import cairosvg  # noqa: F401
        return "pdf"
    except ImportError:
        return "png"


def prepare_markdown(text: str, figure_ext: str = "pdf") -> tuple[str, str]:
    """(title, body): the leading H1 lifted out as the document title,
    figure links pointed at the converted copies, and every pipe table's
    separator row re-dashed in proportion to the square root of its
    longest cell per column (pandoc reads the dashes as relative widths)."""
    lines = text.split("\n")
    title = ""
    for i, line in enumerate(lines):
        if line.strip():
            if line.startswith("# "):
                title = line[2:].strip()
                lines = lines[i + 1:]
            break
    out = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if (line.startswith("|") and i + 1 < len(lines)
                and _SEP_RE.match(lines[i + 1].strip())):
            j = i + 2
            while j < len(lines) and lines[j].startswith("|"):
                j += 1
            rows = [[c.strip() for c in r.strip().strip("|").split("|")]
                    for r in [lines[i]] + lines[i + 2:j]]
            out.append(lines[i])
            out.append("|" + "|".join("-" * w for w in column_dashes(rows)) + "|")
            out.extend(lines[i + 2:j])
            i = j
            continue
        out.append(re.sub(r"\(figures/([A-Za-z0-9_]+)\.svg\)",
                          rf"(figures/\1.{figure_ext})", line))
        i += 1
    return title, "\n".join(out)


def convert_figures(out_dir: Path) -> list[Path]:
    """Every SVG figure as PDF under out_dir/figures (PNG copied if cairosvg
    is missing), for \\includegraphics."""
    fig_out = Path(out_dir) / "figures"
    fig_out.mkdir(parents=True, exist_ok=True)
    written = []
    for svg in sorted(FIG_DIR.glob("*.svg")):
        try:
            import cairosvg
            target = fig_out / f"{svg.stem}.pdf"
            cairosvg.svg2pdf(url=str(svg), write_to=str(target))
        except ImportError:
            target = fig_out / f"{svg.stem}.png"
            shutil.copyfile(svg.with_suffix(".png"), target)
        written.append(target)
    return written


def build_tex(md_path: Path, out_tex: Path, title: str | None = None) -> Path:
    md_path, out_tex = Path(md_path), Path(out_tex)
    out_tex.parent.mkdir(parents=True, exist_ok=True)
    lifted, body = prepare_markdown(md_path.read_text(encoding="utf-8"),
                                    _figure_ext(out_tex.parent))
    title = title or lifted
    cmd = ["pandoc", "--from", PANDOC_FROM, "--to", "latex", "--standalone",
           "--wrap=none", "--metadata", f"title={title}",
           "--variable", f"header-includes={TABLE_PREAMBLE}"]
    for v in PANDOC_VARS:
        cmd += ["--variable", v]
    tex = subprocess.run(cmd, input=body.encode("utf-8"), check=True,
                         capture_output=True).stdout.decode("utf-8")
    out_tex.write_text(polish_cells(tex), encoding="utf-8")
    return out_tex


def polish_cells(tex: str) -> str:
    """Two break opportunities pandoc's LaTeX does not give a table cell:
    TeX never hyphenates the first word of a paragraph, so a zero-width
    space precedes each cell's text, and an escaped underscore (knob
    names) may break the line after it. Link URLs carry raw underscores
    and are untouched."""
    tex = tex.replace("\\raggedright\n", "\\raggedright\\hspace{0pt}\n")
    return tex.replace("\\_", "\\_\\allowbreak{}")


def compile_pdf(tex_path: Path) -> Path:
    """pdflatex twice (longtable and hyperref need the second pass), with
    the PDF date pinned so the bytes do not carry the build time."""
    tex_path = Path(tex_path)
    env = dict(os.environ, SOURCE_DATE_EPOCH="0", FORCE_SOURCE_DATE="1")
    for _ in range(2):
        proc = subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", tex_path.name],
            cwd=tex_path.parent, env=env, capture_output=True, text=True)
        if proc.returncode != 0:
            log = tex_path.with_suffix(".log")
            tail = log.read_text(encoding="utf-8", errors="replace")[-3000:] if log.exists() else proc.stdout[-3000:]
            raise RuntimeError(f"pdflatex failed on {tex_path.name}:\n{tail}")
    for ext in (".aux", ".out", ".toc"):
        tex_path.with_suffix(ext).unlink(missing_ok=True)
    return tex_path.with_suffix(".pdf")


def build_all(out_dir: Path = OUTPUT_DIR) -> list[Path]:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    convert_figures(out_dir)
    written = []
    for md, stem in TARGETS:
        tex = build_tex(md, out_dir / f"{stem}.tex")
        written += [tex, compile_pdf(tex)]
    return written


if __name__ == "__main__":
    for out in build_all():
        print(f"wrote {out.relative_to(ROOT)} ({out.stat().st_size} bytes)", file=sys.stderr)
