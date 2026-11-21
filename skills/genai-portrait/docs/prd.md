# Product Requirements

## Product

GenAI Portrait Skill is an AI-agent capability for editing portraits and headshots while preserving the source person's identity and making the complete photograph visually coherent.

## Users

- People adapting phone portraits into professional headshots.
- Agents preparing white, neutral, or dark-background portraits for websites and documents.
- People requesting portrait-specific changes such as cleanup, reframing, wardrobe edits, restrained face-shape changes, or ID-photo formatting.
- Developers who need inspectable local artifacts rather than a one-shot image API response.

## Problem

Literal image edits often fail at the photographic level. Cutting a brightly lit white-background portrait onto black can preserve the subject outline while still looking fake because the original key light, fill, edge contamination, color temperature, and contrast belong to the former environment.

A capable portrait editor must reason about the whole photograph. The requested local edit is only one input to the actual task. Large changes require the subject, background, lighting, color, optics, and edges to remain mutually plausible.

## Scope

The product covers portrait and headshot edits, including:

- Background creation, replacement, cleanup, and adaptation.
- Relighting and environment-aware color grading.
- White-background and dark-background professional portraits.
- ID-photo and profile-photo preparation.
- Crop, composition, and aspect-ratio adaptation.
- Clothing and grooming cleanup.
- Restrained appearance edits requested by the user.
- Masks, alpha-channel outputs, contact sheets, and review artifacts.

It is not a general-purpose image generator, biometric verification system, or deterministic face-retouching engine.

Official ID-photo work is specification-driven. The agent must use the named authority's current rules for crop, head size, eye position, background, expression, eyewear, dimensions, resolution, and format. Appearance changes beyond neutral cleanup require explicit user intent; the product must not introduce unsolicited face, age, body, skin-tone, ethnicity-associated, gender-expression, or medical changes.

## Expert Behavior

The agent must not reduce a large portrait transformation to the user's most literal instruction. It should infer the photographic consequences of the requested change and address them when necessary.

For example, moving a portrait from white to black may require new subject lighting, lower fill, changed edge separation, background-spill removal, and a different contrast ratio. Merely replacing background pixels does not satisfy the request if the result still looks photographed for the old environment.

The agent should preserve user intent while using professional photographic judgment. It should avoid unrequested identity changes and should explain material trade-offs through artifacts rather than lengthy process narration.

## Success Criteria

- The result remains unmistakably the same person unless identity change is explicitly requested.
- The requested edit is visibly present.
- Lighting direction, light ratio, background luminance, color temperature, rim light, skin tone, clothing response, perspective, depth of field, crop, and edge behavior form a plausible photograph.
- The image contains no obvious generated skin texture, identity drift, malformed glasses, broken text, haloed hair, false rim light, or background seams.
- A vision-capable agent has compared the result with the source and can state why the candidate passes.
- Outputs are local, inspectable, and accompanied by provenance.

## Privacy

Portraits can be sensitive biometric data. The default product is local-artifact-first, has no telemetry, does not commit user inputs, and uses only synthetic subjects in public examples.
