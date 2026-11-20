# Style Presets

Locked design tokens for the `ivory-editorial-v1` preset. These values define the visual contract shared by every poster in a series. New series start from `assets/series-lock.template.yaml`.

## `ivory-editorial-v1`

### Canvas

| Key | Value |
| --- | --- |
| canvas.width | `1080` |
| canvas.height | `1440` |
| canvas.ratio | `"3:4"` |

### Layout

| Key | Value |
| --- | --- |
| layout.ratio | `"50:50"` |
| layout.tolerance | `0` percentage points (strictly equal heights) |
| layout.top_region | `"photograph"` |
| layout.bottom_region | `"abstract"` |
| layout.top_height | exactly 50% of canvas height |
| layout.bottom_height | exactly 50% of canvas height |
| layout.photo_fills_top_region | `true` (edge-to-edge, no borders, no margins inside the photo region) |
| layout.vertical_gap | `0` (seamless edge-to-edge transition) |
| layout.divider | `none` (no line, no border, no gap between the two regions) |

### Crop policy

| Key | Value |
| --- | --- |
| crop.policy | `"subject-focused"` |
| crop.target_ratio | `"3:2"` (matches the top region ratio: full canvas width × exactly half canvas height) |
| crop.orientation | `"landscape"` |
| crop.priority_order | `["primary-subject", "identity-information", "spatial-relationships"]` |
| crop.discard_order | `["distant-background", "peripheral-low-information", "secondary-subjects"]` |
| crop.portrait_mandatory_crop | `true` |
| crop.portrait_layout | `"top-photo-bottom-abstract"` (never left-right) |
| crop.surrounding_reduction_allowed | `true` |
| crop.surrounding_reduction_level | `"flexible"` (crop as needed to achieve exact 3:2 ratio while protecting priority content) |
| crop.subject_framing | `"balanced"` (not too tight, not too loose) |
| crop.result_fills_top_region | `true` (the cropped photo fills the entire top region edge-to-edge with no letterboxing) |

### Background

| Key | Value |
| --- | --- |
| background.color | `"#F3EBDD"` |
| background.name | `"ivory"` |
| background.poster_background | `true` |
| background.abstract_region_background | `"#F3EBDD"` |
| background.region_below_photo | `"#F3EBDD"` |

### Photographic fidelity

| Key | Value |
| --- | --- |
| photo.fidelity | `"strict"` |
| photo.allowed_modifications | `["crop"]` |
| photo.forbidden_modifications | `["filters", "color-grading", "stylization", "retouching", "compositing", "rotation", "stretching"]` |
| photo.native_text_preserved | `true` |
| photo.preserve_subject_identity | `true` |
| photo.preserve_proportions | `true` |
| photo.preserve_perspective | `true` |
| photo.preserve_materials | `true` |
| photo.preserve_light | `true` |
| photo.preserve_shadows | `true` |

### Abstract composition — minimal editorial

| Key | Value |
| --- | --- |
| abstract.approach | `"minimal-editorial"` |
| abstract.style | `"geometric-reductive"` |
| abstract.sensibility | `"high-end-editorial + museum-exhibition + architectural-graphic"` |
| abstract.instantly_recognizable | `true` |
| abstract.clean_geometry | `true` |
| abstract.flat_color_fields | `true` |
| abstract.fine_lines | `true` |
| abstract.gradients | `false` |
| abstract.shadows_in_abstract | `false` |
| abstract.three_d | `false` |
| abstract.decorative_additions_forbidden | `true` |
| abstract.elements_from_source_only | `true` |
| abstract.balanced_central_composition | `true` |
| abstract.generous_margins | `true` |

### Abstract element roles

| Key | Value |
| --- | --- |
| abstract.mandatory_roles | `["primary-form", "secondary-structure", "spatial-anchor"]` |
| abstract.optional_pool | `["organic-accent", "material-pattern", "light-mass", "detail-mark", "figure-silhouette"]` |
| abstract.min_element_count | `4` |
| abstract.max_element_count | `7` |
| abstract.selection_basis | `"source richness and visual strength"` |
| abstract.fewer_strong_better_than_many_weak | `true` |

### Palette roles

| Key | Value |
| --- | --- |
| palette.background | `"#F3EBDD"` |
| palette.mandatory_roles | `["subject", "dark-anchor", "accent"]` |
| palette.additional_pool | `["natural", "sky-water", "material", "highlight", "muted"]` (examples, not exhaustive — any clearly present tone in the photo may be used) |
| palette.count_policy | `"no fixed count — 3 mandatory roles plus only the distinct tones the source photo supports"` |
| palette.restraint | `"fewer rather than more — clean, considered, editorial"` |
| palette.source | `"extracted from the photograph"` |
| palette.all_colors_from_source | `true` |
| palette.selection_basis | `"source color richness under the restraint principle"` |

### Editorial design qualities

| Key | Value |
| --- | --- |
| editorial.negative_space | `"generous"` |
| editorial.margin_width | `"wide"` |
| editorial.composition_balance | `"centered, asymmetrically balanced"` |
| editorial.visual_weight | `"light and considered"` |
| editorial.touch | `"quiet, precise, unhurried"` |
| editorial.luxury_level | `"understated, museum-grade"` |
| editorial.avoid | `["template-feel", "commercial-cliche", "cartoon", "3d-render", "over-decoration", "gradients", "neon", "complex-illustration", "subject-distortion"]` |

### Text

| Key | Value |
| --- | --- |
| text.added_text_forbidden | `true` |
| text.photo_native_text_preserved | `true` |
| text.photo_native_examples | `["signs", "labels", "graffiti", "dates", "slogans", "plaques", "markings"]` |
| text.abstract_region_native_text_allowed | `true` |
| text.abstract_region_native_text_behavior | `["anchored-to-structure", "original-relative-position", "flat-minimal", "not-recomposed"]` |
| text.abstract_region_native_text_examples | `["dates", "mottos", "place-names", "slogans", "plaques"]` |
| text.forbidden_examples | `["title", "year", "caption", "signature", "watermark", "decoration"]` |

### Series identity

| Key | Value |
| --- | --- |
| series.preset_id | `"ivory-editorial-v1"` |
| series.schema_version | `3` |
| series.shared_constants | `["canvas", "layout", "crop-policy", "background", "photo-fidelity", "abstract-style", "palette-roles", "element-roles", "no-added-text"]` |
| series.per_poster_variables | `["crop-window", "specific-colors", "specific-elements", "quality-checks", "photo-origin-notes"]` |
