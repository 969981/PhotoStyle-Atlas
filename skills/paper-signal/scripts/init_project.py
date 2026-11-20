#!/usr/bin/env python3
"""Create a reproducible Paper Signal project without overwriting existing work."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path


SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+){1,4}$")
PRESETS = {
    "minimal-zine-standard": ("cobalt", "#1646B8", "photocopy-halftone", "warm gray-beige aged scanned stock"),
    "weathered-horizon": ("cyanotype-blue", "#0B4F7A", "cyanotype-newsprint", "pale stone-gray scanned stock"),
    "portrait-carbon": ("cobalt", "#1646B8", "carbon-photocopy", "soft bone copier stock"),
    "specimen-index": ("lemon-yellow", "#E2C718", "halftone-risograph", "cool gray-white scanned stock"),
    "architectural-trace": ("cyanotype-blue", "#0B4F7A", "faded-photo-photocopy", "pale stone-gray drafting stock"),
    "blue-window": ("cobalt", "#1646B8", "risograph", "warm bone scanned stock"),
    "yellow-specimen": ("lemon-yellow", "#E2C718", "halftone-risograph", "cool gray-white scanned stock"),
    "red-xerox-fragment": ("tomato-red", "#D63224", "photocopy", "cool off-white copier stock"),
    "moon-dual-panel": ("ultramarine", "#173EA5", "film-newsprint", "pale cool-gray aged stock"),
    "typewriter-map": ("cobalt", "#1646B8", "letterpress-photocopy", "gray-beige archival stock"),
}

SUBJECTS = ("landscape", "portrait", "object", "architecture", "concept", "evidence", "mixed-series")
COMPOSITIONS = {
    "airy-fragment": ("72%-88%", "10%-24%", "1%-5%"),
    "photo-window": ("50%-72%", "24%-45%", "2%-10%"),
    "panorama-strip": ("58%-78%", "18%-36%", "2%-9%"),
    "dual-frame": ("50%-72%", "22%-42%", "2%-10%"),
    "specimen-plate": ("62%-82%", "12%-34%", "1%-7%"),
    "portrait-archive": ("50%-72%", "22%-44%", "2%-10%"),
    "type-object": ("62%-84%", "12%-30%", "1%-8%"),
}
SCHEMA_BASE = "https://raw.githubusercontent.com/jiahuiqu17/paper-signal/main/schemas"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slug", help="2-5 word lowercase kebab-case project slug")
    parser.add_argument("--path", default="paper-signal", help="Parent output directory")
    parser.add_argument("--cards", type=int, default=5, help="Number of cards (1-10)")
    parser.add_argument("--title", help="Human-readable project title")
    parser.add_argument("--language", default="zh-CN")
    parser.add_argument("--platform", default="xiaohongshu")
    parser.add_argument("--ratio", default="3:4", help="Aspect ratio as W:H")
    parser.add_argument(
        "--route",
        choices=("auto", "single-card", "restyle-existing", "new-series"),
        default="auto",
    )
    parser.add_argument("--preset", choices=sorted(PRESETS), default="minimal-zine-standard")
    parser.add_argument("--subject", choices=SUBJECTS, default="concept")
    parser.add_argument("--composition", choices=("auto", *COMPOSITIONS), default="auto")
    parser.add_argument(
        "--public-source-labels",
        action="store_true",
        help="Allow visible source labels in public artwork",
    )
    return parser.parse_args()


def versioned_directory(parent: Path, slug: str) -> Path:
    candidate = parent / slug
    if not candidate.exists():
        return candidate
    suffix = datetime.now().strftime("%Y%m%d-%H%M%S")
    return parent / f"{slug}-{suffix}"


def image_role(index: int, count: int) -> str:
    if count == 1:
        return "poster"
    if index == 1:
        return "cover"
    if index == count:
        return "ending"
    return "content"


def composition_mode(index: int, count: int, subject: str, requested: str) -> str:
    if requested != "auto":
        return requested
    preferred = {
        "landscape": "panorama-strip",
        "portrait": "portrait-archive",
        "object": "specimen-plate",
        "architecture": "photo-window",
        "concept": "airy-fragment",
        "evidence": "airy-fragment",
        "mixed-series": "airy-fragment",
    }
    if count == 1:
        return preferred[subject]
    if index == 1:
        return "airy-fragment"
    if index == count:
        return "type-object"
    families = (preferred[subject], "dual-frame", "photo-window", "specimen-plate", "panorama-strip")
    return families[(index - 2) % len(families)]


def write_text(path: Path, content: str) -> None:
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def build_project(args: argparse.Namespace) -> Path:
    if not SLUG_RE.fullmatch(args.slug):
        raise ValueError("slug must contain 2-5 lowercase kebab-case words")
    if not 1 <= args.cards <= 10:
        raise ValueError("--cards must be between 1 and 10")
    if not re.fullmatch(r"\d+:\d+", args.ratio):
        raise ValueError("--ratio must use W:H, for example 3:4")

    parent = Path(args.path).expanduser().resolve()
    parent.mkdir(parents=True, exist_ok=True)
    project = versioned_directory(parent, args.slug)
    for directory in (project, project / "refs", project / "prompts", project / "outputs"):
        directory.mkdir(parents=True, exist_ok=False)

    title = args.title or args.slug.replace("-", " ").title()
    created_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    anchor_ink, anchor_hex, process, paper = PRESETS[args.preset]

    images = []
    outline_sections = []
    for index in range(1, args.cards + 1):
        role = image_role(index, args.cards)
        stem = f"{index:02d}-{role}-{args.slug}"
        mode = composition_mode(index, args.cards, args.subject, args.composition)
        images.append(
            {
                "index": index,
                "role": role,
                "slug": args.slug,
                "subject_route": args.subject,
                "composition_mode": mode,
                "prompt": f"prompts/{stem}.md",
                "output": f"outputs/{stem}.png",
                "on_image_text": [],
                "claim_ids": [],
            }
        )
        outline_sections.append(
            f"""## Card {index} — {role}
