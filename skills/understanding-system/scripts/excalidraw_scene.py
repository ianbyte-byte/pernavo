#!/usr/bin/env python3
"""Write one .excalidraw file from a row of named nodes and labeled edges."""

from __future__ import annotations

import argparse
import json
import secrets
import sys
import time
from pathlib import Path


FONT_FAMILY = 1
FONT_SIZE = 20
RECT_HEIGHT = 76
GAP = 88


def text_width(text: str, font_size: int = FONT_SIZE) -> float:
    width = 0.0
    for char in text:
        width += font_size * (1.0 if ord(char) > 127 else 0.56)
    return width


def new_id(prefix: str) -> str:
    return "%s-%s" % (prefix, secrets.token_hex(4))


def base(element_id: str, element_type: str, x: float, y: float, width: float, height: float) -> dict:
    return {
        "id": element_id,
        "type": element_type,
        "x": x,
        "y": y,
        "width": width,
        "height": height,
        "angle": 0,
        "strokeColor": "#1e1e1e",
        "backgroundColor": "transparent",
        "fillStyle": "solid",
        "strokeWidth": 2,
        "strokeStyle": "solid",
        "roughness": 1,
        "opacity": 100,
        "groupIds": [],
        "frameId": None,
        "roundness": None,
        "seed": secrets.randbelow(2**31 - 1) + 1,
        "version": 1,
        "versionNonce": secrets.randbelow(2**31 - 1) + 1,
        "isDeleted": False,
        "boundElements": [],
        "updated": int(time.time() * 1000),
        "link": None,
        "locked": False,
    }


def label(shape: dict, text: str, font_size: int = FONT_SIZE) -> dict:
    width = text_width(text, font_size)
    height = font_size * 1.25
    element = base(new_id("label"), "text", shape["x"] + (shape["width"] - width) / 2, shape["y"] + (shape["height"] - height) / 2, width, height)
    element.update(
        {
            "text": text,
            "fontSize": font_size,
            "fontFamily": FONT_FAMILY,
            "textAlign": "center",
            "verticalAlign": "middle",
            "containerId": shape["id"],
            "originalText": text,
            "autoResize": True,
            "lineHeight": 1.25,
            "baseline": int(font_size * 0.9),
        }
    )
    shape["boundElements"].append({"id": element["id"], "type": "text"})
    return element


def node_size(node: dict) -> tuple[float, float]:
    label_width = text_width(node["text"]) + 36
    if node.get("shape") == "diamond":
        side = max(160.0, label_width * 1.7)
        return side, side
    return max(150.0, label_width), RECT_HEIGHT


def parse_scene(scene: dict) -> tuple[list[dict], list[dict], str]:
    if not isinstance(scene, dict):
        raise ValueError("scene must be an object")
    nodes = scene.get("nodes")
    edges = scene.get("edges", [])
    title = scene.get("title", "")
    if not isinstance(nodes, list) or not nodes:
        raise ValueError("scene.nodes must be a non-empty list")
    if not isinstance(edges, list):
        raise ValueError("scene.edges must be a list")
    if not isinstance(title, str):
        raise ValueError("scene.title must be a string")
    seen = set()
    for node in nodes:
        if not isinstance(node, dict) or not node.get("id") or not node.get("text"):
            raise ValueError("each node needs id and text")
        if node["id"] in seen:
            raise ValueError("duplicate node id: %s" % node["id"])
        seen.add(node["id"])
        shape = node.get("shape", "rectangle")
        if shape not in ("rectangle", "diamond"):
            raise ValueError("shape must be rectangle or diamond: %s" % node["id"])
        node["shape"] = shape
    for edge in edges:
        if not isinstance(edge, dict) or edge.get("from") not in seen or edge.get("to") not in seen:
            raise ValueError("each edge needs from and to node ids")
        if not isinstance(edge.get("text", ""), str):
            raise ValueError("edge text must be a string")
    return nodes, edges, title


