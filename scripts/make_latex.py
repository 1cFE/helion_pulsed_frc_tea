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
ASCII physics of the markdown (chi, tau, x_s, B^2/2mu0, the indented
equation blocks) is typeset as LaTeX math through the tables in this
file, and leftover_ascii_math is the guard that a new equation gets a
mapping. The output directory is not tracked.
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

PANDOC_FROM = "markdown-tex_math_dollars-implicit_figures+tex_math_single_backslash"
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


_BYLINE_RE = re.compile(r"^\*([^*]+)\*$")

# The markdown writes its physics in ASCII (chi, tau, x_s, B^2/2mu0) so it
# reads on GitHub and in the HTML page; the LaTeX rendering typesets it.
# Display equations are the indented code blocks, matched whole; inline
# formulas are matched longest first with flexible whitespace, then the
# bare symbols. Config knob names (dd_frac, fuel_recovery, f_rep) stay as
# text, as the writeup's Notation paragraph says they do.
DISPLAY_EQUATIONS = {
    "f_T = 1 - (1 - e^-x)/x, x = (sv_DT / sv_DD) x_DD,":
        r"f_T = 1 - \frac{1 - e^{-x}}{x}, \qquad x = \frac{\langle\sigma v\rangle_{DT}}{\langle\sigma v\rangle_{DD}}\, x_{DD},",
    "gain <= chi x burn time / breakeven time,":
        r"\mathrm{gain} \le \chi \, \frac{\text{burn time}}{\text{breakeven time}},",
}
_ETA_DEC = r"\eta_{\mathrm{dec}}"
_F_PDV = r"f_{\mathrm{pdv}}"
_E_DEL = r"E_{\mathrm{del}}"
_SV = r"\langle\sigma v\rangle"
INLINE_FORMULAS = [
    ("gain <= chi x burn time / breakeven time",
     r"\mathrm{gain} \le \chi \times \text{burn time} / \text{breakeven time}"),
    ("chi(x_s) = 1.5 <beta> x_s^2 / (1.5 <beta> x_s^2 + 1 - x_s^2)",
     r"\chi(x_s) = 1.5\langle\beta\rangle x_s^2 / (1.5\langle\beta\rangle x_s^2 + 1 - x_s^2)"),
    ("chi = 1.5 <beta> x_s^2 / (1.5 <beta> x_s^2 + 1 - x_s^2)",
     r"\chi = 1.5\langle\beta\rangle x_s^2 / (1.5\langle\beta\rangle x_s^2 + 1 - x_s^2)"),
    ("x = (sv_DT/sv_DD)(-ln(1 - f_D))",
     rf"x = ({_SV}_{{DT}}/{_SV}_{{DD}})\,(-\ln(1 - f_D))"),
    ("x_DD = -ln(1 - f_D) = n_D <sigma v>_DD tau",
     rf"x_{{DD}} = -\ln(1 - f_D) = n_D {_SV}_{{DD}}\, \tau"),
    ("CAS30 = fraction x CAS20 x (construction_time_yr / 6 yr)",
     r"\mathrm{CAS30} = \mathrm{fraction} \times \mathrm{CAS20} \times (\mathrm{construction\_time\_yr} / 6\,\mathrm{yr})"),
    ("p_dee = eta_dec (p_driver + p_pdv) - p_driver",
     rf"p_{{\mathrm{{dee}}}} = {_ETA_DEC}\,(p_{{\mathrm{{driver}}}} + p_{{\mathrm{{pdv}}}}) - p_{{\mathrm{{driver}}}}"),
    ("eta_dec chi (1 - f_pdv) p_driver",
     rf"{_ETA_DEC}\, \chi\, (1 - {_F_PDV})\, p_{{\mathrm{{driver}}}}"),
    ("eta_dec[(1 - chi) + chi f_pdv]", rf"{_ETA_DEC}[(1 - \chi) + \chi {_F_PDV}]"),
    ("B^2 tau >= 1.4 (2 + 3 T_e/T_i)^2", r"B^2\tau \ge 1.4\,(2 + 3\,T_e/T_i)^2"),
    ("W = (B^2/2mu0) x annulus volume", r"W = (B^2/2\mu_0) \times \text{annulus volume}"),
    ("W = (B^2 / 2 mu0) x annulus volume", r"W = (B^2/2\mu_0) \times \text{annulus volume}"),
    ("0.90 x 0.80 = 0.72 <= 0.80", r"0.90 \times 0.80 = 0.72 \le 0.80"),
    ("0.192 = 0.08 x 6 / 2.5", r"0.192 = 0.08 \times 6 / 2.5"),
    ("f_T = 1 - (1 - e^-x)/x", r"f_T = 1 - (1 - e^{-x})/x"),
    ("(1/2) n_D <sigma v>_DT tau", rf"\tfrac{{1}}{{2}} n_D {_SV}_{{DT}}\, \tau"),
    ("(1 - x_s^2)/(2.5 - x_s^2)", r"(1 - x_s^2)/(2.5 - x_s^2)"),
    ("V_i = E_del/(B^2/2mu0)", rf"V_i = {_E_DEL}/(B^2/2\mu_0)"),
    ("bf / (1 - fr (1 - bf))", r"\mathrm{bf}/(1 - \mathrm{fr}\,(1 - \mathrm{bf}))"),
    ("<beta> = 1 - x_s^2/2", r"\langle\beta\rangle = 1 - x_s^2/2"),
    ("E_del/(B^2/2mu0)", rf"{_E_DEL}/(B^2/2\mu_0)"),
    ("1 - (V_i/V_f)^(2/3)", r"1 - (V_i/V_f)^{2/3}"),
    ("(1 - e^-t/17.8 yr)", r"(1 - e^{-t/17.8\,\mathrm{yr}})"),
    ("n_D <sigma v> tau", rf"n_D {_SV}\, \tau"),
    ("composite <= 0.80", r"\text{composite} \le 0.80"),
    ("chi(1 - f_pdv)", rf"\chi(1 - {_F_PDV})"),
    ("1.5 B^2/2mu0", r"1.5\, B^2/2\mu_0"),
    ("staffing^0.5", r"\mathrm{staffing}^{0.5}"),
    ("T_e = T_i/2", r"T_e = T_i/2"),
    ("gamma = 5/3", r"\gamma = 5/3"),
    ("T_e = T_i", r"T_e = T_i"),
    ("chi E_del", rf"\chi {_E_DEL}"),
    ("1 - gain", r"1 - \mathrm{gain}"),
    ("beta = 1", r"\beta = 1"),
    ("B^(1/5)", r"B^{1/5}"),
    ("L^(1/3)", r"L^{1/3}"),
    ("1.5 pV", r"1.5\,pV"),
    ("P^0.5", r"P^{0.5}"),
    ("n tau", r"n\tau"),
    ("B^2", r"B^2"),
]
UNITS = [
    ("MW yr/m^2", r"\mathrm{MW\,yr/m^2}"), ("M$/m^2", r"\mathrm{M\$/m^2}"),
    ("MJ/m^2", r"\mathrm{MJ/m^2}"), ("MW/m^2", r"\mathrm{MW/m^2}"),
    ("s/m^3", r"\mathrm{s/m^3}"), ("m^-3", r"\mathrm{m^{-3}}"),
    ("m^3", r"\mathrm{m^3}"), ("m^2", r"\mathrm{m^2}"),
]
SYMBOLS = {
    "eta_dec": _ETA_DEC, "eta_pin": r"\eta_{\mathrm{pin}}", "eta_th": r"\eta_{\mathrm{th}}",
    "f_pdv": _F_PDV, "f_rad": r"f_{\mathrm{rad}}", "E_del": _E_DEL,
    "x_DD": r"x_{DD}", "x_s": r"x_s", "f_T": r"f_T", "f_D": r"f_D", "n_D": r"n_D",
    "T_i": r"T_i", "T_e": r"T_e", "V_i": r"V_i", "V_f": r"V_f",
    "chi": r"\chi", "tau": r"\tau", "mu0": r"\mu_0",
}
ARROW = (" -> ", r" \(\to\) ")
LEFTOVER_RE = re.compile(
    r"\^|<=|>=|<beta>|<sigma|\bmu0\b|\bchi\b|\btau\b|\bx_s\b|\beta_(?:dec|pin|th)\b"
    r"|\bf_pdv\b|\bE_del\b|\bx_DD\b|\bgamma = ")


