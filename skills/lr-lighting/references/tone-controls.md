# Tone controls reference

## Basic light sliders

| Control | Role | Practical notes |
| --- | --- | --- |
| Exposure | Overall brightness (biased to mids) | Set subject first; do not chase background |
| Contrast | Mid-tone separation | After HL/SH often safer |
| Highlights | Bright region compression/expansion | Recover skies, white shirts, windows |
| Shadows | Dark region open/close | Lift for detail; too far = haze/noise |
| Whites | White point / brightest stop | Fine clip control; small moves |
| Blacks | Black point / deepest stop | Add depth; watch for crushed detail |

## Suggested starting magnitudes

For Computer Use, prefer incremental nudges rather than end-stops:

- Exposure: ±0.10 to ±0.35 EV-style steps visually; reassess often
- Highlights / Shadows: start ~10–25 points of the visible slider range; increase only if needed
- Whites / Blacks: smaller than Shadows/Highlights typically
- Contrast: mild unless commercial punch requested

Exact numeric scales differ by Lightroom version; **trust the image**, not a fixed number.

## Curve

Use parametric or point curve when:

- Basics cannot add mid contrast without clipping
- Need soft matte blacks (lift black point slightly on RGB curve)
- Need gentle S-curve for polish

Procedure:

1. Open Curve in Light.
2. Prefer mild S: slight down on shadows, slight up on highlights — or inverse for flat film.
3. Avoid extreme anchors that posterize gradients (skies, skin).

## Histogram reading

- Touching right edge hard → likely highlight clip; pull Highlights/Whites/Exposure
- Touching left edge hard → black clip; lift Shadows/Blacks or Exposure if overall dark
- Gap on both ends → low contrast; may need Contrast/curve or accept flat style
- Color channel spikes → may be color issue; hand off to color skill if cast-driven

## Auto tone

Auto (if present) can be a **starting point** only:

1. Try Auto if the file is far off.
2. Immediately refine manually.
3. Never accept Auto without visual check — it often over-lifts shadows.

## Order rationale

Exposure first centers the subject. Highlights/Shadows recover range.
Whites/Blacks set endpoints. Contrast/curve refine character. Local masks
fix regional conflicts last so globals stay simpler.
