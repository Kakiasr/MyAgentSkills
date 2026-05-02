#!/usr/bin/env python3
"""Create a simple Chinese-capable PDF game design document.

Input is a UTF-8 Markdown-like text file. Use diagram directives to insert a
diagram page from the same JSON format accepted by create_diagram_svg.py:

[[diagram:artifacts/diagrams/core-loop.json]]

This script uses only Python's standard library and PDF built-in CJK font names.
It is intended as a reliable fallback when pandoc, wkhtmltopdf, browser PDF
printing, or reportlab are unavailable.
"""

from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path
from typing import Any


PAGE_W = 595
PAGE_H = 842
MARGIN_X = 54
MARGIN_TOP = 64
LINE_H = 18

STYLES = {
    "action": (0.933, 0.953, 0.984),
    "info": (1.0, 0.961, 0.839),
    "branch": (0.984, 0.878, 0.878),
    "loop": (0.914, 0.878, 0.980),
    "root": (0.0, 0.0, 0.0),
    "category": (0.384, 0.416, 0.451),
    "system": (0.961, 0.969, 0.980),
    "note": (1.0, 1.0, 1.0),
    "purpose": (0.914, 0.357, 0.357),
    "operation": (0.310, 0.514, 0.945),
    "obstacle": (0.961, 0.631, 0.259),
    "and": (1.0, 1.0, 1.0),
    "or": (0.349, 0.380, 0.416),
    "knowledge": (0.910, 0.882, 0.969),
    "reward": (0.875, 0.949, 0.847),
    "decision": (1.0, 0.969, 0.784),
}

WHITE_TEXT = {"root", "category", "purpose", "operation", "obstacle", "or"}


def text_units(text: str) -> int:
    return sum(2 if ord(ch) > 127 else 1 for ch in text)


def wrap(text: str, max_units: int) -> list[str]:
    lines: list[str] = []
    current = ""
    width = 0
    for ch in text:
        char_width = 2 if ord(ch) > 127 else 1
        if current and width + char_width > max_units:
            lines.append(current)
            current = ch
            width = char_width
        else:
            current += ch
            width += char_width
    if current:
        lines.append(current)
    return lines or [""]


def pdf_text(text: str) -> str:
    return "<" + text.encode("utf-16-be").hex().upper() + ">"


def rect(x: float, y: float, w: float, h: float, fill: tuple[float, float, float], stroke: bool = True) -> str:
    r, g, b = fill
    cmds = [f"{r:.3f} {g:.3f} {b:.3f} rg", f"{x:.1f} {y:.1f} {w:.1f} {h:.1f} re"]
    cmds.append("B" if stroke else "f")
    return "\n".join(cmds) + "\n"


def line(x1: float, y1: float, x2: float, y2: float) -> str:
    angle = math.atan2(y2 - y1, x2 - x1)
    size = 7
    a1 = angle + math.pi * 0.82
    a2 = angle - math.pi * 0.82
    p1 = (x2 + math.cos(a1) * size, y2 + math.sin(a1) * size)
    p2 = (x2 + math.cos(a2) * size, y2 + math.sin(a2) * size)
    return (
        f"0 0 0 RG 1.8 w {x1:.1f} {y1:.1f} m {x2:.1f} {y2:.1f} l S\n"
        f"0 0 0 rg {x2:.1f} {y2:.1f} m {p1[0]:.1f} {p1[1]:.1f} l {p2[0]:.1f} {p2[1]:.1f} l f\n"
    )


def text_cmd(x: float, y: float, text: str, size: int = 11, white: bool = False) -> str:
    color = "1 1 1 rg" if white else "0 0 0 rg"
    return f"BT {color} /F1 {size} Tf {x:.1f} {y:.1f} Td {pdf_text(text)} Tj ET\n"


def node_size(label: str, node_type: str) -> tuple[float, float]:
    lines = wrap(label, 14)
    width = max(72, min(150, max(text_units(line) for line in lines) * 6.4 + 18))
    height = max(34, len(lines) * 16 + 16)
    if node_type in {"and", "or"}:
        width = max(34, width / 2)
    return width, height


def draw_node(node: dict[str, Any], scale: float, off_x: float, off_y: float) -> str:
    label = str(node["label"])
    node_type = str(node.get("type", "system"))
    x = off_x + float(node.get("x", 0)) * scale
    y_top = off_y + float(node.get("y", 0)) * scale
    w, h = node_size(label, node_type)
    w *= scale
    h *= scale
    y = PAGE_H - y_top - h
    out = rect(x, y, w, h, STYLES.get(node_type, STYLES["system"]))
    lines = wrap(label, 14)
    text_y = y + h / 2 + (len(lines) - 1) * 7 - 4
    for idx, part in enumerate(lines):
        approx_w = text_units(part) * 5.2 * scale
        out += text_cmd(x + w / 2 - approx_w / 2, text_y - idx * 14 * scale, part, max(8, int(11 * scale)), node_type in WHITE_TEXT)
    return out


