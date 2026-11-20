# Edit session playbook

## Intake template

Fill mentally (or in notes) before touching sliders:

```text
Photo: <filename or visual description>
Intent: natural | warm golden | cool cinematic | airy | moody | product | other
Crop: allowed | locked | aspect=…
Must keep: …
Avoid: …
Reference: …
```

### Default when underspecified

```text
Intent: natural documentary polish
Crop: allowed mild straighten + improve if obvious
Color: accurate WB, subtle vibrance, no heavy grade
Effects: none unless needed
Export: no
```

## Time-box mindset

Computer Use is slow compared to native presets. Prefer:

1. Biggest visual wins first (level, exposure, WB)
2. One local mask only if global fails
3. Subtle grade over complex wheel choreography
4. Stop when the brief is met

## Hero edit then match (future batch)

If user later wants a series:

1. Finish hero with receipt
2. Copy settings / sync only the panels used
3. Spot-check each target for skin and sky failures

Not automated in v1 skills beyond describing the approach.

## Edit receipt format

Use this structure in the final user-facing reply:

```markdown
## Edit receipt

**Photo:** …
**Intent:** …
**Computer Use:** Lightroom focused; Edit mode

### Composition
- …
### Lighting
- …
### Color
- …
### Finish
- … (or none)

### Verification
- Before/after checked: yes/no
- Issues remaining: …

### Not done
- Export / share / batch: …

### Next steps (optional)
- …
```

## Example prompts → behavior

| Prompt | Behavior |
| --- | --- |
| “Full pass, natural look” | Full pipeline, documentary bias |
| “Cinematic grade, already cropped” | Skip composition unless crooked; light then teal-orange-subtle |
| “Just brighten the face” | Lighting + subject mask; skip grade if color OK |
| “4:5 for Instagram, warm” | Composition aspect 4:5 → light → warm golden color |
| “Export JPEG to Desktop” | Complete edit if needed, **confirm**, then export UI only with user approval |

## Regression checklist

Before closing the session:

- [ ] Correct photo still selected
- [ ] Horizon acceptable
- [ ] Subject exposure OK
- [ ] Skin/product color OK
- [ ] No accidental mask left mis-editing globals
- [ ] No export/delete performed unless requested
