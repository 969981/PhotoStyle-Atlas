---
name: lr-edit-session
description: >
  Full single-photo edit session in Adobe Lightroom cloud desktop via Computer
  Use. Orchestrates composition → lighting → color grade with an edit receipt.
  Use when the user asks to "edit this photo", "full pass", "finish this image",
  "make this look like…", "retouch in Lightroom end-to-end", or wants a complete
  Lightroom Computer Use workflow. Not for batch culling, multi-album organization,
  or export unless explicitly requested.
license: MIT
compatibility: >
  Requires ChatGPT Computer Use and Adobe Lightroom cloud desktop. Coordinates
  lr-computer-use, lr-composition, lr-lighting, and lr-color-grade.
metadata:
  author: photo-editing-computer-use
  version: "0.1.0"
  product: lightroom-cloud-desktop
---

# lr-edit-session

Run a **complete single-photo** Lightroom edit with Computer Use. This skill
orchestrates domain playbooks; it does not replace them.

## Load order

1. Follow base ops from `lr-computer-use` (setup, loop, safety).
2. Execute domain steps using the same rules as:
   - `lr-composition`
   - `lr-lighting`
   - `lr-color-grade`
3. Use `references/session-playbook.md` for intake templates and receipt format.

## Session pipeline

### 0. Preflight

- Computer Use on; Lightroom visible and allowed
- Identify target photo; enter **Edit**
- Create Version/Copy if UI offers and edits will be exploratory
- Confirm single photo selected (deselect extras)

### 1. Intake (brief)

Parse user language into:

| Field | Examples |
| --- | --- |
| Intent | natural, cinematic, bright airy, moody, product-accurate |
| Must keep | full body, no crop, brand colors, skin soft |
| Aspect | 4:5, 16:9, original |
| References | “like the previous one”, attached style image description |
| Out of scope | no generative remove, no heavy clarity |

If critical intent is missing, ask **one** concise clarifying question only when
blocked; otherwise assume **natural documentary** polish.

### 2. Composition

Run `lr-composition` workflow:

- Straighten → aspect → reframe → geometry if needed
- Skip if brief forbids crop and frame is already level

### 3. Lighting

Run `lr-lighting` workflow:

- Global light order, then local masks if required
- Match intent (airy vs moody)

### 4. Color grade

Run `lr-color-grade` workflow:

- WB → vibrance/sat → mixer if needed → grading wheels per look
- Protect skin/product

### 5. Soft finish (optional)

Only if brief asks or image clearly needs it:

- Mild Texture/Clarity on subject (not gritty portraits unless asked)
- Mild Dehaze for atmospheric haze
- Subtle vignette for focus

Do not build a full Effects skill here; keep finish minimal.

### 6. Review

1. Fit to screen; before/after
2. Check faces, horizons, clipping, color casts
3. Correct only clear regressions (one tight pass)
4. **Do not export** unless user explicitly asked — then confirm destination/format

### 7. Edit receipt

Return a structured receipt (see playbook):

- Photo identity
- Intent assumed
- Composition / light / color / finish actions
- Skipped steps with reason
- Risks and suggested next steps (export size, preset save, series match)

## Routing shortcuts

| User ask | Path |
| --- | --- |
| Only crop/straighten | `lr-composition` only |
| Only exposure | `lr-lighting` only |
| Only grade/WB | `lr-color-grade` only |
| Full edit / “make it look good” | this skill, full pipeline |
| Setup Computer Use | `lr-computer-use` |

## Batch policy (v1)

Default **one photo**. If user selects many:

1. Ask whether to edit only the primary or sync settings after one hero edit.
2. Do not silently apply across the filmstrip.

## Safety

Inherit hard stops from `lr-computer-use` / `references/computer-use-safety.md`
(export, delete, cloud, credentials, wrong window).

## Additional resources

- `references/session-playbook.md`
- Domain skills under `.agents/skills/lr-*`
