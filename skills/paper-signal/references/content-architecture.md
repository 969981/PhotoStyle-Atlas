# Series architecture

Build a sequence people can understand by swiping once, not a stack of unrelated posters.

## Start with the post promise

Write one sentence that answers:

> After viewing this post, what will the reader understand or decide more easily?

If the answer contains two unrelated outcomes, split the post.

## Caption-load budget

Score each core item before deciding how many belong in one post:

| Load | Item shape | Typical example |
|---|---|---|
| 1 | name + one recommendation | short product pick |
| 2 | two facts + one tradeoff | tool or restaurant note |
| 3 | several facts + interpretation + fit | course review, travel route, detailed comparison |

Keep the total at 9 points or fewer.

- Three courses with assessment, workload, difficulty, and fit: `3 + 3 + 3 = 9` → one post.
- Five quick recommendations with one sentence each: `1 × 5 = 5` → one post.
- Four detailed reviews: `3 × 4 = 12` → split into two posts.

This budget protects both caption length and visual clarity.

## Default five-card arc

| Card | Job | Typical content | Layout family |
|---|---|---|---|
| 1 Cover | Stop and qualify | topic + audience + promise | center-fragment / type-led |
| 2 Item 1 | Establish the reading pattern | strongest or most familiar item | lower-left-float / single-specimen |
| 3 Item 2 | Add contrast | different tradeoff or profile | dual-panel / upper-right-block |
| 4 Item 3 | Complete the choice set | surprising or niche fit | irregular-cutout / single-specimen |
| 5 Ending | Help decide | quick chooser, caveat, next-post signal | type-led / dot-orbit |

For a three-card request, use cover + compressed core + ending. For a single poster, do not force a carousel arc.

## Card contract

Each card entry in `outline.md` must contain:

- `role`
- `job`
- `one_sentence_takeaway`
- `on_card_text` as exact strings
- `caption_handoff` for nuance that stays outside the bitmap
- `layout_family`
- `anchor_form`
- `swipe_reason`

The `swipe_reason` is a narrative decision, not visible “下一页” copy by default.

## Information hierarchy

Use this order:

1. decision-worthy takeaway
2. one or two supporting facts
3. tradeoff or fit signal
4. nuance in the caption
5. provenance in the internal ledger

Do not lead with the existence of data. Lead with what the data helps the reader decide.

## `analysis.md` template

```markdown
# Analysis

## Post promise
[one sentence]

## Audience tension
- Wants:
- Worries about:
- Already knows:

## Evidence map
- Verified:
- Inferred:
- Subjective:
- Missing:

## Scope decision
- Item load:
- Total load:
- Selected items:
- Deferred items / next post:

## Visual opportunities
- Signal candidates:
- Useful comparisons:
- Avoided clichés:
```

## `outline.md` template

```markdown
# Outline

## Card 1 — cover
- Job:
- Takeaway:
- On-card text:
  - "..."
- Caption handoff:
- Layout family:
- Anchor form:
- Swipe reason:
```

## Ending without a generic CTA

Prefer a useful closing device:

- “If you want X, start with A; if you want Y, consider B.”
- “The next post will cover the three heavier options.”
- “Save this for course-registration week.”
- a compact decision tree or fit index

Avoid mandatory “like, save, follow” language. Use it only when the user wants growth copy.
