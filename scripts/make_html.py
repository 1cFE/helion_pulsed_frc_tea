"""Render docs/Helion_writeup.md, docs/Helion_short_writeup.md and docs/ledger.md to HTML with pandoc.

Deterministic: fixed pandoc options, figures embedded as data URIs, no
timestamps, so two builds of the same source are byte-identical. Dollar
signs are prose here (the writeup writes $/MWh and M$/kg bare), so the
tex_math_dollars extension is off; lines are not re-wrapped. Run after
editing the writeup; the output directory is not tracked.
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_DIR = ROOT / "outputs"
WRITEUP_MD = ROOT / "docs" / "Helion_writeup.md"
LEDGER_MD = ROOT / "docs" / "ledger.md"
SHORT_MD = ROOT / "docs" / "Helion_short_writeup.md"
OUTPUT_HTML = OUTPUT_DIR / "Helion_writeup_notion.html"
LEDGER_HTML = OUTPUT_DIR / "ledger_notion.html"
PAGE_TITLE = "Helion pulsed FRC TEA writeup"
LEDGER_TITLE = "Helion pulsed FRC TEA ledger"
TARGETS = ((WRITEUP_MD, OUTPUT_HTML.name, PAGE_TITLE),
           (SHORT_MD, "Helion_short_writeup_notion.html", "Helion pulsed FRC TEA short writeup"),
           (LEDGER_MD, LEDGER_HTML.name, LEDGER_TITLE))


def build_html(md_path: Path = WRITEUP_MD, out_path: Path = OUTPUT_HTML,
               page_title: str = PAGE_TITLE) -> Path:
    md_path, out_path = Path(md_path), Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["pandoc", str(md_path), "--from", "markdown-tex_math_dollars",
         "--to", "html5", "--standalone", "--embed-resources", "--wrap=none",
         f"--resource-path={md_path.parent}", "--metadata", f"pagetitle={page_title}",
         "--output", str(out_path)],
        check=True,
    )
    return out_path


def build_all(out_dir: Path = OUTPUT_DIR) -> list[Path]:
    out_dir = Path(out_dir)
    return [build_html(md, out_dir / name, title) for md, name, title in TARGETS]


if __name__ == "__main__":
    for out in build_all():
        print(f"wrote {out.relative_to(ROOT)} ({out.stat().st_size} bytes)", file=sys.stderr)
