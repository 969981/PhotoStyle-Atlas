# Windows setup — Computer Use + Lightroom

## Install and enable

1. Install ChatGPT desktop (Work or Codex surface).
2. Open **Plugins → Computer Use** and install/enable if needed.
3. Enable Computer Use server/skill toggles.
4. Install and sign in to **Adobe Lightroom** (cloud desktop app).

## App approval

1. Start a task that targets Lightroom.
2. Approve Lightroom when prompted.
3. Optionally add Lightroom to **Always-allowed apps** in Settings → Computer Use.
4. Persistent policy may also live in `$CODEX_HOME/config.toml`:

```toml
[computer_use.windows]
always_allowed_app_ids = ["Lightroom.exe"]
```

Use the exact app id Computer Use reports (exe name or AUMID). Do not guess if
unsure — approve once interactively and copy the reported id.

## Foreground rules

On Windows, Computer Use:

- Operates the **active desktop session**
- Moves the pointer and types in the **foreground**
- Does **not** run Lightroom tasks fully in the background on the same session

Recommendations:

- Keep the PC unlocked and online for long tasks
- Leave Lightroom visible and unobstructed
- Avoid using the same desktop for other work during the run
- For hands-off long jobs, consider a VM or remote-check from phone per ChatGPT docs

## Pre-flight checklist

- [ ] Lightroom launched and finished sync noise if possible
- [ ] Target photo selected
- [ ] Lightroom not minimized
- [ ] No blocking modal dialogs open
- [ ] Second monitors: know which screen Lightroom is on
- [ ] User present for first-time permission prompts

## Troubleshooting

| Symptom | Action |
| --- | --- |
| Agent cannot see Lightroom | Bring app to front; check Always-allow; re-approve |
| Clicks hit wrong app | Close overlapping windows; maximize Lightroom |
| Agent stuck on login | User completes Adobe login manually |
| Sync spinner forever | Wait or ask user; do not spam clicks |
| Edits not appearing | Confirm Edit mode and correct photo selected |

## Safety on Windows

User can stop Computer Use or take over at any time. If local input is detected
in conflict scenarios, pause and re-sync intent with the user.
