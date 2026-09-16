"""LaTeX and PDF renderings of the writeup and the ledger (scripts/make_latex.py),
produced deterministically from the markdown with the figures as PDF."""
import shutil
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from make_latex import (  # noqa: E402
    LEDGER_MD,
    WRITEUP_MD,
    build_all,
    build_tex,
    prepare_markdown,
)

pytestmark = pytest.mark.skipif(
    shutil.which("pandoc") is None or shutil.which("pdflatex") is None,
    reason="pandoc and pdflatex are both needed")


def test_prepare_lifts_the_title_and_byline_and_points_figures_at_pdf():
    title, author, body = prepare_markdown(WRITEUP_MD.read_text(encoding="utf-8"))
    assert title.startswith("The techno-economic floor")
    assert author == "Tal Rubin, Astera Institute"
    assert not body.lstrip().startswith("# ")
    assert not body.lstrip().startswith("*Tal Rubin")
    assert "figures/fig1_ladder.pdf" in body
    assert ".svg" not in body


def test_mathify_sets_display_and_inline_equations():
    from make_latex import mathify
    body = ("so\n\n    gain <= chi x burn time / breakeven time,\n\nwith chi(x_s) = "
            "1.5 <beta> x_s^2 / (1.5 <beta> x_s^2 + 1 - x_s^2) and `eta_dec` in code, "
            "eta_dec in prose, n_D 0.75e22 m^-3 and a 1.5 MJ/m^2 flash")
    out = mathify(body)
    assert "\\[\\mathrm{gain} \\le \\chi" in out
    assert "\\(\\chi(x_s) = 1.5\\langle\\beta\\rangle x_s^2" in out
    assert "`eta_dec`" in out
    assert "\\(\\eta_{\\mathrm{dec}}\\) in prose" in out
    assert "\\(n_D\\) 0.75e22 \\(\\mathrm{m^{-3}}\\)" in out
    assert "\\(\\mathrm{MJ/m^2}\\)" in out
    from make_latex import leftover_ascii_math
    assert leftover_ascii_math(out) == []
    assert mathify(out) == out


def test_no_ascii_math_is_left_in_either_document():
    from make_latex import leftover_ascii_math
    for md in (WRITEUP_MD, LEDGER_MD):
        _, _, body = prepare_markdown(md.read_text(encoding="utf-8"))
        assert leftover_ascii_math(body) == [], md.name


def test_tex_typesets_the_equations(tmp_path):
    tex = build_tex(WRITEUP_MD, tmp_path / "writeup.tex").read_text(encoding="utf-8")
    assert "\\[\\mathrm{gain} \\le \\chi" in tex
    assert "\\eta_{\\mathrm{dec}}" in tex
    assert "\\langle\\sigma v\\rangle_{DD}" in tex
    assert "gain <= chi" not in tex


def test_tex_carries_the_author_on_both_documents(tmp_path):
    for md in (WRITEUP_MD, LEDGER_MD):
        tex = build_tex(md, tmp_path / (md.stem + ".tex")).read_text(encoding="utf-8")
        assert "\\author{Tal Rubin, Astera Institute}" in tex


def test_prepare_widens_table_separators_with_the_content():
    md = "| knob | why |\n|---|---|\n| a | " + "long " * 40 + "|\n"
    _, _, body = prepare_markdown(md)
    sep = body.splitlines()[1]
    cells = [c for c in sep.strip().strip("|").split("|")]
    assert len(cells[1]) > len(cells[0])


def test_prepare_reserves_the_width_an_unbreakable_token_needs():
    """A 17-character number cannot hyphenate or break, so its column's
    dash share must cover it even beside a paragraph column; an
    identifier breaks at its underscores and needs only its longest piece."""
    md = ("| knob | value | note |\n|---|---|---|\n"
          "| dec_staged_recovery_factor | 1234567890.123456 | " + "word " * 120 + "|\n")
    _, _, body = prepare_markdown(md)
    cells = body.splitlines()[1].strip().strip("|").split("|")
    shares = [len(c) / sum(len(x) for x in cells) for c in cells]
    assert shares[1] >= 0.19
    assert shares[0] < shares[1]


def test_tex_cells_get_break_opportunities_and_small_type(tmp_path):
    tex = build_tex(LEDGER_MD, tmp_path / "ledger.tex").read_text(encoding="utf-8")
    assert "\\AtBeginEnvironment{longtable}{\\footnotesize}" in tex
    assert "\\raggedright\\hspace{0pt}" in tex
    assert "wall\\_\\allowbreak{}dpa\\_\\allowbreak{}tolerance" in tex


def test_tex_carries_the_title_escaped_dollars_and_figures(tmp_path):
    out = build_tex(WRITEUP_MD, tmp_path / "writeup.tex")
    tex = out.read_text(encoding="utf-8")
    assert "\\title{The techno-economic floor" in tex
    assert tex.count("\\includegraphics") == 5
    assert "figures/fig1_ladder.pdf" in tex
    assert "\\$/MWh" in tex
    assert "\\begin{figure}" not in tex


def test_two_tex_builds_are_byte_identical(tmp_path):
    a = build_tex(WRITEUP_MD, tmp_path / "a.tex")
    b = build_tex(WRITEUP_MD, tmp_path / "b.tex")
    assert a.read_bytes() == b.read_bytes()


def test_ledger_tex_renders_every_table_as_a_longtable(tmp_path):
    tex = build_tex(LEDGER_MD, tmp_path / "ledger.tex").read_text(encoding="utf-8")
    assert tex.count("\\begin{longtable}") == 11
    assert "\\real{" in tex


def test_build_all_compiles_all_three_documents(tmp_path):
    written = build_all(tmp_path)
    names = sorted(p.name for p in written)
    assert names == ["ledger.pdf", "ledger.tex", "short_writeup.pdf", "short_writeup.tex",
                     "writeup.pdf", "writeup.tex"]
    for p in written:
        if p.suffix == ".pdf":
            assert p.stat().st_size > 50_000
            assert p.read_bytes()[:5] == b"%PDF-"
