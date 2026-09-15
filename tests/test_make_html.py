"""The HTML rendering of the writeup is produced by scripts/make_html.py,
deterministically, from docs/writeup.md with the figures embedded."""
import shutil
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from make_html import WRITEUP_MD, build_html  # noqa: E402

pytestmark = pytest.mark.skipif(shutil.which("pandoc") is None, reason="pandoc not installed")


def test_html_carries_the_writeup_title_and_embedded_figures(tmp_path):
    out = tmp_path / "writeup.html"
    build_html(WRITEUP_MD, out)
    html = out.read_text(encoding="utf-8")
    assert "<title>Helion pulsed FRC TEA writeup</title>" in html
    assert "The techno-economic floor of a Helion-class pulsed inductive fusion power plant" in html
    assert html.count("data:image/svg+xml") == 5
    assert "figures/fig1_ladder.svg" not in html


def test_two_builds_are_byte_identical(tmp_path):
    a, b = tmp_path / "a.html", tmp_path / "b.html"
    build_html(WRITEUP_MD, a)
    build_html(WRITEUP_MD, b)
    assert a.read_bytes() == b.read_bytes()
