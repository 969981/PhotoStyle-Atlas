---
name: photo-to-minimal-editorial-poster
description: >-
  Turn one or more photographs into a consistent series of separate 3:4
  minimalist editorial posters: a strictly faithful top photographic region
  over a source-specific minimal abstract composition. The lower region
  reinterprets the subject's most recognizable contours and structures as
  clean geometric forms, flat color fields, fine lines, and generous negative
  space — abstract yet instantly recognizable, with a palette extracted from
  the source photo. Ivory background, generous margins, balanced central
  composition. No added text or decoration: photo-native text is preserved,
  and recognizable cultural text (dates, mottos, place names, slogans) may be
  carried into the abstract region anchored to its structure at its original
  relative position, never recomposed as separate typography. The overall
  direction is high-end minimal editorial design, contemporary art-exhibition
  and architectural graphic feel, understated luxury, museum-level art
  direction, and wide negative space.
license: MIT
metadata:
  author: SARSfang
  version: "1.3.0"
---
# Photo to Minimal Editorial Poster

Create one standalone poster per source photograph with the locked `ivory-editorial-v1` house style. The poster pairs a strictly faithful photographic region (top half) with a minimal abstract composition (bottom half) that distills the subject's most recognizable forms into a clean, geometric, reductive visual statement. The overall feeling is that of a high-end editorial or museum-exhibition poster — quiet, precise, spacious, and considered.

This requires visual input and an image-generation or image-editing capability that can use the source photograph directly; otherwise use the defined fallback. Different conversations do not share hidden series memory: use the default preset or an explicit series lock. Keep reusable series rules separate from each poster's source-specific manifest.

## Load the style contract

Before every generation:

1. Read [references/style-presets.md](references/style-presets.md). This is mandatory, not conditional.
2. Read [references/series-lock.md](references/series-lock.md). If the user supplies state, identify it by `document_type`; migrate a legacy lock before continuing. Otherwise start from [assets/series-lock.template.yaml](assets/series-lock.template.yaml).
3. Read [references/poster-design-rules.md](references/poster-design-rules.md) for source-specific abstraction method, palette, element selection, prompt construction, and quality review.
4. Create one [assets/poster-manifest.template.yaml](assets/poster-manifest.template.yaml) copy per source photo. Never reuse another photo's resolved values.

Do not claim to remember a custom series from another conversation. To continue a customized series in a new conversation, the user must provide its lock; without one, use `ivory-editorial-v1`.

## Preserve these invariants

- One source photo produces one poster. Never combine source photos.

- The canvas is 1080 × 1440 or the same 3:4 ratio.

- The layout is a strictly equal top-photo / bottom-abstract split at exactly 50:50 — both regions have the exact same height. No tolerance.

- The photographic region fills the entire top region edge-to-edge at a 3:2 landscape ratio. All source aspect ratios (16:9, 4:3, 3:2, 1:1, portrait, etc.) are handled by cropping to 3:2. The 50:50 split is non-negotiable.

- Portrait sources never use a left-right poster layout. Automatically select their strongest subject-preserving 3:2 horizontal crop without asking for a crop position.

- The photographic region must remain exactly as in the source — no filters, color grading, stylization, retouching, or compositing of any kind. Only cropping is allowed.

- Content-aware cropping is subject-focused: it may reduce surrounding scene and background to achieve the exact 3:2 ratio while protecting the primary subject and identity information.

- Preserve subject identity, proportions, perspective, materials, light, shadows, and important spatial relationships. Never stretch, rotate, or synthesize a replacement subject.

- Distill the subject into 4 to 7 abstract elements: 3 mandatory element roles plus 1–4 optional roles selected from the candidate pool based on source richness.

- Use source-derived colors: always include the 3 mandatory color roles (subject, dark-anchor, accent), then add only the distinct tones the photograph itself supports, all on the fixed ivory background. There is no fixed color count — keep the palette restrained, fewer rather than more.

- No added text: no title, no year, no caption, no signature, no watermark. Text naturally present in the photograph (signs, labels, graffiti, dates, slogans) is preserved as part of the photo. Recognizable cultural text may also appear in the abstract region, anchored to the structure it belongs to at its original relative position — never lifted out and recomposed as separate typography.

- No decorative elements that are not derived from the source photograph. Every abstract element must trace back to something visible in the photo.

- The abstract style is minimal editorial: clean geometric forms, flat color fields, fine lines, generous negative space.

