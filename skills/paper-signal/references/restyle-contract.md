# Restyle contract

Restyling changes the material and editorial reading of an image while preserving its semantic and visual identity.

## Classify every input

Label each image as:

- `edit-target` — preserve its subject and change only approved treatment
- `style-reference` — extract paper, process, type, color, and spacing traits only
- `content-reference` — use facts or object details, not appearance
- `series-anchor` — maintain material continuity across new images

Do not assume an attachment is the edit target. Inspect local edit targets with `view_image` before prompting.

## Build a preservation record

Record:

- subject route and exact subject identity
- aspect ratio and protected crop
- horizon, eye line, pose, silhouette, or architectural axis
- expression, hands, clothing, materials, labels, and defining details
- exact visible text, values, units, and item order
- light direction, dominant colors, and scene-defining background features
- elements the user likes and defects they want removed

These become prompt invariants, not optional notes.

## Choose transformation depth

Use the least invasive level that satisfies the request:

1. `reframe` — preserve the image; change crop, paper field, and surrounding type.
2. `print-transfer` — preserve subject and geometry; convert the surface to xerox, riso, halftone, cyanotype, letterpress-like type, or faded print.
3. `editorial-composite` — preserve subject identity; introduce one related frame, clipping, or paper-color relation.
4. `scene-transform` — alter weather, time, setting, clothing, or objects only when explicitly requested.

Do not use generative scene transformation when a print transfer is enough.

## Invariants

Unless the user explicitly changes them, keep:

- identity, wording, spelling, numbers, units, and ordering
- horizon, pose, expression, object silhouette, building geometry, and essential crop
- product marks and labels exactly as supplied; do not invent replacements
- card role, aspect ratio, and semantic relationships
- chart/comparison meaning when data is present
- user-approved visual elements

Change only:

- crop or framing within the preservation record
- paper and reproduction treatment
- sparse type character and hierarchy
- one anchor hue and its physical form
- explicitly requested content corrections

## Restyle prompt clause

Repeat the following meaning on every generation and correction:

```text
Treat the supplied image as the edit target. Change only the approved Paper Signal art direction: crop framing, paper integration, one reproduction process, sparse typography, and one single-ink intervention. Keep all approved text, values, item order, subject identity, face or scene geometry, defining details, aspect ratio, and semantic relationships unchanged. Do not redesign, replace, beautify, or add to the subject. Do not add claims, logos, decorative icons, pseudo-text, faux Asian characters, or invented metadata.
```

Add subject-specific preservation clauses from `subject-routing.md`.

## Photo-to-zine strategies

- **Window:** place the preserved photo in a 24%-45% paper window with one physically softened edge.
- **Strip:** crop landscape or architecture into an 18%-36% directional strip while preserving its horizon or axis.
- **Archive portrait:** keep the face at phone-readable scale and move type outside protected facial regions.
- **Specimen:** isolate an object only when its edge can remain honest and materially believable.
- **Dual frame:** pair context and detail, or original crop and tonal echo, without changing meaning.
- **Partial plate:** convert one meaningful region—sky, garment, window, shadow, vegetation, reflection—into the single saturated ink.

## Series conversion

When converting several images:

1. audit each preservation record
2. approve one representative image as the material anchor
3. restyle later images against that anchor, not against inconsistent old styles
4. route each card's subject separately and vary composition mode
5. keep paper, process, type, hue logic, and texture intensity fixed
6. save versioned siblings; never destroy originals

## Text correction

OCR may flag possible errors but is not an authority. Compare text against supplied copy, outline, and evidence. If generated text is wrong, regenerate rather than covering it programmatically.
