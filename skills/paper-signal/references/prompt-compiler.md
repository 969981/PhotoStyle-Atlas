# Subject-aware prompt compiler

Save exactly the prompt passed to the raster model. Keep planning metadata, source paths, checklists, and explanations in `manifest.json` or the surrounding project—not in the prompt file.

## Compile in this order

1. Select the delivery route and subject route.
2. Select one composition mode from `subject-routing.md`.
3. Select one material preset and one lead reproduction process.
4. Write a one-sentence visual thesis: `subject / action or state / emotional tension`.
5. Decide whether visible text adds meaning. Use no text when it does not.
6. Compile four compact paragraphs.

## Four-paragraph shape

### Paragraph 1 — canvas, paper, and attention geometry

State:

- exact aspect ratio and intended use
- full-frame paper surface; no border or mockup
- selected composition mode
- perceptual paper and image-area ranges appropriate to that mode
- decisive image position, crop direction, and safe zones
- protected horizon, pose, face, object silhouette, or architectural axis when relevant

Do not default to `80% paper and an 18% central cluster` for every subject. A `photo-window`, `portrait-archive`, or `panorama-strip` should be large enough to carry its content.

### Paragraph 2 — subject and physical image treatment

Describe one imageable relation and the features that must stay recognisable.

- landscape: horizon, weather, depth, and one place-defining detail
- portrait: identity, expression, pose, skin tone, and protected facial features
- object: silhouette, material, scale, and functional details
- architecture: proportions, openings, verticals, perspective, and light logic
- concept: one noun, one action, and one tension
- evidence: exact values and the physical relation that carries them

Choose one lead process: photocopy, risograph, newsprint halftone, letterpress, cyanotype/single-ink photo, or faded film print. Name only defects caused by that process.

### Paragraph 3 — type and chromatic signal

State:

- every exact visible string in quotation marks, or explicitly require no visible text
- type role, scale, and relation to the image
- one saturated hue, its physical form, and its approximate area range for the selected composition mode
- one or two coherent print defects
- no added letters, fake metadata, pseudo-language, logo, or watermark

Prefer zero to three short exact strings. Real place, date, weather, course, product, and measurement information must come from the user or evidence ledger.

### Paragraph 4 — emotional temperature and hard avoids

Require a flat, matte, printed or scanned image with a specific emotional temperature. Reject the most likely failure mode for the subject plus the global failures:

- generic clean beige poster or Swiss-template spacing
- full-bleed stock-photo or glossy campaign treatment
- random grunge, tape, coffee stains, decorative archive codes, or faux Asian text
- dashboard, UI cards, infographic grid, or corporate comparison columns
- waxy face, identity drift, impossible hands, warped architecture, or invented object features
- 3D depth, cinematic lens effects, neon, cute illustration, logo, CTA, watermark, or extra text

## Edit-preservation clause

For `restyle-existing`, include this meaning in paragraphs 1 and 2 of every prompt:

```text
Treat the supplied image as the edit target. Change only crop framing, paper integration, reproduction process, sparse typography, and the specified single-ink intervention. Preserve the subject identity, scene geometry, horizon or pose, defining details, approved text, values, aspect ratio, and semantic relationships. Do not replace or redesign the subject.
```

Strengthen the clause with subject-specific invariants from `subject-routing.md`. Repeat the invariants on correction prompts.

## Reference-image clause

Label every supplied image by role:

- `edit target`: preserve its protected content
- `style reference only`: extract paper, process, type character, and color logic; do not copy subject, wording, signature, or exact composition
- `content reference`: use its facts or object details, not its aesthetic
- `series anchor`: preserve material system; vary composition and factual content

Do not use a style reference as permission to imitate a living artist or reproduce a copyrighted image.

## Data without dashboard aesthetics

Select one decision-worthy signal per image and embody it as printed matter.

- split → two adjacent photo/paper fragments
- count → specimen label or repeated impression
- trend → three uneven printed strips or sequential crops
- ranking → one selected row or marked specimen
- comparison → paired frames joined by a seam

Keep exact labels and units. Put the explanation in the caption. A number may become prominent only in `type-object`, and only when the number itself is the subject.

## Correction prompts

Correct one failure class at a time and preserve all accepted details.

- subject too small → move to a more generous composition mode or enlarge only the image-bearing area
- subject drift → restate protected identity, crop, horizon, silhouette, or spatial geometry
- generic beige design → strengthen the image–signal relation and physical print process; remove decorative text
- too clean → add process-specific edge softness, ink absorption, fibre interaction, or plate offset; do not add random dirt
- too scrapbook-like → remove tape, labels, extra fragments, and competing defects
- too muted → preserve quiet paper while restoring the single hue as an opaque plate, crop, seam, or object region
- too dense → remove secondary text and move it to the caption
- garbled text → shorten or remove strings and regenerate to a versioned output

## Example — new landscape poster

```text
Tall 3:5 editorial poster, a flat scan of pale stone-gray uncoated paper with fine fibres, uneven absorption and one faint vertical fold. Use panorama-strip composition: about 66% of the page remains quiet directional paper, while a horizontal coastal image strip occupies about 28% across the lower-middle, well clear of every edge. Keep the horizon continuous and slightly below the strip centre.

Show Edinburgh after rain as one authored photographic fragment: dark wet stone, a distant slate skyline, low cloud and a single warm window reflected on the road. Preserve believable depth and place; crop decisively rather than showing a complete postcard view. Print the scene as a soft cyanotype/newsprint hybrid led by one deep-blue photo plate, with paper highlights showing through, gentle dot gain and one dissolved toner edge.

Render only "AFTER THE RAIN" and "EDINBURGH / 18:42", exactly spelled, in small old-book serif and restrained typewriter lettering beside the strip, never over the skyline. Use one opaque vermilion-red window reflection occupying about 2.5% of the whole canvas; no other saturated hue. Mild ink absorption and a one-millimetre plate offset only. No invented coordinates, pseudo-text, signature, logo or watermark.

Quiet, damp, observant and memory-like; matte paper, low-to-medium contrast, flat orthographic scan. No generic beige template, postcard saturation, giant headline, arbitrary bird or moon, stock-photo polish, dashboard, collage clutter, tape, coffee stains, fake Japanese/Korean text, glossy mockup, 3D depth, cinematic lens effects, neon, CTA or extra text.
```

## Example — portrait restyle

```text
Preserve the supplied 3:4 portrait as the edit target and keep its aspect ratio. Reframe it as a portrait-archive page on soft bone copier stock: about 58% quiet paper and a single portrait window occupying about 36% slightly left of centre. Preserve the original head size, eye line, expression, pose, hairline and crop; keep type outside the eyes and mouth.

Keep the person's identity, facial geometry, skin tone, clothing, hands and background-defining detail unchanged. Convert only the photographic surface into a carbon-rich soft photocopy with fine newsprint dots, paper highlights, restrained toner bloom and one naturally softened edge. Do not beautify, regenerate the face or invent accessories.

Render only the supplied name, exactly spelled, as a small serif line beside the cheek-level image edge; if no name was supplied, use no visible text. Add one opaque cobalt paper crop behind a narrow garment region, about 5% of the canvas, with a slight plate offset. No added letters, archive codes, dates, logo or watermark.

Intimate, documentary and quiet; flat matte scanned page with clear facial readability at phone size. No waxy skin, sharpened eyes, identity drift, fashion-campaign lighting, text across the face, generic grunge, glossy mockup, clean corporate poster, 3D depth, neon, CTA or extra text.
```
