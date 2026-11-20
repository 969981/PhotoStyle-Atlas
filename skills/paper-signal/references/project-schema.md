# Project schema

`manifest.json` is the machine-readable production plan. Single-image projects may keep a compact artifact set; series and evidence routes add editorial files.

## Required manifest

```json
{
  "$schema": "https://raw.githubusercontent.com/jiahuiqu17/paper-signal/main/schemas/project-manifest-1.1.schema.json",
  "schema_version": "1.1",
  "project": {
    "slug": "edinburgh-after-rain",
    "title": "Edinburgh after rain",
    "language": "en",
    "created_at": "2026-08-11T12:00:00Z"
  },
  "route": "single-card",
  "subject_route": "landscape",
  "platform": "poster",
  "aspect_ratio": "3:5",
  "public_source_labels": false,
  "status": "planned",
  "style": {
    "preset": "weathered-horizon",
    "composition_mode": "panorama-strip",
    "paper": "pale stone-gray scanned stock",
    "process": "cyanotype-newsprint",
    "display_type": "small old-book serif",
    "utility_type": "typewriter microtext",
    "anchor_ink": "vermilion",
    "anchor_hex": "#D9472B",
    "quiet_paper": "58%-78%",
    "active_image": "18%-36%",
    "color_area": "2%-9%",
    "texture_intensity": "medium"
  },
  "images": [
    {
      "index": 1,
      "role": "poster",
      "slug": "after-rain",
      "subject_route": "landscape",
      "composition_mode": "panorama-strip",
      "prompt": "prompts/01-poster-after-rain.md",
      "output": "outputs/01-poster-after-rain.png",
      "on_image_text": ["AFTER THE RAIN"],
      "claim_ids": []
    }
  ]
}
```

`$schema` is optional for existing projects and enables editor validation when present. For backward compatibility, validators may accept schema `1.0` and the legacy `cards` key. New projects use schema `1.1` and `images`.

Allowed routes: `new-series`, `single-card`, `restyle-existing`.

Allowed subject routes: `landscape`, `portrait`, `object`, `architecture`, `concept`, `evidence`, `mixed-series`.

Allowed composition modes: `airy-fragment`, `photo-window`, `panorama-strip`, `dual-frame`, `specimen-plate`, `portrait-archive`, `type-object`.

Allowed statuses: `draft`, `planned`, `prompted`, `rendered`, `validated`.

For an accepted correction, point `prompt` and `output` to the selected version and optionally record `base_prompt` and `parent_output`.

## Artifact sets

### Single new image

Required:

- `brief.md`
- `manifest.json`
- selected `prompts/*.md`
- selected `outputs/*` when rendered

Optional: `evidence.json`, `analysis.md`, `caption.md`, `outline.md`, and `refs/`.

### Existing-image restyle

Required:

- single-image requirements
- `preservation.md`
- original edit target in `refs/` or an unambiguous external path recorded in the manifest

### Series

Required:

- `brief.md`
- `analysis.md`
- `outline.md`
- `caption.md` when publishing copy is requested
- `manifest.json`
- prompt and output for every selected image
- `evidence.json` when any factual claim, review, ranking, or source document is used

## Filename rules

- Project slug: 2-5 lowercase kebab-case words.
- Prompt: `NN-{role}-{slug}.md`.
- Output: same stem, `.png` preferred.
- Indices: zero-padded, sequential, and unique.
- Preserve old files with `-v2`, `-v3`, or a timestamp; never silently overwrite.

## Prompt requirements

Every prompt file contains exactly four compact paragraphs:

1. canvas, paper, adaptive composition, and protected crop
2. subject invariants and one reproduction process
3. exact text or no-text instruction, type, hue/form/area, and print defects
4. emotional temperature and hard avoids

Do not include YAML, source paths, production notes, or labelled planning sections.

## Validation states

- `planned`: brief and manifest complete; prompts may be missing.
- `prompted`: every selected image has a saved prompt.
- `rendered`: every selected output exists.
- `validated`: automated checks pass and human full-size/thumbnail review is recorded.

Do not mark a project `validated` based only on the script.