def build(scene: dict) -> dict:
    nodes, edges, title = parse_scene(scene)
    elements = []
    placed = {}
    cursor = 40.0
    top = 80.0
    for index, node in enumerate(nodes):
        width, height = node_size(node)
        y = top + (0 if node["shape"] == "rectangle" else (RECT_HEIGHT - height) / 2)
        shape = base(str(node["id"]), node["shape"], cursor, y, width, height)
        shape["backgroundColor"] = "#ffec99" if node["shape"] == "diamond" else "#a5d8ff"
        if node["shape"] == "rectangle":
            shape["roundness"] = {"type": 3}
        elements.append(shape)
        elements.append(label(shape, node["text"]))
        placed[node["id"]] = (index, shape)
        cursor += width + GAP

    if title:
        title_width = text_width(title, 28)
        title_el = base(new_id("title"), "text", 40, 24, title_width, 36)
        title_el.update(
            {
                "text": title,
                "fontSize": 28,
                "fontFamily": FONT_FAMILY,
                "textAlign": "left",
                "verticalAlign": "top",
                "originalText": title,
                "autoResize": True,
                "lineHeight": 1.25,
                "baseline": 25,
                "containerId": None,
            }
        )
        elements.insert(0, title_el)

    for edge in edges:
        source = placed[edge["from"]][1]
        target = placed[edge["to"]][1]
        start_x = source["x"] + source["width"]
        start_y = source["y"] + source["height"] / 2
        end_x = target["x"]
        end_y = target["y"] + target["height"] / 2
        source_index = placed[edge["from"]][0]
        target_index = placed[edge["to"]][0]
        if target_index == source_index + 1 and end_x >= start_x:
            points = [[0, 0], [end_x - start_x, end_y - start_y]]
        else:
            lift = min(source["y"], target["y"]) - 48 - start_y
            points = [[0, 0], [0, lift], [end_x - start_x, lift], [end_x - start_x, end_y - start_y]]
        arrow = base(new_id("edge"), "arrow", start_x, start_y, abs(points[-1][0]), abs(points[-1][1]))
        arrow.update(
            {
                "points": points,
                "endArrowhead": None if edge.get("text") in ("1", "N", "M") else "arrow",
                "startBinding": {"elementId": source["id"], "focus": 0, "gap": 8, "fixedPoint": [1, 0.5]},
                "endBinding": {"elementId": target["id"], "focus": 0, "gap": 8, "fixedPoint": [0, 0.5]},
                "backgroundColor": "transparent",
            }
        )
        source["boundElements"].append({"id": arrow["id"], "type": "arrow"})
        target["boundElements"].append({"id": arrow["id"], "type": "arrow"})
        elements.append(arrow)
        edge_text = edge.get("text") or ""
        if edge_text:
            mid_x = start_x + points[-1][0] / 2
            mid_y = start_y + points[-1][1] / 2 - 22
            width = text_width(edge_text, 16)
            tag = base(new_id("edge-label"), "text", mid_x - width / 2, mid_y, width, 20)
            tag.update(
                {
                    "text": edge_text,
                    "fontSize": 16,
                    "fontFamily": FONT_FAMILY,
                    "textAlign": "center",
                    "verticalAlign": "middle",
                    "originalText": edge_text,
                    "autoResize": True,
                    "lineHeight": 1.25,
                    "baseline": 14,
                    "containerId": None,
                }
            )
            elements.append(tag)

    return {
        "type": "excalidraw",
        "version": 2,
        "source": "https://excalidraw.com",
        "elements": elements,
        "appState": {"gridSize": None, "viewBackgroundColor": "#ffffff"},
        "files": {},
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Write a .excalidraw file from a scene JSON object.")
    parser.add_argument("scene", type=Path, help="Scene JSON with nodes and edges")
    parser.add_argument("-o", "--output", type=Path, required=True, help="Output .excalidraw path")
    args = parser.parse_args()
    try:
        scene = json.loads(args.scene.read_text(encoding="utf-8"))
        document = build(scene)
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(str(error), file=sys.stderr)
        return 2
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
