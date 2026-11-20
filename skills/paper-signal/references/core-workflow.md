# Core workflow

Treat every image request as a small editorial production. The workflow stays light for a single poster and expands only when a series, evidence, or caption requires it.

## Production states

Move through these states:

1. `intake` — resolve purpose, subject, output, exact text, image roles, and constraints.
2. `protected` — record subject, identity, crop, factual, and semantic invariants.
3. `routed` — choose delivery route, subject route, composition mode, and transformation depth.
4. `architected` — for a series, decide image jobs, story rhythm, scope, and caption handoffs.
5. `art-directed` — lock paper, process, type, hue, image–signal relation, and texture intensity.
6. `compiled` — save one final four-paragraph prompt per image.
7. `rendered` — generate raster assets and preserve versions.
8. `audited` — pass subject, evidence, text, material, composition, and delivery gates.
9. `delivered` — show the image and return its reproducible artifacts.

For a single new image, `grounded` evidence work and multi-card architecture may be unnecessary. Never skip `protected`, `routed`, `compiled`, or `audited`.

## Smart defaults

| Field | Default |
|---|---|
| Delivery route | Single card |
| Subject route | Infer from the dominant visual subject |
| Canvas | Preserve edit target; otherwise 3:5 poster or 3:4 social card |
| Visible text | One short phrase or none |
| Public source labels | Hidden |
| Preset | `minimal-zine-standard` |
| Composition | Subject-aware, never globally fixed |
| Anchor ink | Derive from subject; cobalt fallback |
| Raster backend | Runtime-native tool |

Ask only if an unresolved choice changes identity, factual meaning, rights, output count, or the dominant visual direction. Combine questions.

## Confirmation gate

Confirm immediately before raster generation after all prompt files exist. Show:

- delivery and subject routes
- count and aspect ratio
- composition mode and preset
- anchor hue and lead process
- edit invariants when applicable
- public source-label policy when applicable
- output directory

Skip only when the current request explicitly says to generate directly, use defaults, or skip confirmation.

## Source-of-truth hierarchy

When artifacts disagree, use:

1. explicit current user instruction
2. edit-target preservation record or verified claim in `evidence.json`
3. approved outline or art-direction record
4. current prompt file
5. generated bitmap

The bitmap is never the source of truth. Correct upstream artifacts first.

## Versioning

- Text revision: `filename-v2.md`, then `filename-v3.md`.
- Image revision: `NN-role-slug-v2.png`.
- Whole-project collision: append `-YYYYMMDD-HHMMSS`.
- Record the selected prompt and output in `manifest.json`.
- Never destroy the edit target or a generated candidate to make room for a correction.

## Generation sequence

1. Save and verify every prompt for the current generation group.
2. Render the first image without an unnecessary series reference.
3. Inspect subject integrity, composition scale, paper, process, type, hue, and anti-AI failures.
4. For a series, accept the first image as the material reference.
5. Render later images as distinct calls with their own subject-aware composition modes.
6. Make one targeted correction per retry and preserve successful outputs.

Do not use variants from one generic prompt as substitutes for distinct cards.

## Progress communication

- after routing: state delivery route, subject route, and composition choice
- after art direction: state paper, process, hue, and protected details
- during rendering: report accepted images, not every internal attempt
- at completion: state paths, validation result, and caveats

## Completion definition

A single-image job is complete when the selected raster, saved prompt, and mode record exist and visual gates pass. A series is complete only when every requested image, caption/outline when needed, evidence trail when needed, manifest, and validation result are present.
