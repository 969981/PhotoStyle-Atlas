# Evidence ledger

The ledger makes it possible to hide source labels from the artwork without losing traceability.

## Claim classes

| Status | Meaning | Allowed public wording |
|---|---|---|
| `verified` | Directly supported by a primary or authoritative source | State as fact with the correct scope/date |
| `inferred` | Reasonable calculation or interpretation from verified material | Use “roughly”, “suggests”, or explain the inference |
| `subjective` | Supplied personal view or attributed review pattern | Frame as experience/opinion, not universal fact |
| `unknown` | Missing, conflicting, or too unstable to confirm | Omit or label the uncertainty |

## Source priority

For current course, product, policy, price, or schedule facts:

1. official current page, handbook, specification, or dataset
2. official archived document for the relevant year
3. trustworthy secondary source with a visible date
4. public reviews only for clearly attributed sentiment patterns

Use reviews to understand friction and fit, not to manufacture consensus. Paraphrase; do not copy long review text.

## Required `evidence.json` shape

```json
{
  "schema_version": "1.0",
  "as_of": "YYYY-MM-DD",
  "public_source_labels": false,
  "claims": [
    {
      "id": "claim-001",
      "text": "Coursework contributes 40% of the final mark.",
      "status": "verified",
      "source_title": "Official course descriptor",
      "source_uri": "https://example.edu/course",
      "source_date": "YYYY-MM-DD",
      "locator": "Assessment section",
      "notes": "Applies to 2026/27 only."
    }
  ]
}
```

For local files, use an absolute source path while working. Before publishing the project to a public repository, replace private paths with portable labels or omit the raw source files.

## Public source-label policy

`public_source_labels: false` means:

- no “Source:” line in the image
- no visible document filename or FOI identifier unless requested
- provenance still exists in `evidence.json`
- the caption may stay citation-free if the user requests it

It does not waive copyright, attribution, privacy, or platform rules. If an image, quotation, or licensed asset requires credit, preserve the required credit or do not use the asset.

## Derived values

For calculated percentages, averages, rankings, or trends, store:

- input claim IDs
- formula or transformation
- rounding rule
- output value
- scope and time period

Never calculate from values that refer to different cohorts or academic years without explicitly reconciling them.

## Evidence-to-copy handoff

Every factual sentence in `caption.md` should be traceable to one or more claim IDs during drafting. Claim IDs do not need to appear in the final caption.

Useful phrasing:

- verified: “The current assessment split is 40/60.”
- inferred: “That usually makes the module feel less exam-only than it first appears.”
- subjective: “If you enjoy building something concrete, this is likely the better fit.”
- unknown: “The teaching pattern can change by year, so check the latest handbook before choosing.”
