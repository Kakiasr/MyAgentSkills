# Unity Import Reference

## Recommended Sprite Settings

- Texture Type: Sprite (2D and UI)
- Sprite Mode: Multiple for sprite sheets, Single for individual frames
- Mesh Type: Full Rect for predictable pivots, Tight only when overdraw matters and pivots are verified
- Alpha Is Transparency: enabled for PNG sprites
- Filter Mode: Point for pixel art, Bilinear for painted art
- Compression: None for pixel art or source review, Normal Quality for production painted art after visual QA
- Pixels Per Unit: choose from design scale; common values are 16, 32, 64, or 100

## Pivots

Use bottom-center for characters that stand on ground. Use center for projectiles, UI effects, and radial bursts. Keep the same pivot for every frame in one character set.

Unity Sprite Editor custom pivot uses normalized coordinates where bottom-left is `(0, 0)` and top-right is `(1, 1)`. Bottom-center is `(0.5, 0.0)`.

## Slicing

For uniform sheets, use Grid By Cell Size:

1. Set Cell Size to the per-frame canvas size.
2. Set Offset to `0, 0` unless the sheet has an intentional margin.
3. Set Padding to `0, 0` unless the packing script or atlas uses gutters.
4. Apply the same pivot to all slices.

## Animation Clips

Create one Animation Clip per action and direction:

```text
hero_idle_right.anim
hero_walk_right.anim
hero_attack_right.anim
hero_death_right.anim
```

Set clip sample rate to the requested FPS. Enable Loop Time only for looping actions such as idle, walk, run, fly, or aura effects.

## Delivery Notes

When delivering Unity-ready assets, include:

- Sprite sheet path and cell size.
- Pixels Per Unit recommendation.
- Pivot value in Unity coordinates.
- Clip names, FPS, and loop settings.
- Gameplay event frame indices, such as attack hit frame or footstep frames.
