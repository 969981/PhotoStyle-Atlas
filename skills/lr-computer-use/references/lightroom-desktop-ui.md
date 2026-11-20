# Lightroom cloud desktop — UI reference

Target product: **Adobe Lightroom** (cloud-connected desktop app), not
Lightroom Classic. Classic uses Library/Develop modules and different panel
keyboard maps. Re-read on-screen labels each session; Adobe renames icons over time.

## Main regions

Typical layout:

- **Left / top**: navigation (All Photos, Albums, People, folders, search)
- **Center**: filmstrip / grid, or large preview in Edit
- **Right**: Edit tool sections when in Edit mode
- **Bottom or filmstrip**: adjacent photos (use carefully — easy to switch by accident)

## Modes

### Browse / Library

- Grid of thumbnails
- Filters, ratings, flags if enabled
- Double-click or Edit control to enter detail editing

### Edit

- Large preview
- Right rail of tool sections
- Local adjustments via Masking
- Presets browser often accessible from Edit

Confirm mode before adjusting. Crop tools behave differently from Light/Color sliders.

## Edit sections (common)

Order and icons vary. Identify by tooltip or expanded header text.

| Section | Typical controls | Used by |
| --- | --- | --- |
| Crop & Rotate | Aspect, angle, constrain, flip | `lr-composition` |
| Healing / Remove | Heal, clone, generative remove | only if asked |
| Masking | Subject, sky, background, objects, brush, linear, radial | `lr-lighting`, selective color |
| Light | Exposure, contrast, HL/SH, whites/blacks, curve, presence-related light | `lr-lighting` |
| Color | Temp, tint, vibrance, sat, B&W mix, color mixer, point color, color grading | `lr-color-grade` |
| Effects | Texture, clarity, dehaze, vignette, grain | optional finish in session |
| Detail | Sharpen, NR, color NR | out of core domain skills |
| Optics | Remove CA, enable lens corrections | optional |
| Geometry | Upright, guided upright, transform | `lr-composition` |
| Presets | Adobe / user / recommended | only if brief allows |

## Masking notes

Masks support local Exposure, Highlights, Shadows, Temp, Tint, etc.

Prefer:

1. Auto Subject / Sky when quality is good
2. Linear gradient for sky-to-ground or wall falloff
3. Brush for fixes auto-mask misses

Always check mask overlay on/off before heavy local edits.

## Histogram

When visible:

- Spikes hard left → deep blacks / possible crush
- Spikes hard right → highlight clip
- Use as a guide with the image; do not “perfect the histogram” at the cost of mood

## Before / after and history

- Toggle before/after when available to verify improvements
- History / versions: step back rather than zeroing all settings
- If a Version button exists, create one before aggressive experimental looks

## Presets

- Preview on hover when the UI supports it
- Prefer mild presets, then refine with Light + Color
- Do not stack many conflicting presets

## Common failure modes for Computer Use

1. **Clicked filmstrip** → switched photo mid-edit. Re-select target.
2. **Still in Browse** → sliders missing. Enter Edit.
3. **Mask still active** → global sliders may apply locally. Exit mask or intentionally edit mask.
4. **Collapsed section** → control not visible. Expand header.
5. **Dialog open** (export, delete, AI credit) → handle or cancel deliberately.
6. **Zoomed in** → misread global exposure. Fit-to-screen for overall judgment.

## Version differences

If a control from this doc is missing:

1. Search the Edit rail icons
2. Check under nested headers (Color may nest Color Grading)
3. Proceed with nearest equivalent; note the substitution in the edit receipt
