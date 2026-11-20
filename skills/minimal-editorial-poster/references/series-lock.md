# Portable State

Keep reusable series rules separate from source-specific poster decisions. State files do not contain hidden conversation memory and do not make image generation pixel-deterministic.

## Identify the document

- `document_type: series-lock`, `schema_version: 3`: current reusable series state for `ivory-editorial-v1`.
- `document_type: poster-manifest`, `schema_version: 3`: one poster's source-specific decisions and review evidence.
- `document_type: series-lock`, `schema_version: 3`, `preset_id: ivory-decon-v1`: previous deconstruction pure-form series lock; migrate to `ivory-editorial-v1` before use.
- `document_type: poster-manifest`, `schema_version: 3`, `preset_id: ivory-decon-v1`: previous deconstruction manifest; informational only, not migrated forward.
- `document_type: series-lock`, `schema_version: 2`, `preset_id: ivory-pure-v1`: earlier pure-form v1 series lock; migrate through schema 3 deconstruction then to editorial.
- `document_type: poster-manifest`, `schema_version: 2`, `preset_id: ivory-pure-v1`: earlier pure-form manifest; informational only.
- No `document_type`, `schema_version: 1`, `preset_id: museum-ivory-v1`: legacy minimal-form mixed lock; migrate it before use.
- `document_type: series-lock`, `preset_id: museum-ivory-v1`: minimal-form series lock; can be imported as a starting point but the preset must change to `ivory-editorial-v1`.
- Any other type, schema, or preset: report the incompatibility and do not pretend to continue the series.

## Series lock

Start from `assets/series-lock.template.yaml`. It stores only fields that later posters inherit:

- preset, canvas, crop policy, protected-content priority, layout, and background;
- photographic fidelity policy (strict source-only, crop-only modifications);
- palette mandatory roles, optional role pool, and min/max count (not resolved hex colors);
- abstract mandatory element roles, optional role pool, and min/max count (not resolved forms);
- no-added-text rule with photo-native text preserved;
- abstract style guidance (minimal editorial, geometric reductive, flat color, fine lines, generous negative space, wide margins, balanced central composition);
- explicit series-level overrides the user wants later posters to inherit.

Do not store source paths, crop descriptions, resolved colors, resolved elements, personal metadata, or unrelated conversation text in the lock.

## Poster manifest

Copy `assets/poster-manifest.template.yaml` once per source. Resolve its source label, orientation, crop, palette (roles + values + count), abstract elements (roles + descriptions + photo origins + count), generation state, retry record, and quality checks. Multiple inputs require multiple manifests.

The manifest is an audit record for one poster. Never use one poster's resolved palette, elements, or crop as the next photo's content decisions. The next photo inherits only the series lock.

Use a non-sensitive source label. Do not store local absolute paths, image bytes, identity guesses, hidden prompts, API keys, or unrelated conversation data.

## Resolution order

1. Identify supplied state using the rules above.
2. For a current schema 3 `ivory-editorial-v1` lock, fill missing supported series fields from the preset and report their names.
3. For a schema 3 deconstruction lock (`ivory-decon-v1`), migrate it: keep canvas/crop/layout/background/palette structure, rename deconstruction → abstract with new element roles and style fields (minimal-editorial, geometric-reductive, flat color, fine lines, generous negative space), change preset to `ivory-editorial-v1`.
4. For a schema 2 pure-form lock (`ivory-pure-v1`), migrate it through schema 3 deconstruction form, then to editorial.
5. For a legacy minimal-form lock (`museum-ivory-v1`), import it as a starting point: keep canvas/crop/layout/background, change preset to `ivory-editorial-v1`, update palette and abstract element structures to the 3-mandatory + optional pool model, remove all typography title/year fields, add photographic fidelity and abstract style fields.
6. Without a lock, copy `assets/series-lock.template.yaml`.
7. Apply current explicit overrides. Store them in the lock only when the user wants later posters to inherit them.
8. Create a fresh manifest for each source and resolve photo-specific values there.
9. Save the lock and manifests beside outputs when possible; otherwise return separate YAML blocks.

## Conflicts and stopping rules

- Missing supported series fields: restore defaults and report the field names.
- Unknown type, schema, or preset: stop state continuation and explain the supported forms.
- Existing migration target: choose a new output location; never overwrite it.
- Current request conflicts with a locked field: the explicit request wins for this poster. Update the lock only if the user wants the change to continue.
- A portrait crop cannot preserve all protected content: keep the primary subject and identity information, record losses in the current manifest, and retain the top-and-bottom layout.
- Element count: the series lock defines the allowed range (4–7); the exact count per poster is chosen during photo analysis and recorded in the manifest, not in the lock. Color count is not range-limited: the 3 mandatory roles are always present and additional colors follow the source under the restraint principle (fewer rather than more).
