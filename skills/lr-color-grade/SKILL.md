---
name: lr-color-grade
description: >
  Color and look work in Adobe Lightroom cloud desktop via Computer Use: white
  balance, vibrance/saturation, color mixer / point color, and color grading
  wheels. Use when the user asks to "grade", "color grade", "white balance",
  "warm it up", "cool it down", "teal and orange", "vibrance", "saturation",
  "color mixer", or "cinematic look". Not for crop, primary exposure recovery,
  healing, or export.
license: MIT
compatibility: >
  Requires ChatGPT Computer Use and Adobe Lightroom cloud desktop. Follow
  lr-computer-use base patterns.
metadata:
  author: photo-editing-computer-use
  version: "0.1.0"
  product: lightroom-cloud-desktop
---

# lr-color-grade

Shape **color and photographic look** in Lightroom cloud desktop with Computer Use.
Assume `lr-computer-use` loop and safety. Prefer tone roughly set first
(`lr-lighting`) when both are in scope.

## Goal

Believable white balance, controlled saturation, intentional grade — matching
the brief while protecting skin and product colors.

## Preconditions

1. Lightroom frontmost; photo in **Edit**.
2. Open **Color** section (and nested Color Grading / Mixer as needed).
3. Exit crop/healing; clear mask selection unless doing selective color.

## Workflow

### 1. Diagnose color

Observe:

- Cast (yellow tungsten, green mixed, blue shade, magenta LED)
- Skin present? Product brand colors must stay accurate?
- Saturation already high (phone JPEG / Instagram-ready)?
- Desired look words: natural, warm sunset, cool cinematic, pastel, faded film, vibrant travel

### 2. White balance first

1. Set **Temp** and **Tint** for a plausible neutral on neutral surfaces *or* for intentional mood if brief wants warmth/coolness overall.
2. Use WB eyedropper on neutral gray/white when available and trustworthy.
3. For skin: err slightly warm rather than corpse-green/magenta.

Details: `references/white-balance-and-mixer.md`.

### 3. Global saturation controls

- **Vibrance** first (gentler on skin)
- **Saturation** second, sparingly
- Avoid double-max vibrance + saturation

### 4. Mixer / Point Color (optional)

Use when:

- One hue is wrong (sick neon greens, muddy oranges)
- Sky/foliage needs separation
- Brand color needs a nudge without full regrade

Prefer small HSL moves. Point Color / variance tools: adjust target hue carefully; verify no bleeding into skin.

### 5. Color Grading wheels

Open **Color Grading** (shadows / midtones / highlights / global / blending / balance).

Principles:

- Start **subtle** — if you only notice it in a blind A/B, good; if it screams, pull back
- Shadows often cooler or complementary; highlights warmer (classic) — invert only intentionally
- Use midtones for skin-affecting mood with extreme care
- Blending/balance: refine separation; do not hide a bad grade

Look recipes: `references/grading-looks.md`.

### 6. B&W

Convert to black and white **only if requested**. Then use B&W mixer for channel contrast, not Color Grading rainbow.

### 7. Verify

1. Faces / brand colors first.
2. Skies and foliage second.
3. Before/after.
4. Check for posterization / banding in gradients after heavy grade.

## Style guardrails

| Brief | Approach |
| --- | --- |
| Natural documentary | WB correct; vibrance slight; skip heavy wheels |
| Warm golden | WB warmer; mild warm highlights; restrained sat |
| Cool cinematic | Slightly cool WB or cool shadows; teal-leaning shadows, warm highlights carefully |
| Faded film | Mild grade + slightly lifted blacks via lighting skill; lower contrast |
| Vibrant travel | Vibrance up; selective mixer; avoid clown skin |

## Do not

- Use grade to fix severe underexposure (return to `lr-lighting`)
- Nuke skin orange or magenta
- Apply stacked presets + heavy wheels without checking
- Export

## Completion

Report:

- WB intent (neutral vs warm/cool)
- Vibrance/saturation changes
- Mixer / point color targets
- Grading recipe used (shadows/mids/highlights)
- Skin/product risk notes

## Additional resources

- `references/white-balance-and-mixer.md`
- `references/grading-looks.md`
- Shared UI: `../lr-computer-use/references/lightroom-desktop-ui.md`
