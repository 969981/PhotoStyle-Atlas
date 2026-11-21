# GenAI Portrait Skill

GenAI Portrait Skill helps vision-capable AI agents edit portraits and headshots as coherent photographs rather than isolated collections of pixels.

The intended scope includes background adaptation, relighting, ID-photo preparation, cleanup, reframing, wardrobe adjustments, restrained appearance changes, and other portrait-specific edits. A difficult request such as moving a bright white-background headshot onto a black website is treated as a photographic transformation: the background, subject lighting, color, edge behavior, and visual separation must all agree.

The repository includes a composable CLI and one canonical agent skill. The CLI produces artifacts; a vision-capable agent inspects them and decides whether to accept, retry, or change strategy.

## Install

```bash
uv venv .venv
uv pip install --python .venv/bin/python -e '.[dev]'
scripts/genai-portrait --help
```

Copy `.env.example` to `.env` and replace only the credentials needed by the provider you use.

## CLI

Run a generative edit with one or more ordered input images:

```bash
genai-portrait edit \
  --provider gemini \
  --input portrait.jpg \
  --prompt-file prompt.txt \
  --output-dir runs/lighting-study
```

For identity-preserving lighting transfer, provide the authoritative portrait first and the lighting reference second:

```bash
genai-portrait edit \
  --provider openai \
  --input portrait.jpg \
  --input lighting-reference.png \
  --prompt-file transfer-prompt.txt \
  --output-dir runs/lighting-transfer
```

Apply an alpha mask without modifying RGB values:

```bash
genai-portrait apply-alpha \
  --image relit.png \
  --mask matte.png \
  --output runs/composite/portrait-rgba.png
```

Create a visual comparison:

```bash
genai-portrait inspect source.jpg candidate-1.png candidate-2.png \
  --output runs/review/contact-sheet.jpg
```

Every `edit` run writes `manifest.json` with relative input paths, hashes, provider/model metadata, prompt provenance, and output artifacts.

## Synthetic Demonstration

The demonstration uses a fully synthetic person generated for this repository. It shows a difficult environment change rather than a pixel-only background replacement.

| Synthetic white-background source | Final GPT lighting transfer |
|---|---|
| ![Synthetic white-background source](examples/assets/synthetic_white_input.png) | ![Synthetic final dark-studio portrait](examples/assets/synthetic_dark_final.png) |

The full comparison sheet also includes the Gemini lighting reference. Its three columns are:

- `synthetic_white_input.png`: a flat, bright white-background phone-style headshot.
- `synthetic_gemini_lighting_reference.png`: Gemini establishes a coherent dark-studio lighting design but visibly changes identity-bearing details.
- `synthetic_dark_final.png`: GPT receives the original first and the Gemini candidate second, then transfers the lighting concept while using the original as the sole identity authority.

The example is not evidence that one model always wins. It demonstrates the skill's execution-review-correction loop: inspect the actual candidates, diagnose the failure, and choose the next operation based on the acceptance criteria.

The prompts are committed under `examples/prompts/`. Full-resolution synthetic inputs and outputs are under `examples/assets/`.

## Design Direction

- Define success through identity preservation, photographic coherence, and artifact-free output.
- Let a vision-capable agent inspect candidates and choose whether to accept, retry, switch models, or revise prompts.
- Use generative models for semantic image edits.
- Keep local Python processing auditable and limited to artifacts, masks, alpha compositing, manifests, and inspection views.
- Treat user portraits as private data. Public examples use synthetic subjects.

## Agent Installation

Give this repository URL to Codex, Claude Code, Cursor, OpenCode, or another coding agent and ask it to install `skills/skill_genai_portrait.md` into the workspace's existing skill discovery chain. The installer should first read the target workspace's `AGENTS.md` or `CLAUDE.md`, follow any routing file, and update `rules/skills/INDEX.md`, `skills/INDEX.md`, or the nearest equivalent pointer.

## License

MIT
