# Test Strategy

## Offline Default

The default suite must not contact Gemini, OpenAI, or any external service. It will cover CLI parsing, provider request construction, manifest generation, path safety, image inspection, and deterministic compositing.

## Unit Coverage

- Stable command contracts and helpful validation errors.
- Multi-image role ordering, especially identity source versus lighting reference.
- Relative manifest paths and content hashes.
- Alpha application without hidden RGB changes.
- Metadata and privacy behavior.
- Public repository contract, including exactly one root skill.

## Provider Integration

Provider calls will use fake clients and synthetic fixtures in normal tests. Real calls require `GENAI_PORTRAIT_ENABLE_LIVE_TESTS=1` and valid local credentials.

## Visual E2E

Automated tests cannot establish identity preservation or photographic quality. A live demonstration therefore requires a vision-capable agent to inspect source, candidates, and final output against the skill's acceptance criteria. The committed demonstration must use a synthetic subject.

## Handoff Gate

- Ruff passes.
- Offline pytest passes.
- CLI help renders without credentials.
- Privacy scan finds no private paths, real credentials, or real portraits.
- `docs/working.md` records commands and results.