- The overall feeling is high-end editorial design, contemporary art-exhibition, architectural graphic, understated luxury, museum-level art direction.

- Generous margins and balanced central composition in the abstract region.

- Keep every locked token unless the user explicitly overrides it; write a continuing series-level override to the series lock and current photo decisions only to its poster manifest.

## Execute each source

1. Inspect the image and identify the primary subject, faces, identity signage, unique structure, spatial relationships, leading lines, key light, textures, and notable details.
2. Select a subject-focused 3:2 crop. For portrait inputs this is mandatory; for landscape inputs crop to focus on the primary subject. The crop may reduce surrounding scene and background. Protect the primary subject and identity information first, then spatial relationships. Remove low-information background and distant surroundings before secondary subjects.
3. If no 3:2 window contains every protected element, choose the window preserving the primary subject and identity information most completely. Record discarded secondary elements in the current manifest; do not switch to a left-right layout.
4. Determine abstract elements: select the 3 mandatory roles (primary-form, secondary-structure, spatial-anchor) plus 1–4 optional roles from the candidate pool (organic-accent, material-pattern, light-mass, detail-mark, native-text-mark, figure-silhouette). Choose 4–7 total based on the source's visual richness. Each element must have a clear origin in the photograph. Fewer strong elements beat many weak ones. When culturally significant text is present (dates, mottos, place names, slogans), prefer the native-text-mark role: keep it anchored to the structure it belongs to at its original relative position, flat and minimal, never recomposed as separate typography.
5. Determine palette: always include the 3 mandatory color roles (subject, dark-anchor, accent), then add only distinct tones the photograph actually shows (candidates include natural, sky-water, material, highlight, muted, and any other clearly present tone). There is no fixed count — follow the source's color richness, but keep the palette restrained: prefer fewer, cleaner colors over many. All colors must be sampled from the photograph.
6. Fill the current poster manifest with crop, resolved colors with roles, resolved abstract elements with roles and photo-origin notes, and the series lock version. Do not copy these values into the series lock.
7. Construct the image instruction in this fixed order: crop → canvas and exact 50:50 layout (equal heights, no tolerance) → photographic strict-fidelity (no filters, no editing, only crop, photo fills top region edge-to-edge at 3:2) → abstract element list with roles → color list with roles and background → minimal editorial style (clean geometry, flat color, fine lines, generous space, balanced composition) → prohibited treatments (no added text, no added decoration, no photo modification, no template feel, no 3D, no gradients, no neon).
8. Use an available image-generation or image-editing tool with only the corresponding source photo attached as content reference. A series lock is a text constraint, not a content image.
9. Inspect the result against the preset and source. Any split that is not exactly 50:50 (unequal heights), photo not filling the top region edge-to-edge, letterboxing, unsafe crop, subject distortion, collage, wrong element count, any added text or decoration, wrong background, any filter or color change on the photo, or decorative elements not from the photo is a concrete defect. Text naturally present in the photo is not a defect.
10. Update the manifest quality checks. Retry a defective result once with the defect named explicitly and record the defect. If the second result still fails, report the limitation rather than regenerating indefinitely.
11. Save the series lock and one manifest per poster in the output directory when possible; otherwise return them as separate copyable YAML blocks.

If the environment cannot generate or edit images, provide the completed photo-specific instruction, series lock, and current manifest instead of claiming an image was produced. If it cannot inspect images, stop before inventing photo content. If it cannot attach the source as a direct image reference, prepare the instruction but do not generate a substitute subject.

## Final check

Confirm: 3:4 canvas; one source; exact 3:2 subject-focused crop filling the entire top region edge-to-edge; photo above; minimal abstract composition below; exactly 50:50 split with strictly equal heights (no tolerance); no divider, no gap, no letterboxing; fixed ivory background; photographic region strictly unchanged from source except for cropping (no filters, no color changes, no retouching); all colors from the source with the 3 mandatory roles present and the palette restrained; 4–7 source-specific abstract elements with clear photo origins; no added text or decoration (photo-native text including signs, dates, slogans is fine; recognizable cultural text kept in the abstract region stays anchored to its structure at its original relative position, never recomposed); clean geometric minimal editorial style; flat color and fine lines; generous whitespace and balanced composition; high-end museum-exhibition editorial feel; faithful subject; series lock plus one current-photo manifest returned or saved.
