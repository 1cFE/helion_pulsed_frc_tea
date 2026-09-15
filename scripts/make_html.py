"""Render docs/writeup.md to outputs/writeup_notion.html with pandoc.

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
WRITEUP_MD = ROOT / "docs" / "writeup.md"
OUTPUT_HTML = ROOT / "outputs" / "writeup_notion.html"
PAGE_TITLE = "Helion pulsed FRC TEA writeup"


def build_html(md_path: Path = WRITEUP_MD, out_path: Path = OUTPUT_HTML) -> Path:
    md_path, out_path = Path(md_path), Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["pandoc", str(md_path), "--from", "markdown-tex_math_dollars",
         "--to", "html5", "--standalone", "--embed-resources", "--wrap=none",
         f"--resource-path={md_path.parent}", "--metadata", f"pagetitle={PAGE_TITLE}",
         "--output", str(out_path)],
        check=True,
    )
    return out_path


if __name__ == "__main__":
    out = build_html()
    print(f"wrote {out.relative_to(ROOT)} ({out.stat().st_size} bytes)", file=sys.stderr)