def draw_diagram(spec: dict[str, Any]) -> str:
    nodes = list(spec.get("nodes", []))
    by_id = {str(node["id"]): node for node in nodes}
    max_x = max((float(n.get("x", 0)) + node_size(str(n["label"]), str(n.get("type", "system")))[0] for n in nodes), default=600)
    max_y = max((float(n.get("y", 0)) + node_size(str(n["label"]), str(n.get("type", "system")))[1] for n in nodes), default=300)
    scale = min((PAGE_W - 70) / max_x, (PAGE_H - 140) / max_y, 1.0)
    off_x = 35
    off_y = 80
    out = text_cmd(36, PAGE_H - 42, str(spec.get("title", "图示")), 16)

    for edge in spec.get("edges", []):
        src = by_id[str(edge["from"])]
        dst = by_id[str(edge["to"])]
        sw, sh = node_size(str(src["label"]), str(src.get("type", "system")))
        dw, dh = node_size(str(dst["label"]), str(dst.get("type", "system")))
        sx = off_x + (float(src.get("x", 0)) + sw) * scale
        sy_top = off_y + (float(src.get("y", 0)) + sh / 2) * scale
        dx = off_x + float(dst.get("x", 0)) * scale
        dy_top = off_y + (float(dst.get("y", 0)) + dh / 2) * scale
        out += line(sx, PAGE_H - sy_top, dx, PAGE_H - dy_top)

    for node in nodes:
        out += draw_node(node, scale, off_x, off_y)
    return out


class PDF:
    def __init__(self) -> None:
        self.pages: list[str] = []

    def add_page(self, stream: str) -> None:
        self.pages.append(stream)

    def write(self, path: Path) -> None:
        objects: list[bytes] = []
        objects.append(b"<< /Type /Catalog /Pages 2 0 R >>")
        kids = " ".join(f"{3 + i * 2} 0 R" for i in range(len(self.pages)))
        objects.append(f"<< /Type /Pages /Kids [{kids}] /Count {len(self.pages)} >>".encode())
        for i, stream in enumerate(self.pages):
            content_obj = 4 + i * 2
            page = (
                f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 {PAGE_W} {PAGE_H}] "
                f"/Resources << /Font << /F1 << /Type /Font /Subtype /Type0 /BaseFont /STSong-Light "
                f"/Encoding /UniGB-UCS2-H /DescendantFonts [<< /Type /Font /Subtype /CIDFontType0 "
                f"/BaseFont /STSong-Light /CIDSystemInfo << /Registry (Adobe) /Ordering (GB1) /Supplement 2 >> >>] >> >> >> "
                f"/Contents {content_obj} 0 R >>"
            )
            objects.append(page.encode())
            data = stream.encode("latin-1")
            objects.append(f"<< /Length {len(data)} >>\nstream\n".encode() + data + b"\nendstream")
        output = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
        offsets = [0]
        for idx, obj in enumerate(objects, start=1):
            offsets.append(len(output))
            output.extend(f"{idx} 0 obj\n".encode())
            output.extend(obj)
            output.extend(b"\nendobj\n")
        xref = len(output)
        output.extend(f"xref\n0 {len(objects)+1}\n0000000000 65535 f \n".encode())
        for offset in offsets[1:]:
            output.extend(f"{offset:010d} 00000 n \n".encode())
        output.extend(f"trailer << /Size {len(objects)+1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF\n".encode())
        path.write_bytes(output)


def add_text_pages(pdf: PDF, text: str, base_dir: Path) -> None:
    stream = ""
    y = PAGE_H - MARGIN_TOP
    for raw in text.splitlines():
        match = re.fullmatch(r"\[\[diagram:(.+?)\]\]", raw.strip())
        if match:
            if stream:
                pdf.add_page(stream)
                stream = ""
                y = PAGE_H - MARGIN_TOP
            spec_path = (base_dir / match.group(1)).resolve()
            spec = json.loads(spec_path.read_text(encoding="utf-8"))
            pdf.add_page(draw_diagram(spec))
            continue

        line_text = raw.strip()
        if not line_text:
            y -= LINE_H
            continue
        size = 15 if line_text.startswith("# ") else 12 if line_text.startswith("## ") else 10
        clean = re.sub(r"^#+\s*", "", line_text)
        clean = re.sub(r"^[*-]\s*", "• ", clean)
        for part in wrap(clean, 58 if size <= 10 else 42):
            if y < 54:
                pdf.add_page(stream)
                stream = ""
                y = PAGE_H - MARGIN_TOP
            stream += text_cmd(MARGIN_X, y, part, size)
            y -= LINE_H if size <= 10 else LINE_H + 4
    if stream:
        pdf.add_page(stream)


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a PDF game design document.")
    parser.add_argument("input_md", help="Markdown-like UTF-8 input file")
    parser.add_argument("output_pdf", help="Output PDF path")
    args = parser.parse_args()
    input_path = Path(args.input_md).resolve()
    output_path = Path(args.output_pdf).resolve()
    pdf = PDF()
    add_text_pages(pdf, input_path.read_text(encoding="utf-8"), input_path.parent)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    pdf.write(output_path)
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
