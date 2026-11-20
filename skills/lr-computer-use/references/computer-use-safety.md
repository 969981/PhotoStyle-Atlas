# Computer Use safety for Lightroom

## Permission model

Computer Use can view the screen and operate allowed apps. Treat everything
visible in Lightroom (including private photos, names, map locations, client
galleries) as context the model may process while the task runs.

- Grant **Always allow** only for apps the user trusts for repeated automation.
- System permissions (macOS Screen Recording / Accessibility) are separate from
  in-app Always-allow lists.
- File and shell actions still follow Codex/ChatGPT sandbox settings; GUI edits
  in Lightroom may not show in a code review pane until exported.

## Allowed by default

- Navigate Library / Edit
- Select photos the user indicated
- Adjust edit sliders and tools on the current photo
- Create a version/copy when the UI offers it and the edit is experimental
- Toggle before/after or history for verification
- Read histogram and panel values when visible

## Require explicit user confirmation

- Export (any format, destination, overwrite)
- Share / publish / invite / generate web gallery
- Delete photos, albums, or people groups
- Move large sets of assets between cloud storage states
- Apply presets that rewrite many photos at once (batch)
- Generative AI tools that may use cloud credits if the user did not request them
- Sign-out, account, payment, or subscription UI

## Stop immediately

Stop the Computer Use task and describe the screen when:

- A password, 2FA, or OS elevation prompt appears
- The frontmost window is not Lightroom (or the expected dialog)
- The wrong photo is selected and identity is ambiguous
- Lightroom shows a blocking error, catalog/sync conflict, or crash dialog
- The user takes over the keyboard/mouse mid-task (especially on Windows)
- An action would affect many photos when the brief was single-photo

## Batch and cloud risk

Lightroom cloud desktop syncs edits. Prefer single-photo work in v1 skills.
If multiple photos are selected, **deselect extras** or ask before applying
global changes.

## Secrets and sensitive content

Do not open unrelated apps. Do not read notification toasts for secrets.
If a photo contains sensitive documents (IDs, medical, children in contexts
the user did not intend to process), pause and confirm scope.

## Recovery

- Prefer panel-level Reset or History step-back over full image reset.
- If the edit went wrong: undo recent steps, re-observe, try a smaller change.
- If lost in UI: return to All Photos / grid, re-select the photo, re-enter Edit.
