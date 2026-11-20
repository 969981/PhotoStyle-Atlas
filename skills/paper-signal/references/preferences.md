# Preferences contract

Read this file only when a Paper Signal preference file exists.

## Resolution order

Use the first available file:

1. `.paper-signal/PREFERENCES.md` in the current project
2. `${XDG_CONFIG_HOME:-$HOME/.config}/paper-signal/PREFERENCES.md` for the user

The current request always wins. Preferences may refine an omitted choice but must not override exact text, protected subject details, evidence integrity, output destination, or an explicit user instruction.

## Supported fields

Preference files use YAML frontmatter so defaults remain scannable and editable:

| Field | Value | Effect |
|---|---|---|
| `schema_version` | `"1.0"` | Preference contract version |
| `default_aspect_ratio` | ratio string | Default for new images only; never recrop an edit target silently |
| `default_platform` | string | Platform safe-zone and delivery assumption |
| `preferred_presets` | string list | Ordered material presets to consider before fallback |
| `preferred_process` | string | Preferred lead reproduction process when compatible with the subject |
| `preferred_anchor_inks` | string list | Small personal palette; choose one meaningful ink per image |
| `texture_intensity` | `low`, `medium`, or `high` | Default physical-surface strength |
| `visible_text_policy` | `none`, `minimal`, or `content-led` | Default text burden when the request is silent |
| `public_source_labels` | boolean | Default public artwork policy; provenance remains internal either way |
| `caption_voice` | short description | Preferred voice for requested social copy |
| `banned_motifs` | string list | Personal anti-cliché list |
| `notes` | string | Additional bounded preference |

Ignore unknown fields and mention them only if they affect the current task. Reject values that conflict with the active route or quality contract.

## Application rules

1. Report only preferences that materially affected the run.
2. Do not force a favourite composition onto an unsuitable subject.
3. Do not use every preferred ink in one image.
4. Treat banned motifs as additions to, not replacements for, the shared anti-pattern rules.
5. Do not invent first-person experience from `caption_voice`.
6. Keep project and user preferences outside generated image prompts unless the field changes pixels.

Copy `assets/PREFERENCES.example.md` to one of the supported locations as a starting point.
