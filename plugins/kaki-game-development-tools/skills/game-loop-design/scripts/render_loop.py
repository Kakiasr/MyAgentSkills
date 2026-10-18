"""Render explicitly authored loop graphs to SVG and Mermaid; stdlib only."""
import argparse
import html
import json
import math
import re
import unicodedata
from pathlib import Path

KINDS = {"action": "#edf2fc", "information": "#fff2cb", "branch": "#ffe4e2", "subloop": "#eae1fc"}


def number(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{name} must be a finite number")
    return value


def graph_data(data):
    if not isinstance(data, dict):
        raise ValueError("Graph must be a JSON object")
    width, height = number(data.get("width", 1100), "width"), number(data.get("height", 800), "height")
    if width < 100 or height < 100:
        raise ValueError("Canvas dimensions must be at least 100")
    nodes, edges = data.get("nodes"), data.get("edges")
    if not isinstance(nodes, list) or not nodes or not isinstance(edges, list):
        raise ValueError("Provide a nonempty nodes list and an edges list")
    lookup = {}
    for original in nodes:
        if not isinstance(original, dict):
            raise ValueError("Every node must be an object")
        node = dict(original)
        key = node.get("id")
        if not isinstance(key, str) or not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", key) or key in lookup:
            raise ValueError(f"Invalid or duplicate node ID: {key!r}")
        if not isinstance(node.get("label"), str) or not node["label"].strip():
            raise ValueError(f"Node {key} requires a label")
        if node.get("kind") not in KINDS:
            raise ValueError(f"Node {key}: kind must be action, information, branch, or subloop")
        for prop, default in (("width", 180), ("height", 72)):
            node[prop] = number(node.get(prop, default), f"{key}.{prop}")
            if node[prop] <= 0:
                raise ValueError("Node dimensions must be positive")
        for prop in ("x", "y"):
            node[prop] = number(node.get(prop), f"{key}.{prop}")
        if not (0 <= node["x"] - node["width"] / 2 and node["x"] + node["width"] / 2 <= width
                and 0 <= node["y"] - node["height"] / 2 and node["y"] + node["height"] / 2 <= height):
            raise ValueError(f"Node {key} is outside canvas")
        lookup[key] = node
    loops = data.get("loops")
    if not isinstance(loops, list) or not loops:
        raise ValueError("Provide loop bodies with separately scoped global_information")
    loop_lookup, global_ids = {}, set()
    for original in loops:
        if not isinstance(original, dict):
            raise ValueError("Every loop body must be an object")
        loop = dict(original)
        key = loop.get("id")
        if not isinstance(key, str) or not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", key) or key in loop_lookup:
            raise ValueError("Invalid or duplicate loop ID")
        if not isinstance(loop.get("label"), str) or not loop["label"].strip():
            raise ValueError(f"Loop {key} requires a name")
        for prop in ("x", "y", "width", "height"):
            loop[prop] = number(loop.get(prop), f"{key}.{prop}")
        if loop["width"] <= 0 or loop["height"] <= 0 or not (
            0 <= loop["x"] - loop["width"]/2 < loop["x"] + loop["width"]/2 <= width
            and 0 <= loop["y"] - loop["height"]/2 < loop["y"] + loop["height"]/2 <= height):
            raise ValueError(f"Loop {key} has invalid bounds")
        facts = loop.get("global_information")
        if not isinstance(facts, list) or any(not isinstance(f, str) for f in facts) or len(facts) != len(set(facts)):
            raise ValueError(f"Loop {key} requires a global_information ID list")
        note = loop.get("global_information_note", "")
        if not isinstance(note, str) or (not facts and not note.strip()):
            raise ValueError(f"Loop {key}: explicitly state no available information or unknown scope")
        for fact in facts:
            if fact not in lookup or lookup[fact]["kind"] != "information" or lookup[fact].get("loop") != key or fact in global_ids:
                raise ValueError(f"Global information {fact} must be an information node owned by loop {key}")
        global_ids.update(facts)
        loop_lookup[key] = loop
    for node in lookup.values():
        scope = node.get("loop")
        if not isinstance(scope, str) or scope not in loop_lookup:
            raise ValueError(f"Node {node['id']} requires a known loop scope")
        loop = loop_lookup[scope]
        if abs(node["x"]-loop["x"]) + node["width"]/2 > loop["width"]/2 or abs(node["y"]-loop["y"]) + node["height"]/2 > loop["height"]/2:
            raise ValueError(f"Node {node['id']} is outside its loop body")
        if node.get("loop_ref") is not None and (node["kind"] != "subloop" or node["loop_ref"] not in loop_lookup):
            raise ValueError(f"Invalid expanded subloop reference on {node['id']}")
    normalized_edges = []
    for original in edges:
        if not isinstance(original, dict):
            raise ValueError("Every edge must be an object")
        edge = dict(original)
        if not isinstance(edge.get("from"), str) or not isinstance(edge.get("to"), str) or edge["from"] not in lookup or edge["to"] not in lookup:
            raise ValueError("Edge references an unknown node")
        if edge["from"] in global_ids or edge["to"] in global_ids:
            raise ValueError("Global information belongs to a loop body, not the step sequence")
        if not isinstance(edge.get("label", ""), str):
            raise ValueError("Edge label must be a string")
        via = edge.get("via", [])
        if not isinstance(via, list):
            raise ValueError("via must be a point list")
        for point in via:
            if not isinstance(point, list) or len(point) != 2:
                raise ValueError("Each via point must have x and y")
            x, y = number(point[0], "via.x"), number(point[1], "via.y")
            if not (0 <= x <= width and 0 <= y <= height):
                raise ValueError("via point is outside canvas")
        if ("label_x" in edge) != ("label_y" in edge):
            raise ValueError("Provide both label_x and label_y")
        if "label_x" in edge:
            x, y = number(edge["label_x"], "label_x"), number(edge["label_y"], "label_y")
            if not (0 <= x <= width and 0 <= y <= height):
                raise ValueError("Edge label is outside canvas")
        edge["via"] = via
        normalized_edges.append(edge)
    start = data.get("start", nodes[0]["id"])
    if not isinstance(start, str) or start not in lookup or start in global_ids:
        raise ValueError("Unknown start node")
    return width, height, lookup, normalized_edges, start, loop_lookup, global_ids


def graph_checks(nodes, edges, start, global_ids=()):
    adjacent = {key: [] for key in nodes}
    for edge in edges:
        adjacent[edge["from"]].append(edge["to"])
    active, done, cyclic = set(), set(), False

    def visit(key):
        nonlocal cyclic
        if key in active:
            cyclic = True
            return
        if key in done:
            return
        active.add(key)
        for target in adjacent[key]:
            visit(target)
        active.remove(key)
        done.add(key)

    for key in nodes:
        visit(key)
    reachable, pending = set(), [start]
    while pending:
        key = pending.pop()
        if key not in reachable and key not in global_ids:
            reachable.add(key)
            pending.extend(adjacent[key])
    warnings = []
    if not cyclic:
        warnings.append("No directed cycle: this may be a flow, not a closed gameplay loop.")
    for key in nodes:
        if key not in reachable and key not in global_ids:
            warnings.append(f"Unreachable node: {key}")
        if nodes[key]["kind"] == "branch":
            outgoing = [edge for edge in edges if edge["from"] == key]
            if len(outgoing) < 2 or any(not edge.get("label", "").strip() for edge in outgoing):
                warnings.append(f"Decision {key} needs labeled outcome branches.")
        for other in nodes:
            if key >= other:
                continue
            a, b = nodes[key], nodes[other]
            if abs(a["x"] - b["x"]) < (a["width"] + b["width"]) / 2 and abs(a["y"] - b["y"]) < (a["height"] + b["height"]) / 2:
                warnings.append(f"Overlapping node bounds: {key}, {other}")
    return {"nodes": len(nodes), "edges": len(edges), "has_directed_cycle": cyclic,
            "global_information_nodes": sorted(global_ids),
            "unreachable_nodes": sorted(set(nodes) - reachable - set(global_ids)), "warnings": warnings,
            "visual_preview_performed": False, "gameplay_tests_executed": False}


def boundary(node, toward):
    dx, dy = toward[0] - node["x"], toward[1] - node["y"]
    if dx == 0 and dy == 0:
        raise ValueError("Edge needs a distinct routing point (self-loops require via points)")
    ratio = max(abs(dx) / (node["width"] / 2), abs(dy) / (node["height"] / 2))
    return node["x"] + dx / ratio, node["y"] + dy / ratio


def text_svg(text, x, y, size=16):
    lines = text.splitlines() or [""]
    top = y - (len(lines) - 1) * (size + 4) / 2
    return f'<text x="{x}" y="{top}" font-size="{size}" text-anchor="middle" dominant-baseline="middle">' + "".join(
        f'<tspan x="{x}" dy="{0 if i == 0 else size + 4}">{html.escape(line)}</tspan>' for i, line in enumerate(lines)) + '</text>'


def mermaid_label(value):
    return html.escape(value, quote=True).replace("\n", "<br/>")


def render(data):
    width, height, nodes, edges, start, loops, global_ids = graph_data(data)
    title = data.get("title", "")
    if not isinstance(title, str):
        raise ValueError("Title must be a string")
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
           '<rect width="100%" height="100%" fill="#f8fafc"/>',
           '<defs><marker id="arrow" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 Z" fill="#475569"/></marker></defs>',
           '<g font-family="Segoe UI,Microsoft YaHei,Noto Sans CJK SC,sans-serif" fill="#0f172a">']
    if title.strip():
        svg.append(text_svg(title, width / 2, 24, 21))
    mmd = ['flowchart TD']
    for key, loop in loops.items():
        left, top = loop["x"]-loop["width"]/2, loop["y"]-loop["height"]/2
        svg.append(f'<rect x="{left}" y="{top}" width="{loop["width"]}" height="{loop["height"]}" rx="14" fill="#ffffff" stroke="#c7cdd8"/>')
        svg.append(text_svg(loop["label"], loop["x"], top+25, 20))
        facts = [nodes[f] for f in loop["global_information"]]
        if facts:
            x1=min(n["x"]-n["width"]/2 for n in facts)-12
            x2=max(n["x"]+n["width"]/2 for n in facts)+12
            y1=min(n["y"]-n["height"]/2 for n in facts)-38
            y2=max(n["y"]+n["height"]/2 for n in facts)+12
            if not (left <= x1 < x2 <= left+loop["width"] and top+45 <= y1 < y2 <= top+loop["height"]):
                raise ValueError(f"Loop {key}: leave room for global information header and panel")
            svg.append(f'<rect x="{x1}" y="{y1}" width="{x2-x1}" height="{y2-y1}" rx="8" fill="#fffdf6" stroke="#e1d6ae"/>')
            svg.append(text_svg("全局可获取信息", (x1+x2)/2, y1+17, 16))
        else:
            svg.append(text_svg("全局可获取信息："+loop["global_information_note"], loop["x"], top+65, 16))
        mmd.append(f'  subgraph L_{key}["{mermaid_label(loop["label"])}"]')
        mmd.append(f'    subgraph G_{key}["全局可获取信息"]')
        for fact in facts:
            mmd.append(f'      N_{fact["id"]}["{mermaid_label(fact["label"])}"]')
        if not facts:
            mmd.append(f'      G_{key}_note["{mermaid_label(loop["global_information_note"])}"]:::information')
        mmd.append('    end')
        for node in nodes.values():
            if node["loop"] == key and node["id"] not in global_ids:
                mmd.append(f'    N_{node["id"]}["{mermaid_label(node["label"])}"]')
        mmd.append('  end')
    for edge in edges:
        a, b = nodes[edge["from"]], nodes[edge["to"]]
        via = edge["via"]
        points = [boundary(a, via[0] if via else (b["x"], b["y"])), *via,
                  boundary(b, via[-1] if via else (a["x"], a["y"]))]
        path = " ".join(("M" if i == 0 else "L") + f"{p[0]},{p[1]}" for i, p in enumerate(points))
        svg.append(f'<path d="{path}" fill="none" stroke="#475569" stroke-width="2" marker-end="url(#arrow)"/>')
        label = edge.get("label", "")
        if label:
            middle = len(points) // 2
            p, q = points[middle - 1], points[middle]
            x = edge.get("label_x", (p[0] + q[0]) / 2)
            y = edge.get("label_y", (p[1] + q[1]) / 2 - 12)
            line_width = max(sum(2 if unicodedata.east_asian_width(c) in 'WF' else 1 for c in line) for line in label.splitlines()) * 6.5 + 12
            label_height = max(1, len(label.splitlines())) * 17 + 4
            svg.append(f'<rect x="{x-line_width/2}" y="{y-label_height/2}" width="{line_width}" height="{label_height}" rx="4" fill="#f8fafc"/>')
            svg.append(text_svg(label, x, y, 13))
        mmd.append(f'  N_{edge["from"]} -->' + (f'|"{mermaid_label(label)}"|' if label else '') + f' N_{edge["to"]}')
    for node in nodes.values():
        x, y, w, h = node["x"], node["y"], node["width"], node["height"]
        fill = KINDS[node["kind"]]
        svg.append(f'<rect x="{x-w/2}" y="{y-h/2}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="#334155"/>')
        svg.append(text_svg(node["label"], x, y))
    for kind, color in KINDS.items():
        mmd.append(f'  classDef {kind} fill:{color},stroke:#334155;')
        members = [f'N_{key}' for key, node in nodes.items() if node["kind"] == kind]
        if members:
            mmd.append(f'  class {",".join(members)} {kind};')
    svg.append('</g></svg>')
    report = graph_checks(nodes, edges, start, global_ids)
    report["loop_bodies"] = len(loops)
    return '\n'.join(svg) + '\n', '\n'.join(mmd) + '\n', report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('graph', type=Path)
    parser.add_argument('--output-dir', type=Path, required=True)
    parser.add_argument('--overwrite', action='store_true')
    args = parser.parse_args()
    try:
        svg, mmd, report = render(json.loads(args.graph.read_text(encoding='utf-8-sig')))
        output = args.output_dir.resolve()
        targets = [output / name for name in ('loop.svg', 'loop.mmd', 'loop-check.json')]
        if output == args.graph.resolve().parent and args.graph.resolve() in targets:
            raise ValueError('Output would replace input graph')
        if not args.overwrite and any(path.exists() for path in targets):
            raise ValueError('Output exists; use a new output directory or explicitly authorize --overwrite')
        output.mkdir(parents=True, exist_ok=True)
        for path, text in zip(targets, (svg, mmd, json.dumps(report, ensure_ascii=False, indent=2) + '\n')):
            path.write_text(text, encoding='utf-8')
        print(json.dumps({'outputs': [str(p) for p in targets], 'checks': report}, ensure_ascii=False))
    except (ValueError, OSError) as exc:
        parser.exit(2, f'Cannot render graph: {exc}\n')


if __name__ == '__main__':
    main()
