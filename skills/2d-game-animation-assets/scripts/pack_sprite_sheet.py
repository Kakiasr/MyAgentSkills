#!/usr/bin/env python3
import argparse
import json
import math
from pathlib import Path

try:
    from PIL import Image
except ImportError as exc:
    raise SystemExit("Pillow is required. Install with: python3 -m pip install Pillow") from exc


def parse_pivot(value):
    parts = value.split(",")
    if len(parts) != 2:
        raise argparse.ArgumentTypeError("pivot must be formatted as x,y")
    x, y = (float(part.strip()) for part in parts)
    if not (0 <= x <= 1 and 0 <= y <= 1):
        raise argparse.ArgumentTypeError("pivot values must be between 0 and 1")
    return {"x": x, "y": y, "convention": "top-left-origin-normalized"}


def collect_frames(input_dir):
    frames = sorted(
        path for path in Path(input_dir).iterdir()
        if path.is_file() and path.suffix.lower() == ".png"
    )
    if not frames:
        raise SystemExit(f"No PNG frames found in {input_dir}")
    return frames


def main():
    parser = argparse.ArgumentParser(description="Pack uniform PNG frames into a sprite sheet and manifest.")
    parser.add_argument("--input", required=True, help="Directory containing ordered PNG frames.")
    parser.add_argument("--output", required=True, help="Output sprite sheet PNG path.")
    parser.add_argument("--manifest", required=True, help="Output JSON manifest path.")
    parser.add_argument("--columns", type=int, default=0, help="Grid columns. Defaults to ceil(sqrt(frame_count)).")
    parser.add_argument("--fps", type=int, default=12, help="Animation FPS.")
    parser.add_argument("--animation", default="animation", help="Animation name for the manifest.")
    parser.add_argument("--asset", default="", help="Asset or character name for the manifest.")
    parser.add_argument("--loop", action=argparse.BooleanOptionalAction, default=True, help="Whether the animation loops.")
    parser.add_argument("--pivot", type=parse_pivot, default=parse_pivot("0.5,1.0"), help="Normalized pivot x,y using top-left origin.")
    args = parser.parse_args()

    frame_paths = collect_frames(args.input)
    images = [Image.open(path).convert("RGBA") for path in frame_paths]
    width = max(image.width for image in images)
    height = max(image.height for image in images)
    columns = args.columns or math.ceil(math.sqrt(len(images)))
    if columns <= 0:
        raise SystemExit("--columns must be greater than 0")
    rows = math.ceil(len(images) / columns)

    sheet = Image.new("RGBA", (columns * width, rows * height), (0, 0, 0, 0))
    manifest_frames = []

    for index, (path, image) in enumerate(zip(frame_paths, images)):
        col = index % columns
        row = index // columns
        x = col * width
        y = row * height
        offset_x = (width - image.width) // 2
        offset_y = height - image.height
        sheet.alpha_composite(image, (x + offset_x, y + offset_y))
        manifest_frames.append({
            "index": index,
            "name": path.name,
            "x": x,
            "y": y,
            "w": width,
            "h": height
        })

    output_path = Path(args.output)
    manifest_path = Path(args.manifest)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output_path)

    manifest = {
        "asset": args.asset or Path(args.input).name,
        "animation": args.animation,
        "fps": args.fps,
        "loop": args.loop,
        "canvas": {"width": width, "height": height},
        "sheet": {
            "path": str(output_path),
            "columns": columns,
            "rows": rows,
            "width": sheet.width,
            "height": sheet.height
        },
        "pivot": args.pivot,
        "frames": manifest_frames,
        "events": []
    }
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"Packed {len(images)} frames into {output_path}")
    print(f"Wrote manifest to {manifest_path}")


if __name__ == "__main__":
    main()