- Job:
- Takeaway:
- On-card text:
- Caption handoff:
- Subject route: {args.subject}
- Composition mode: {mode}
- Anchor form:
- Swipe reason:
"""
        )

    route = args.route if args.route != "auto" else ("single-card" if args.cards == 1 else "new-series")
    manifest = {
        "$schema": f"{SCHEMA_BASE}/project-manifest-1.1.schema.json",
        "schema_version": "1.1",
        "project": {
            "slug": args.slug,
            "title": title,
            "language": args.language,
            "created_at": created_at,
        },
        "route": route,
        "subject_route": args.subject,
        "platform": args.platform,
        "aspect_ratio": args.ratio,
        "public_source_labels": args.public_source_labels,
        "status": "planned",
        "style": {
            "preset": args.preset,
            "paper": paper,
            "process": process,
            "display_type": "small old-book serif",
            "utility_type": "typewriter microtext",
            "anchor_ink": anchor_ink,
            "anchor_hex": anchor_hex,
            "composition_mode": composition_mode(1, args.cards, args.subject, args.composition),
            "quiet_paper": COMPOSITIONS[composition_mode(1, args.cards, args.subject, args.composition)][0],
            "active_image": COMPOSITIONS[composition_mode(1, args.cards, args.subject, args.composition)][1],
            "color_area": COMPOSITIONS[composition_mode(1, args.cards, args.subject, args.composition)][2],
            "texture_intensity": "medium",
        },
        "images": images,
    }
    evidence = {
        "$schema": f"{SCHEMA_BASE}/evidence-ledger-1.0.schema.json",
        "schema_version": "1.0",
        "as_of": created_at[:10],
        "public_source_labels": args.public_source_labels,
        "claims": [],
    }

    write_text(
        project / "brief.md",
        f"""# Brief

- Title: {title}
- Platform: {args.platform}
- Language: {args.language}
- Aspect ratio: {args.ratio}
- Card count: {args.cards}
- Route: {route}
- Subject route: {args.subject}
- Composition: {args.composition}
- Public source labels: {str(args.public_source_labels).lower()}
- Preset: {args.preset}
- Anchor ink: {anchor_ink} ({anchor_hex})

## Visual thesis

[Subject / action or state / emotional tension.]

## Protected details

[Identity, horizon, pose, silhouette, geometry, exact text, values, and crop to preserve.]

## Non-negotiables

[Exact text, exclusions, reference-image roles, and output requirements.]
""",
    )
    write_text(
        project / "analysis.md",
        """# Analysis

## Post promise

[One sentence.]

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
""",
    )
    write_text(project / "outline.md", "# Outline\n\n" + "\n".join(outline_sections))
    write_text(
        project / "caption.md",
        """# Caption

[Write the publishable caption here. Keep nuance and caveats out of the bitmap.]
""",
    )
    (project / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (project / "evidence.json").write_text(
        json.dumps(evidence, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    if route == "restyle-existing":
        write_text(
            project / "preservation.md",
            """# Preservation record

- Edit target:
- Subject identity:
- Protected crop / horizon / eye line / pose / silhouette / geometry:
- Defining details:
- Exact text and values:
- Light and color invariants:
- Approved changes:
- Forbidden changes:
""",
        )
    return project


def main() -> int:
    args = parse_args()
    try:
        project = build_project(args)
    except ValueError as exc:
        raise SystemExit(f"error: {exc}") from exc
    print(project)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
