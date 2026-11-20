# Local light masks

## When global is enough

Skip masks if one Exposure/HL/SH pass fixes the frame without harming key areas.

## When to mask

- Sky needs different exposure than foreground
- Subject face darker than background (or reverse)
- Interior + bright window
- Product needs lift without washing the backdrop

## Mask types (prefer order)

1. **Select Subject / People** — portraits, product-in-hand, heroes
2. **Select Sky** — landscapes, travel
3. **Background** — isolate subject by inverse
4. **Linear gradient** — gradual sky or wall falloff
5. **Radial** — soft vignette-like light on subject
6. **Brush** — cleanup misses; use feathered edges

## Local light adjustments

On a mask, prefer:

- Exposure, Highlights, Shadows first
- Whites/Blacks sparingly
- Contrast only if the region needs it
- Clarity/Texture lightly on subject if appropriate

Avoid heavy local Dehaze on faces.

## Overlay discipline

1. Enable mask overlay to verify coverage.
2. Subtract/add with brush if hair, edges, or product boundaries fail.
3. Disable overlay before final judgment.

## Common mistakes

| Mistake | Fix |
| --- | --- |
| Forgot mask active → thought globals broken | Exit mask; re-check global Light panel |
| Harsh mask edge | Feather / increase refinement; avoid hard brush |
| Sky mask eats buildings | Subtract buildings from sky mask |
| Subject mask includes bright window | Subtract window; treat window separately |
| Too many overlapping masks | Simplify; merge intent into fewer masks |

## Performance / Computer Use tips

- Create one mask, adjust, verify, then next mask
- Do not build five masks before looking at results
- Name-level awareness: if UI shows mask list, select the correct one before dragging sliders
