# Quality contract

Judge the actual bitmap in this order. Apply evidence and authorship gates only when the image makes factual or experiential claims; apply subject, visual, text, and delivery gates to every output.

## Gate A — Subject integrity (blocking)

- The chosen subject remains recognisable at phone size.
- Landscape horizon, weather, spatial depth, and place-defining detail remain coherent.
- Portrait identity, expression, face geometry, pose, and protected features have not drifted.
- Object silhouette, material, function, label, and defining construction remain intact.
- Architecture preserves proportions, openings, perspective, verticals, and spatial logic.
- Restyled images change only the approved variables.
- No invented object, person, logo, jewellery, tattoo, product feature, building detail, or scene event appears.

## Gate B — Evidence and authorship integrity (blocking when relevant)

- Every objective number and quotation maps to `evidence.json`.
- Current facts use an appropriately current source.
- `inferred` and `subjective` claims are not written as verified facts.
- First-person experience appears only when the user supplied it.
- Recommendations state tradeoffs and fit rather than universal certainty.
- Hidden public citations do not mean discarded provenance.

## Gate C — Text integrity (blocking)

- Every visible string matches the approved prompt and outline exactly.
- Names, dates, places, values, units, and punctuation are correct.
- No pseudo-language, faux Japanese/Korean characters, fake archive codes, invented coordinates, or meaningless microtext appears.
- Text supports the image rather than filling space.
- Essential text remains readable and clear of platform overlay zones.
- If exact text is garbled, regenerate; never patch it with code.

## Gate D — Material craft

At full size, verify:

- the paper has nonuniform fibres, tonal drift, and believable absorption without a repeated digital-noise pattern
- one lead reproduction process explains image softness, grain, bleed, halftone, or plate offset
- the image is printed into the page rather than dropped on top as a clean digital rectangle
- edge behaviour is deliberate and physically plausible
- type feels printed and slightly fallible, not like a modern UI layer
- one chromatic signal remains clear without competing saturated hues
- texture supports hierarchy rather than masking weak composition

Reject random tape, coffee rings, repeated scratches, fake damage, decorative registration marks, and multiple unrelated print processes.

## Gate E — Composition and subject scale

Compare the image against its selected mode:

| Mode | Pass condition |
|---|---|
| `airy-fragment` | 72%-88% quiet paper; one meaningful 10%-24% image/type relation |
| `photo-window` | photo remains rewarding at 24%-45%; paper field still shapes the reading |
| `panorama-strip` | horizon or directional axis stays uninterrupted; strip occupies 18%-36% |
| `dual-frame` | two frames create one relation; together occupy 22%-42% |
| `specimen-plate` | object retains material and silhouette at 12%-34% |
| `portrait-archive` | face and expression survive phone size; portrait occupies 22%-44% |
| `type-object` | type is genuinely the subject; physical print character prevents campaign polish |

Ranges are perceptual review aids. A strong preserved edit may sit outside them. Do not force compliance by cropping away the subject.

At thumbnail size, verify:

- the subject or visual relation appears within one second
- the chromatic signal is visible but not dominant over everything else
- the paper does not collapse into muddy gray
- the image does not look like a generic beige quote template
- any required name or phrase remains legible

## Gate F — Authored-image test

Ask five questions:

1. Could this composition belong to any unrelated topic after swapping the title?
2. Is any symbol present only because zine prompts often contain it?
3. Does the empty space create direction, pause, scale, or emotional pressure?
4. Is every defect caused by the chosen reproduction process?
5. Would removing the atmospheric microtext make the image stronger?

If the first two answers are yes, or the final three expose weak choices, revise the art direction before adding more texture.

## Gate G — Series continuity

- Paper family, process, type pairing, hue logic, and texture intensity remain coherent.
- Composition modes vary according to card subject and story role.
- No more than two consecutive cards use the same mode or near-identical crop.
- Later images preserve the anchor's material character without copying its layout or factual text.
- A mixed-subject series still feels related at thumbnail size.

## Gate H — Platform and delivery (blocking)

- Aspect ratio, dimensions, safe zones, and ordered filenames are correct.
- A saved prompt exists for every selected image.
- Manifest points to final selected versions.
- Project-bound images live in `outputs/`, not only in a tool cache.
- Required caption, evidence, and outline files exist for series/evidence routes.
- Existing user files were not silently overwritten.

## Severity

| Severity | Meaning | Action |
|---|---|---|
| Error | subject drift, false claim, wrong text, wrong ratio, missing artifact, or unreproducible output | block and fix |
| Warning | weak scale, generic metaphor, borderline safe zone, visual drift, or uncertain source | review explicitly |
| Note | optional aesthetic refinement | deliver if accepted |

## Targeted regeneration

Change one failure class per retry:

- lost subject → restore protected structure and reduce the styling intervention
- subject too small → enlarge only the image-bearing area or choose a more generous mode
- generic template → strengthen the specific crop and image–signal relation; remove filler text
- bad texture → keep one process and remove generic grunge
- weak color signal → change its form or opacity without adding a second hue
- excessive density → remove secondary copy or split the card
- garbled text → shorten strings and regenerate
- series drift → restate paper, process, type, and hue invariants while retaining a different composition

Preserve every failed candidate with a version suffix for comparison.
