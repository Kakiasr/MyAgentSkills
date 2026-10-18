#!/usr/bin/env python3
"""Render Mermaid diagram sources in a folder to image files.

The script prefers local Mermaid CLI (`mmdc`) when available. If `mmdc` is not
installed, it keeps the `.mmd` files intact and reports the command to run.
Use this for game design document diagrams that must be delivered as images.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
from pathlib import Path


def render_with_mmdc(source: Path, output: Path) -> None:
    subprocess.run(
        ["mmdc", "-i", str(source), "-o", str(output), "--backgroundColor", "white"],
        check=True,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Render .mmd files to SVG/PNG images.")
    parser.add_argument("diagram_dir", help="Directory containing Mermaid .mmd files")
    parser.add_argument(
        "--png",
        action="store_true",
        help="Also render PNG files. SVG is always rendered first.",
    )
    args = parser.parse_args()

    diagram_dir = Path(args.diagram_dir).resolve()
    if not diagram_dir.exists():
        raise SystemExit(f"Directory does not exist: {diagram_dir}")

    sources = sorted(diagram_dir.glob("*.mmd"))
    if not sources:
        print(f"No .mmd files found in {diagram_dir}")
        return 0

    if not shutil.which("mmdc"):
        print("Mermaid CLI `mmdc` was not found.")
        print("Install it with: npm install -g @mermaid-js/mermaid-cli")
        print("Then rerun this script:")
        print(f"python3 {Path(__file__).name} {diagram_dir}")
        return 1

    for source in sources:
        svg = source.with_suffix(".svg")
        render_with_mmdc(source, svg)
        print(f"Rendered {svg}")

        if args.png:
            png = source.with_suffix(".png")
            render_with_mmdc(source, png)
            print(f"Rendered {png}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
