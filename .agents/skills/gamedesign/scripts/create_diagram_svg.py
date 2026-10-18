#!/usr/bin/env python3
"""Create SVG diagram images for game design documents from JSON.

This fallback renderer avoids Mermaid/Node dependencies. It supports the node
types required by the game-design skill:

- Game loop: action, info, branch, loop
- Interaction chain: purpose, operation, obstacle, and, or, knowledge, reward, decision
- System maps: root, category, system, note

Input JSON:
{
  "title": "Core Loop",
  "nodes": [
    {"id": "a", "label": "行为：移动", "type": "action", "x": 40, "y": 80}
  ],
  "edges": [{"from": "a", "to": "b", "label": "optional"}]
}
"""

from __future__ import annotations

import argparse
import html
import json
import math
from pathlib import Path
from typing import Any


STYLES = {
    "action": ("#EEF3FB", "#111", "#111"),
    "info": ("#FFF5D6", "#111", "#111"),
    "branch": ("#FBE0E0", "#111", "#111"),
    "loop": ("#E9E0FA", "#111", "#111"),
    "root": ("#000000", "#000", "#FFFFFF"),
    "category": ("#626A73", "#111", "#FFFFFF"),
    "system": ("#F5F7FA", "#111", "#111"),
    "note": ("#FFFFFF", "#FFFFFF", "#111"),
    "purpose": ("#E95B5B", "#111", "#FFFFFF"),
    "operation": ("#4F83F1", "#111", "#FFFFFF"),
    "obstacle": ("#F5A142", "#111", "#FFFFFF"),
    "and": ("#FFFFFF", "#111", "#111"),
    "or": ("#59616A", "#111", "#FFFFFF"),
    "knowledge": ("#E8E1F7", "#111", "#111"),
    "reward": ("#DFF2D8", "#111", "#111"),
    "decision": ("#FFF7C8", "#111", "#111"),
}


def text_width_units(text: str) -> int:
    return sum(2 if ord(ch) > 127 else 1 for ch in text)


def wrap_text(text: str, max_units: int = 14) -> list[str]:
    parts: list[str] = []
    current = ""
    width = 0
    for ch in text:
        char_width = 2 if ord(ch) > 127 else 1
        if current and width + char_width > max_units:
            parts.append(current)
            current = ch
            width = char_width
        else:
            current += ch
            width += char_width
    if current:
        parts.append(current)
    return parts


def node_size(label: str, node_type: str) -> tuple[int, int]:
    lines = wrap_text(label)
    width = max(90, min(220, max(text_width_units(line) for line in lines) * 9 + 28))
    height = max(46, len(lines) * 24 + 22)
    if node_type in {"and", "or"}:
        width = max(48, width // 2)
        height = max(40, height - 8)
    return width, height


def assign_layout(nodes: list[dict[str, Any]]) -> None:
    for index, node in enumerate(nodes):
        node.setdefault("x", 40 + index * 190)
        node.setdefault("y", 90)


def arrow(start: tuple[float, float], end: tuple[float, float], label: str = "") -> str:
    sx, sy = start
    ex, ey = end
    midx = (sx + ex) / 2
    midy = (sy + ey) / 2 - 8
    label_svg = ""
    if label:
        label_svg = (
            f'<text x="{midx:.1f}" y="{midy:.1f}" text-anchor="middle" '
            f'font-size="14" fill="#111">{html.escape(label)}</text>'
        )
    return (
        f'<line x1="{sx:.1f}" y1="{sy:.1f}" x2="{ex:.1f}" y2="{ey:.1f}" '
        'stroke="#111" stroke-width="3" marker-end="url(#arrow)" />'
        f"{label_svg}"
    )


def render_node(node: dict[str, Any]) -> str:
    label = str(node["label"])
    node_type = str(node.get("type", "system"))
    fill, stroke, color = STYLES.get(node_type, STYLES["system"])
    width, height = node_size(label, node_type)
    x = float(node["x"])
    y = float(node["y"])
    radius = 8
    lines = wrap_text(label)
    text_start = y + height / 2 - (len(lines) - 1) * 12 + 7

    text_svg = []
    for index, line in enumerate(lines):
        text_svg.append(
            f'<text x="{x + width / 2:.1f}" y="{text_start + index * 24:.1f}" '
            f'text-anchor="middle" font-size="20" font-family="Arial, PingFang SC, sans-serif" '
            f'font-weight="700" fill="{color}">{html.escape(line)}</text>'
        )

    return (
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{width}" height="{height}" '
        f'rx="{radius}" fill="{fill}" stroke="{stroke}" stroke-width="3" />'
        + "".join(text_svg)
    )


def edge_points(source: dict[str, Any], target: dict[str, Any]) -> tuple[tuple[float, float], tuple[float, float]]:
    sw, sh = node_size(str(source["label"]), str(source.get("type", "system")))
    tw, th = node_size(str(target["label"]), str(target.get("type", "system")))
    sx = float(source["x"]) + sw
    sy = float(source["y"]) + sh / 2
    tx = float(target["x"])
    ty = float(target["y"]) + th / 2
    if tx < sx:
        sx = float(source["x"]) + sw / 2
        sy = float(source["y"]) + sh
        tx = float(target["x"]) + tw / 2
        ty = float(target["y"])
    return (sx, sy), (tx, ty)


def render(spec: dict[str, Any]) -> str:
    nodes = list(spec.get("nodes", []))
    edges = list(spec.get("edges", []))
    assign_layout(nodes)
    by_id = {str(node["id"]): node for node in nodes}

    max_x = 800
    max_y = 420
    for node in nodes:
        width, height = node_size(str(node["label"]), str(node.get("type", "system")))
        max_x = max(max_x, math.ceil(float(node["x"]) + width + 40))
        max_y = max(max_y, math.ceil(float(node["y"]) + height + 40))

    edge_svg = []
    for edge in edges:
        source = by_id[str(edge["from"])]
        target = by_id[str(edge["to"])]
        edge_svg.append(arrow(*edge_points(source, target), str(edge.get("label", ""))))

    title = html.escape(str(spec.get("title", "")))
    title_svg = ""
    if title:
        title_svg = f'<text x="24" y="34" font-size="24" font-weight="800" fill="#111">{title}</text>'

    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{max_x}" height="{max_y}" viewBox="0 0 {max_x} {max_y}">
<defs>
  <marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth">
    <path d="M0,0 L0,6 L9,3 z" fill="#111" />
  </marker>
</defs>
<rect width="100%" height="100%" fill="#fff" />
{title_svg}
{''.join(edge_svg)}
{''.join(render_node(node) for node in nodes)}
</svg>
'''


def main() -> int:
    parser = argparse.ArgumentParser(description="Create an SVG diagram from JSON.")
    parser.add_argument("input_json", help="Diagram spec JSON")
    parser.add_argument("output_svg", help="Output SVG path")
    args = parser.parse_args()

    spec = json.loads(Path(args.input_json).read_text(encoding="utf-8"))
    output = Path(args.output_svg)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(render(spec), encoding="utf-8")
    print(f"Wrote {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