def _pat(ascii_text: str) -> re.Pattern:
    """Whitespace-flexible, word-bounded match for an ASCII formula."""
    body = r"\s+".join(re.escape(w) for w in ascii_text.split())
    lead = r"(?<![\w])" if ascii_text[0].isalnum() else ""
    tail = r"(?![\w])" if ascii_text[-1].isalnum() else ""
    return re.compile(lead + body + tail)


_RULES = ([(_pat(a), b) for a, b in INLINE_FORMULAS]
          + [(_pat(a), b) for a, b in UNITS]
          + [(re.compile(rf"(?<![\w]){re.escape(a)}(?![\w])"), b) for a, b in SYMBOLS.items()])


def _mathify_plain(text: str) -> str:
    """Inline rules on a run of plain text: each match becomes a sentinel so
    a later, shorter rule cannot fire inside it; sentinels become math."""
    found = []
    for rx, latex in _RULES:
        def keep(m, latex=latex):
            found.append(latex)
            return f"\x00{len(found) - 1}\x00"
        text = rx.sub(keep, text)
    text = text.replace(*ARROW)
    return re.sub(r"\x00(\d+)\x00", lambda m: rf"\({found[int(m.group(1))]}\)", text)


def mathify(body: str) -> str:
    """The ASCII physics of the markdown as LaTeX math, leaving code spans
    and unmapped code blocks alone."""
    lines = body.split("\n")
    out, i = [], 0
    while i < len(lines):
        if lines[i].startswith("    ") and (i == 0 or not lines[i - 1].strip()):
            j = i
            while j < len(lines) and lines[j].startswith("    "):
                j += 1
            key = " ".join(" ".join(l.split()) for l in lines[i:j])
            if key in DISPLAY_EQUATIONS:
                out.append(rf"\[{DISPLAY_EQUATIONS[key]}\]")
            else:
                out.extend(lines[i:j])
            i = j
            continue
        out.append(lines[i])
        i += 1
    text = "\n".join(out)
    parts = _PROTECTED_RE.split(text)
    return "".join(p if _PROTECTED_RE.fullmatch(p) else _mathify_plain(p) for p in parts)


