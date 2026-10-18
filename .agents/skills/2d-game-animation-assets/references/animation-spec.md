# Animation Spec Reference

## Planning Fields

Use this compact spec for each animation:

```text
name:
purpose:
style:
canvas:
frame_count:
fps:
loop:
pivot:
directions:
events:
export:
```

## Common Frame Counts

- Idle: 4-8 frames, 6-10 FPS, loop.
- Walk: 6-8 frames, 10-12 FPS, loop.
- Run: 6-8 frames, 12-16 FPS, loop.
- Jump start: 2-4 frames, 10-14 FPS, no loop.
- Fall: 2-4 frames, 8-12 FPS, loop or hold.
- Land: 2-4 frames, 10-14 FPS, no loop.
- Light attack: 5-8 frames, 12-18 FPS, no loop.
- Heavy attack: 7-12 frames, 10-16 FPS, no loop.
- Hit react: 3-6 frames, 10-14 FPS, no loop.
- Death: 8-16 frames, 8-12 FPS, no loop or hold last.
- Effect burst: 6-12 frames, 12-24 FPS, usually no loop.

## Manifest Shape

Prefer JSON manifests with this structure:

```json
{
  "asset": "hero",
  "animation": "walk",
  "fps": 12,
  "loop": true,
  "canvas": { "width": 128, "height": 128 },
  "pivot": { "x": 0.5, "y": 1.0 },
  "frames": [
    { "index": 0, "name": "hero_walk_000.png", "x": 0, "y": 0, "w": 128, "h": 128 }
  ],
  "events": []
}
```

Use normalized pivot coordinates where `(0, 0)` is top-left and `(1, 1)` is bottom-right unless the target engine requires a different convention. For Unity custom pivots, bottom-center is `(0.5, 0.0)` in Sprite Editor UI terms, but many JSON tools represent bottom-center as `(0.5, 1.0)` when origin is top-left; state the convention.

## Image-Generation Prompt Pattern

Include these constraints when generating frames:

```text
Create a transparent-background 2D game sprite animation sheet for [subject].
Style: [pixel art / clean hand-painted / anime / vector-like].
Camera: orthographic side view, no perspective shift.
Canvas: [width]x[height] per frame, [columns] columns by [rows] rows.
Animation: [name], [frame_count] frames at [fps] FPS.
Motion notes: [anticipation/contact/recovery or loop cycle].
Consistency: identical character design, outfit, proportions, palette, weapon size, lighting, and baseline in every frame.
Output: evenly spaced frames, transparent background, no shadows outside the canvas, no text labels.
```

## Quality Checks

- Scrub the animation at target FPS and half speed.
- Check feet or contact points for sliding unless intended.
- Check silhouette readability at in-game scale.
- Confirm every frame fits inside the same canvas without edge clipping.
- Confirm frame order is visible from filenames and manifest indices.
