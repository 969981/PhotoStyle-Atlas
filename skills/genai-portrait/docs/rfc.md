# Architecture RFC

## Design Thesis

Reliability comes from a visual execution-review-correction loop, not from a fixed prompt recipe. The repository provides composable tools and a result-oriented skill. A vision-capable agent drives both.

## Responsibility Boundary

Generative providers own semantic RGB edits such as relighting, appearance edits, background synthesis, and wardrobe changes.

Local Python owns deterministic artifact work: input validation, provider request assembly, masks, alpha-channel application, manifests, hashes, metadata handling, previews, and contact sheets. Local code must not silently relight or color-grade the subject.

## Planned Components

- A Python package under `src/genai_portrait/`.
- A stable `genai-portrait` console command.
- Provider adapters for Gemini and OpenAI image models.
- Multi-image editing so one image can be authoritative for identity while another supplies lighting or environmental reference.
- Deterministic alpha compositing and inspection commands.
- A manifest for every run with relative paths, input hashes, model information, prompt provenance, artifacts, and Python-processing declarations.
- One canonical root skill that defines visual acceptance criteria and lets the agent choose the workflow.

## Recommended Strategy, Not Mandatory Pipeline

Experiments show a useful default for difficult white-to-dark portrait adaptation:

- Gemini can explore a coherent lighting design but may drift facial identity.
- GPT may preserve identity better when given the original portrait plus a separate lighting reference.
- Repeatedly editing generated portraits can accumulate false pores, mottling, freckles, and high-frequency texture artifacts.

An agent may therefore use Gemini to produce a lighting reference and GPT multi-image editing to transfer that lighting onto the original identity source. This is a strong default, not a required sequence. If the Gemini candidate already preserves identity and passes visual review, further generation may reduce quality. If a different model or a single edit passes, the agent should stop.

## Photographic Coherence Model

For material edits, the agent should review the complete image system:

- Key-light direction, size, softness, and height.
- Fill level and lighting ratio rather than global brightness alone.
- Background luminance, color, and distance from the subject.
- Hair and shoulder separation without artificial glowing outlines.
- Skin-tone continuity and highlight rolloff.
- Clothing reflectance and readable but plausible detail.
- Perspective, focal-length cues, depth of field, crop, and headroom.
- Edge spill, semi-transparent hair, glasses, and fine contours.

The agent should treat these as coupled variables. A background change can imply a lighting change; a face-shape edit can imply shadow and contour changes; a crop can alter visual balance and headroom.

## Provider Boundary

Provider SDKs will be imported lazily so offline tests and CLI help never contact external services. Credentials come from environment variables. The package will not contain private credential routing.

## Public Artifact Policy

Run directories are ignored by default. Public demonstrations use synthetic people. Raw API payloads, image base64, private absolute paths, and secret material are never written to committed manifests.
