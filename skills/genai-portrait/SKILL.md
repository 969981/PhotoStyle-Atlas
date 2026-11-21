---
name: genai-portrait
description: Agent-driven portrait and headshot editing with identity preservation, photographic coherence, model iteration, masks, and alpha outputs.
---

# GenAI Portrait Skill

## Use This Skill When

Use this skill for portrait and headshot work: background adaptation, relighting, white or dark studio portraits, ID-photo preparation, crop and composition changes, grooming or wardrobe cleanup, restrained appearance edits, masks, and transparent outputs.

This is not a general image-generation skill. Its central problem is changing a portrait while keeping the person recognizable and the complete photograph physically and aesthetically coherent.

## Goal

Produce a local portrait that satisfies the user's intent, remains unmistakably the same person unless identity change was requested, and looks like a plausible photograph rather than a subject pasted into altered pixels.

The final judge is visual identity preservation plus artifact-free photographic plausibility, not API success, prompt compliance, or dramatic style.

## Agent Autonomy

The vision-capable agent owns the execution loop. It may choose models, prompts, references, masks, candidates, contact sheets, and retry strategy. Prefer result constraints over fixed steps. Adapt the workflow to the failure actually visible in the images.

The CLI produces artifacts. It does not replace visual judgment. Inspect source and candidates directly; never declare success from exit status or file existence alone.

The agent should also apply expert photographic judgment beyond the user's literal wording. A major edit can imply coupled changes. Replacing a white background with black may require changed key light, fill ratio, edge separation, spill, clothing response, and color grade. A face-shape edit may require coherent contour and shadow changes. Do not perform only the easiest local operation when it leaves the photograph implausible.

## Acceptance Criteria

A task is complete only when:

- The requested change is clearly present.
- The subject remains unmistakably the same person as the authoritative source.
- Identity-bearing details remain stable unless explicitly requested otherwise: facial geometry, eyes, eyebrows, nose, mouth, jaw, ears, glasses, hairline, expression, pose, body geometry, clothing geometry, and visible text.
- Key-light direction, softness, height, fill ratio, background luminance, color temperature, rim light, skin tone, clothing reflectance, perspective, depth of field, crop, and edges form one plausible photograph.
- Low-key work uses local light-and-shadow structure, not global underexposure. Lit facial planes remain properly exposed while shadow planes fall naturally darker.
- There are no obvious generated artifacts: false pores, mottling, freckles, blemishes, waxy skin, HDR texture, warped glasses, inconsistent eyes, malformed ears, broken text, haloed hair, glowing outlines, or background seams.
- Fine hair and semi-transparent edges blend naturally against the intended background.
- The agent has visually compared the final image with the source and at least one baseline or rejected candidate, unless one-shot completion is clearly justified.
- Final artifacts and provenance exist locally.

## Photographic Review

Review the image at normal size and zoom into the face, eyes, glasses, hairline, ears, mouth, jaw, clothing text, and background edges. When candidates differ materially, create a contact sheet.

Ask whether the scene could have been photographed this way. Check light source direction, catchlights, shadow continuity, subject-background separation, color spill, highlight rolloff, and whether clothing and skin respond to the same environment.

The most attractive candidate is not automatically the winner. Prefer identity and photographic credibility over stronger style.

## Useful CLI Operations

Generative edit:

```bash
genai-portrait edit --provider gemini \
  --input portrait.jpg \
  --prompt-file prompt.txt \
  --output-dir runs/candidate-a
```

Multi-image lighting or environment transfer:

```bash
genai-portrait edit --provider openai \
  --input identity-source.jpg \
  --input lighting-reference.png \
  --prompt-file transfer.txt \
  --output-dir runs/candidate-b
```

The first image must be declared in the prompt as the sole identity and geometry authority. Reference images may influence only the explicitly requested property.

Apply alpha without changing RGB:

```bash
genai-portrait apply-alpha --image relit.png --mask matte.png --output runs/final/final.png
```

Compare candidates:

```bash
genai-portrait inspect source.jpg candidate-a.png candidate-b.png --output runs/review/comparison.jpg
```

## Default Strategy For Difficult Environment Changes

For a demanding transformation such as a bright white-background headshot to a dark studio portrait, a useful default is:

- Let Gemini explore a coherent lighting concept.
- Reject it as final if identity drifts.
- Give GPT the original portrait first and the Gemini result second, asking GPT to transfer only lighting and environment while treating the original as the sole identity authority.
- Apply a reviewed mask or alpha channel only after the RGB edit is accepted.

This is a recommendation, not a mandatory pipeline. Stop early if a candidate already passes. Switch models or restart from the original when the observed failure calls for it.

## Known Failure Modes

Repeated GPT edits can accumulate false high-frequency skin texture. If pores, mottling, spots, grain, or dirty HDR-like skin appear, do not keep editing that candidate. Restart from the original or the cleanest earlier source.

Gemini can create coherent lighting while changing age, facial proportions, eyes, hairline, glasses, or expression. A polished Gemini candidate still fails if it looks like a sibling rather than the same person.

Multi-image edits can blend identities. The identity image must be the sole authority. A lighting reference may contribute light direction, ratio, exposure, rim light, background tone, and color grade, but not facial or body geometry.

A hard silhouette mask can remove fine hair; a broad feather can create a visible halo. Inspect edge behavior on the actual target background. Let the agent choose matting, backing-plate, regeneration, or another strategy based on the visible failure.

## Retry And Stop Rules

Retry from the original when identity drifts, skin texture becomes synthetic, glasses warp, text breaks, or edges become contaminated. Narrow the prompt when identity is intact but the requested change is weak. Switch strategy after repeated failures of the same kind.

As a default budget, try two to four materially different attempts. More attempts are justified only when testing a new hypothesis. Stop when the best candidate passes and further edits are more likely to trade identity for style.

## Privacy

Treat real portraits as private data. Store run artifacts in ignored local directories. Do not commit user portraits, private prompts, raw payloads, API keys, or absolute private paths. Public examples must use synthetic or appropriately licensed subjects.
