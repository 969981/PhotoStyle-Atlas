# White balance and color mixer

## White balance

### Temp

- Higher / warmer → yellow-orange
- Lower / cooler → blue

### Tint

- Magenta vs green axis
- Mixed LED/fluorescent often needs magenta or green correction

### Strategy

1. If a neutral reference exists (card, white shirt in shade, gray concrete), sample it.
2. If no neutral, set WB by skin or by known scene (shade is cooler; tungsten warmer).
3. Match series consistency when editing multiple related photos later.

### Intentional non-neutral WB

Allowed when the brief wants mood (golden hour warmth, night blue). State that WB is stylistic, not corrective.

## Vibrance vs saturation

| Control | Behavior | Prefer when |
| --- | --- | --- |
| Vibrance | Boosts weaker colors more; gentler on skin | Portraits, general polish |
| Saturation | Global boost of all colors | Graphics, already-flat RAW needing more life |

Push vibrance moderately before touching saturation. If colors clip or plasticize, reverse.

## Color mixer (HSL)

Per-color channels typically: Hue, Saturation, Luminance for Reds, Oranges, Yellows, Greens, Aquas, Blues, Purples, Magentas (set varies).

### Common fixes

| Issue | Mixer tendency |
| --- | --- |
| Skin too red | Oranges/reds sat down slightly; hue carefully |
| Foliage neon | Greens hue toward yellow or sat down; luminance as needed |
| Sky weak | Blues luminance / sat carefully; avoid banding |
| Water unwanted green | Aquas/greens hue toward blue |

### Point Color

When available:

1. Sample the problem color.
2. Adjust range/variance so only intended pixels move.
3. Nudge hue/sat/luma small amounts.
4. Check edges and skin for spill.

## Selective color via masks

For local color (e.g. cooler background only):

1. Create background or linear mask.
2. Adjust Temp/Tint or color controls on that mask.
3. Verify subject unchanged.

## Skin protection checklist

- Oranges/reds not oversaturated
- No green/magenta death cast on faces
- Eyes and teeth not neon from global sat
- Makeup colors still plausible