_PROTECTED_RE = re.compile(r"(`[^`\n]*`|\\\[.*?\\\]|\\\(.*?\\\))", re.S)


def leftover_ascii_math(text: str) -> list[str]:
    """ASCII math still in the prose of a mathified body (code spans and
    math excluded): the guard that a new equation gets a mapping."""
    plain = _PROTECTED_RE.sub(" ", text)
    return sorted(set(m.group(0) for m in LEFTOVER_RE.finditer(plain)))


def prepare_markdown(text: str, figure_ext: str = "pdf") -> tuple[str, str, str]:
    """(title, author, body): the leading H1 lifted out as the document
    title and the italic byline under it as the author, figure links
    pointed at the converted copies, and every pipe table's separator row
    re-dashed by column_dashes (pandoc reads the dashes as relative
    widths)."""
    lines = text.split("\n")
    title = author = ""
    for i, line in enumerate(lines):
        if line.strip():
            if line.startswith("# "):
                title = line[2:].strip()
                lines = lines[i + 1:]
            break
    for i, line in enumerate(lines):
        if line.strip():
            m = _BYLINE_RE.match(line.strip())
            if m:
                author = m.group(1).strip()
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
    return title, author, mathify("\n".join(out))


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
    lifted, author, body = prepare_markdown(md_path.read_text(encoding="utf-8"),
                                            _figure_ext(out_tex.parent))
    title = title or lifted
    cmd = ["pandoc", "--from", PANDOC_FROM, "--to", "latex", "--standalone",
           "--wrap=none", "--metadata", f"title={title}",
           "--variable", f"header-includes={TABLE_PREAMBLE}"]
    if author:
        cmd += ["--metadata", f"author={author}"]
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
