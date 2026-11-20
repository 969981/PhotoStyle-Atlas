---
name: lr-composition
description: >
  Reframe photos in Adobe Lightroom cloud desktop via Computer Use: crop,
  straighten, aspect ratio, horizon, subject placement, and geometry/perspective.
  Use when the user asks to "compose", "crop", "straighten", "reframe", "rule of
  thirds", "fix horizon", "aspect ratio", or "geometry". Not for exposure,
  white balance, color grading, healing, or export.
license: MIT
compatibility: >
  Requires ChatGPT Computer Use and Adobe Lightroom cloud desktop. Follow
  lr-computer-use base patterns.
metadata:
  author: photo-editing-computer-use
  version: "0.1.0"
  product: lightroom-cloud-desktop
---

# lr-composition

Improve framing and geometry in **Lightroom cloud desktop** using Computer Use.
Assume `lr-computer-use` safety, observe→act→verify loop, and UI map.

## Goal

Deliver a stronger frame: level horizons, intentional aspect ratio, balanced
subject placement, corrected keystone when needed — without cutting critical
content the brief requires.

## Preconditions

1. Computer Use active; Lightroom frontmost and allowed.
2. Target photo selected; **Edit** mode open.
3. Confirm no active mask unless intentionally transforming a masked workflow (normally global crop).

## Workflow

### 1. Read the image

Observe:

- Subject(s) and primary story
- Horizon / verticals (buildings, trees, poles)
- Distracting edges (half objects, bright corners)
- Existing crop / aspect (square, 4:5, 16:9, free)
- User constraints (“no crop”, “keep full body”, “Instagram 4:5”, “level only”)

If the frame is already strong and level, **skip crop** and report that.

### 2. Straighten first

1. Open **Crop & Rotate** (or equivalent).
2. Use angle control / straighten tool / auto-straighten when available.
3. Align horizon or dominant verticals — pick one priority (usually horizon for landscapes; verticals for architecture).
4. Verify edges still hold essential content.

Details: `references/crop-and-geometry.md`.

### 3. Choose aspect ratio

| Brief | Prefer |
| --- | --- |
| Social portrait feed | 4:5 |
| Stories / reels cover | 9:16 (only if content supports) |
| Landscape / YouTube | 16:9 |
| Print classic | 3:2 or 4:3 |
| Unspecified | Keep native or mild free crop |

Lock aspect when the user specified one. Avoid extreme crops that destroy resolution without reason.

### 4. Place the subject

Use heuristics as **aids**, not laws — see `references/composition-heuristics.md`.

Default moves:

- Give the subject looking-room / walking-room in the direction of gaze/motion
- Reduce empty boredom only if it competes with the story
- Pull edges off amputated joints (cut mid-joint is worse than cleanly above joint)
- Keep key text/faces away from extreme corners after crop

Make **one** crop adjustment cluster, then re-observe full-frame at fit zoom.

### 5. Geometry / perspective (when needed)

Open **Geometry** (or Upright / Transform) when:

- Buildings lean unnaturally
- Wide-angle keystone distracts
- User asked to “fix perspective”

Prefer mild upright modes over aggressive full warp. Check for stretched faces and cut corners after transform; re-crop if needed.

### 6. Verify

1. Fit image to screen.
2. Check horizon/verticals.
3. Check subject integrity (faces, hands, product edges).
4. Toggle before/after if available.
5. Exit crop tool to confirm the applied crop (some UIs require Done/Enter).

## Do not

- Crop into a different photo via filmstrip misclick
- Apply geometry so hard that faces look melted
- Change exposure/color here (hand off to `lr-lighting` / `lr-color-grade`)
- Export the crop result unless asked

## Completion

Report:

- Aspect ratio used
- Straighten amount / intent (horizon vs verticals)
- Composition intent (e.g. “subject on right third, more sky”)
- Geometry tools used
- Content lost at edges (if any)

## Additional resources

- `references/crop-and-geometry.md`
- `references/composition-heuristics.md`
- Shared UI/safety: `../lr-computer-use/references/lightroom-desktop-ui.md`
