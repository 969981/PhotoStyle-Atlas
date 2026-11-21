# Working Notes

## Changelog

### 2026-07-12

- Scaffolded the public repository around portrait-wide photographic coherence rather than background replacement alone.
- Defined provider, Python-processing, privacy, documentation, and testing boundaries.
- Recorded the experimental Gemini-to-GPT lighting-transfer strategy as a recommendation rather than a fixed pipeline.
- Added the canonical result-oriented skill, multi-image provider CLI, alpha-only compositing, manifests, contact sheets, and offline tests.
- Ran the public CLI end to end on a synthetic white-background portrait: Gemini produced the lighting reference and GPT-Image-2 performed the two-image identity-authoritative transfer.
- Added the full-resolution synthetic source, intermediate reference, final output, prompts, and comparison sheet to the public demonstration.
- Validated 11 offline tests, Ruff, CLI smoke checks, Gemini live editing, OpenAI multi-image live editing, and public privacy scans.

## Lessons Learned

- Repeated GPT image edits can amplify skin texture into false pores, mottling, spots, and HDR-like artifacts. Restart from the original source instead of editing a damaged candidate.
- Gemini can produce coherent portrait lighting while changing identity-bearing facial features. A polished image must still fail if it no longer depicts the same person.
- A lighting-reference image can improve GPT results when the original portrait remains the sole identity authority.
- Low-key photography is not global darkening. It uses controlled local exposure and lighting ratio so lit planes remain correctly exposed while shadow planes fall naturally darker.
- A background replacement is often a whole-photograph transformation. Light, spill, color, clothing response, and edge separation must agree with the new environment.
- GPT-Image-2 rejects the `input_fidelity` request parameter. Preserve identity through authoritative input ordering, explicit role prompts, and visual review rather than borrowing parameters from other OpenAI image models.
