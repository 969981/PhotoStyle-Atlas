---
name: lr-computer-use
description: >
  Drive Adobe Lightroom (cloud desktop app) via ChatGPT Computer Use. Use when
  the user asks to "use Lightroom with computer use", "open Lightroom and edit",
  "drive Lightroom", "@Computer Lightroom", or needs setup/safety for GUI photo
  editing. Not for Lightroom Classic Develop module maps, pure coding tasks, or
  export/delete workflows without explicit user confirmation.
license: MIT
compatibility: >
  Requires ChatGPT desktop (Work or Codex) with Computer Use plugin, and Adobe
  Lightroom cloud desktop on Windows or macOS. Windows Computer Use is foreground-only.
metadata:
  author: photo-editing-computer-use
  version: "0.1.0"
  product: lightroom-cloud-desktop
---

# lr-computer-use

Operate **Adobe Lightroom (cloud desktop)** with Computer Use using a tight
observe → act → verify loop. This is the shared base for composition, lighting,
and color-grade skills.

## When to use

- User wants ChatGPT/Codex to control Lightroom on the desktop
- Domain skills need shared UI navigation and safety rules
- Setup or troubleshooting Computer Use + Lightroom access

Do **not** use for Lightroom Classic-only workflows (different UI), or for tasks
that only need file-system operations without the Lightroom GUI.

## Prerequisites

1. ChatGPT desktop app in **Work** or **Codex**; Computer Use plugin installed and enabled.
2. User has approved **Lightroom** (or will approve when prompted). Prefer Always-allow only if they trust ongoing control.
3. Lightroom is installed, signed in, and **visible** on the active desktop (required on Windows).
4. Target photo is open or clearly selectable in Library.

Read `references/windows-setup.md` on Windows; read `references/computer-use-safety.md` before destructive or cloud actions.

## Invocation

Mention Computer Use and the app explicitly:

```text
With Computer Use, open @Lightroom and edit the selected photo.
```

```text
Use Computer Use on Lightroom — crop and brighten this image.
```

If the Computer Use skill/server is available, keep it enabled for the session.

## Core control loop

Repeat for every meaningful change:

1. **Observe** — Confirm Lightroom is the frontmost relevant window. Read Edit vs Library mode, selected photo, open panel, histogram if visible.
2. **Decide** — One goal only (e.g. “lift shadows slightly”, “straighten horizon”).
3. **Act** — Open the correct Edit section, adjust a small cluster of related controls.
4. **Verify** — Re-read the image (and histogram). Undo or dial back if worse.
5. **Report** — Note what changed before moving on.

Never chain many unrelated panels without re-observing. Prefer small slider moves over extreme jumps.

## Lightroom desktop UI (map)

Lightroom cloud desktop is **not** Lightroom Classic. Labels vary slightly by version; re-identify from the screen each session.

| Area | What to look for |
| --- | --- |
| Library / All Photos | Grid or filmstrip of assets |
| Edit mode | Detail view with right-side edit tools |
| Crop | Crop & rotate, aspect ratio, straighten |
| Healing / Remove | Spot remove, heal, generative remove (use only if asked) |
| Masking | Subject, sky, background, brush, linear/radial |
| Light | Exposure, contrast, highlights, shadows, whites, blacks, curve |
| Color | Temp, tint, vibrance, saturation, mixer / point color, color grading |
| Effects | Texture, clarity, dehaze, vignette, grain |
| Detail | Sharpening, noise reduction |
| Optics | Lens corrections, defringe |
| Geometry | Upright / transform / perspective |
| Presets | Saved looks; apply only if brief allows |

Full panel notes: `references/lightroom-desktop-ui.md`.

### Enter Edit mode

1. Focus Lightroom.
2. Select the target photo if not already selected.
3. Open **Edit** (toolbar or double-click into edit, depending on current view).
4. Confirm right-side edit sections are visible.

### Open a section

Click the section icon/name (Light, Color, Crop, etc.). Expand collapsed groups by clicking headers. Do not assume Classic keyboard panel shortcuts (`Ctrl+1`… panel numbers) work the same way.

## Interaction preferences

1. Prefer **visible labeled controls** over memorized pixel coordinates.
2. If using coordinates, re-anchor from a fresh screenshot every step.
3. Drag sliders slowly; pause to let the preview refresh.
4. Use **Reset** only for the current tool/panel group when intentional — never global reset without confirmation.
5. Prefer **Version / Copy** (if present) before experimental heavy edits when the user cares about non-destructive rollback.

## Safety (hard stops)

Pause and ask the user before:

- Export, share, publish, or email
- Delete photo, remove from cloud, empty trash
- Overwrite originals or replace existing exports
- Account, subscription, or privacy settings
- Generative Remove / AI tools that may consume credits (unless user asked)

If the wrong window, wrong photo, or a system permission dialog appears: **stop**, describe what is on screen, and wait.

Details: `references/computer-use-safety.md`.

## Platform notes

### Windows

- Computer Use runs on the **active desktop** and takes foreground pointer/keyboard.
- Keep Lightroom maximized or clearly unobscured while the task runs.
- Optional allow-list in Codex config (app id as reported by Computer Use), e.g. Lightroom executable / AUMID when known.
- User should not use the same desktop for other work during the run.

### macOS

- Screen Recording + Accessibility permissions for Computer Use.
- Prefer keeping Lightroom on a dedicated space if locked-use is not enabled.

## Handoff to domain skills

| Need | Skill |
| --- | --- |
| Crop, straighten, reframe, geometry | `lr-composition` |
| Exposure, tone, curves, light masks | `lr-lighting` |
| WB, color mixer, grading looks | `lr-color-grade` |
| Full ordered edit + receipt | `lr-edit-session` |

Domain skills assume this base loop and safety model. Load `references/lightroom-desktop-ui.md` only when panel layout is unclear.

## Completion report

When finishing any Computer Use Lightroom task, report:

1. **Photo** identified (name/thumbnail context if known)
2. **Panels / tools** used
3. **Changes** in plain language (not only slider names)
4. **Verification** (before/after or what improved)
5. **Not done** (export, batch, etc.) unless requested
6. **Risks** (clipping, skin tones, over-crop)

## Additional resources

- `references/computer-use-safety.md` — permissions, destructive actions, stop conditions
- `references/lightroom-desktop-ui.md` — Edit sections and navigation detail
- `references/windows-setup.md` — Windows Computer Use + Lightroom setup
