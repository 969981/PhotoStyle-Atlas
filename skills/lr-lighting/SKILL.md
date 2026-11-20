---
name: lr-lighting
description: >
  Adjust exposure and tone in Adobe Lightroom cloud desktop via Computer Use:
  exposure, contrast, highlights, shadows, whites, blacks, curves, and light
  masks. Use when the user asks for "lighting", "exposure", "too dark", "too
  bright", "lift shadows", "recover highlights", "contrast", "tone", or "curves".
  Not for crop/composition, white balance/color grading as primary work, or export.
license: MIT
compatibility: >
  Requires ChatGPT Computer Use and Adobe Lightroom cloud desktop. Follow
  lr-computer-use base patterns.
metadata:
  author: photo-editing-computer-use
  version: "0.1.0"
  product: lightroom-cloud-desktop
---

# lr-lighting

Shape global and local **light/tone** in Lightroom cloud desktop with Computer Use.
Assume `lr-computer-use` loop and safety.

## Goal

Readable subject, controlled clipping, intentional contrast — matching the brief
(natural documentary vs punchy commercial) without plastic HDR.

## Preconditions

1. Lightroom frontmost; photo in **Edit**.
2. Prefer composition fixed first when both are requested (`lr-composition` / session order).
3. Exit unrelated tools (crop committed, healing closed) so Light sliders apply as intended.

## Workflow

### 1. Diagnose

Observe image + histogram if visible:

- Overall too dark / bright?
- Highlight clip (windows, sky, skin shine)?
- Shadow crush (lost detail in blacks)?
- Flat (needs contrast) vs already contrasty?
- Single subject vs high dynamic range scene?

Read `references/tone-controls.md` for control meanings and safe ranges.

### 2. Global light — fixed order

Open **Light** section. Adjust in this order unless the brief demands otherwise:

1. **Exposure** — set middle-tone brightness for the subject
2. **Highlights** — recover or tame bright areas
3. **Shadows** — open or deepen dark areas
4. **Whites** — set white point carefully (watch clip)
5. **Blacks** — set black point for depth
6. **Contrast** — refine mid-tone separation last among basics
7. **Curve** — only if basics cannot reach the look

Make small moves; re-observe after each cluster (Exposure alone, then HL/SH, then White/Black).

### 3. Presence-related light (optional)

If Texture / Clarity / Dehaze live under Light or Effects:

- Prefer **subtle** Clarity/Texture for subject pop
- Dehaze: small amounts for haze or mild sky punch; large amounts look fake
- Skip if the brief is soft / filmic / low-contrast

### 4. Local light masks

Use Masking when global fixes hurt other regions:

| Problem | Typical mask |
| --- | --- |
| Bright sky, dark land | Sky mask or linear gradient |
| Subject underexposed | Subject / people mask |
| Face slightly dark | Subject or brush on face |
| Window blast indoors | Highlights on window region or exposure down on windows |

Details: `references/local-light-masks.md`.

After local work: turn mask overlay off and judge the whole frame.

### 5. Style guardrails

| Brief | Bias |
| --- | --- |
| Natural / documentary | Mild Exposure/HL/SH; modest contrast |
| Bright airy | Lift Exposure/Shadows; protect skin highlights |
| Moody / dark | Lower Exposure; richer Blacks; protect subject eyes |
| High-impact social | Slightly punchier contrast; still avoid neon HDR |

Avoid:

- Maxed Shadows + maxed Highlights on everything (HDR glow)
- Crushed blacks that hide product detail the user cares about
- Blown skin speculars on portraits

### 6. Verify

1. Fit to screen; check subject first, then extremes.
2. Peek histogram for hard wall spikes.
3. Before/after toggle.
4. If skin exists, verify faces still natural.

## Do not

- Fix white balance here (use `lr-color-grade`) except tiny temp only if inseparable from exposure perception — prefer color skill
- Crop or geometry
- Export
- Batch-sync light settings unless user asked

## Completion

Report:

- Global changes (Exposure/HL/SH/Whites/Blacks/Contrast/Curve)
- Masks used and purpose
- Remaining issues (e.g. “sky still hot; needs color or crop”)
- Style intent matched

## Additional resources

- `references/tone-controls.md`
- `references/local-light-masks.md`
- Shared UI: `../lr-computer-use/references/lightroom-desktop-ui.md`
