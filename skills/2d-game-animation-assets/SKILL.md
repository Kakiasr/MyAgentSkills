---
name: 2d-game-animation-assets
description: Produce 2D game animation assets for browser games, Unity, Godot, or custom engines. Use when Codex needs to design, generate, normalize, pack, or document sprite animation assets such as frame sequences, sprite sheets, idle/walk/run/attack/death loops, effects animations, pixel-art or hand-painted 2D characters, animation manifests, pivots, collision boxes, import settings, or asset-production prompts for image generation.
---

# 2D Game Animation Assets

## Workflow

1. Clarify the target runtime and asset style only when missing and consequential: engine, resolution, pixel-art vs painted, frame size, directions, animation list, frame count, FPS, pivot, transparency, and export format.
2. Produce a compact animation plan before generating or editing assets. Include animation names, frame counts, loop mode, FPS, canvas size, anchor point, and gameplay notes.
3. Generate or edit source frames with consistent character scale, silhouette, lighting, palette, camera angle, and transparent background. Prefer full sprite strips or frame grids when consistency matters.
4. Normalize frames before delivery: equal canvas size, stable pivot, no crop jitter, consistent baseline, transparent padding, predictable filename order.
5. Pack frames into engine-ready outputs when requested. Use `scripts/pack_sprite_sheet.py` for existing PNG frame sequences.
6. Deliver import guidance and a manifest. For Unity work, read `references/unity-import.md` when import settings, slicing, pivots, animation clips, or Pixels Per Unit matter.

## Tool Dependencies

- Use Python 3 with `Pillow>=12.0,<13` for PNG generation, normalization, sheet packing, and manifest creation.
- Before running bundled image scripts, check dependencies with `scripts/ensure_tools.py`. If Pillow is missing, the script should create a local virtual environment and install requirements from `requirements.txt`.
- Prefer project-local tool environments when working inside a game repo: run `python3 <skill>/scripts/ensure_tools.py --venv ./Tools/2d-assets/.venv --requirements ./Tools/2d-assets/requirements.txt` when the project provides those files.
- If the project has no local requirements file, use the skill's bundled `requirements.txt` and keep the virtual environment outside shipped game assets, such as `.venv-2d-assets` or `Tools/2d-assets/.venv`.

## Asset Standards

- Keep every frame in an animation on the same canvas dimensions.
- Use transparent PNG for source frames and packed sheets unless the user asks for another format.
- Use deterministic names: `<character>_<animation>_<direction>_<frame>.png`, with zero-padded frame numbers.
- Preserve a stable pivot across all frames. Default to bottom-center for characters and center for effects unless gameplay implies another anchor.
- Avoid changing costume details, weapon length, face design, outlines, or color palette between frames.
- For pixel art, require integer scaling, no antialiasing on final frames, and a fixed palette unless the user asks otherwise.
- For combat animations, include anticipation, contact, follow-through, and recovery frames; mark the hit frame in the manifest.
- For loops, make the first and last frames compatible without duplicating the same pose unless the target tool requires it.

## References

- Read `references/animation-spec.md` when planning animation sets, frame counts, timing, naming, manifests, or image-generation prompts.
- Read `references/unity-import.md` when producing Unity-specific sprite sheets, slicing settings, pivots, animation clips, or importer instructions.

## Scripts

Use the script when the user provides existing PNG frames or when generated frames need packing:

```bash
PYTHON=$(python3 scripts/ensure_tools.py)
$PYTHON scripts/pack_sprite_sheet.py \
  --input frames \
  --output dist/hero_walk_sheet.png \
  --manifest dist/hero_walk_manifest.json \
  --columns 6 \
  --fps 12 \
  --animation hero_walk
```

If dependencies are already available in the active Python, this direct form also works:

```bash
python3 scripts/pack_sprite_sheet.py \
  --input frames \
  --output dist/hero_walk_sheet.png \
  --manifest dist/hero_walk_manifest.json \
  --columns 6 \
  --fps 12 \
  --animation hero_walk
```

The script creates a uniform grid sprite sheet and JSON manifest with frame rectangles, pivot, FPS, and loop metadata.

## Delivery Checklist

For finished asset work, include:

- Output paths for frames, sprite sheets, and manifest files.
- Animation list with frame count, FPS, loop mode, and gameplay events.
- Engine import notes, especially pivot and Pixels Per Unit for Unity.
- Any limits or assumptions, such as generated concept frames needing art-director approval before final cleanup.
