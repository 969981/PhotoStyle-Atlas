#!/usr/bin/env python3
"""Build the deterministic single-file Agent Skill distribution."""

from __future__ import annotations

import re
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "SKILL.md"
OUTPUT = ROOT / "dist" / "standalone" / "SKILL.md"
RESOURCES = (
    ("references/style-presets.md", "markdown", "Style Presets"),
    ("references/series-lock.md", "markdown", "Portable State"),
    ("assets/series-lock.template.yaml", "yaml", "Series Lock Template"),
    ("assets/poster-manifest.template.yaml", "yaml", "Poster Manifest Template"),
    ("references/poster-design-rules.md", "markdown", "Poster Design Rules"),
)
LINK_TARGETS = {
    "references/style-presets.md": "#style-presets",
    "references/series-lock.md": "#portable-state",
    "assets/series-lock.template.yaml": "#series-lock-template",
    "assets/poster-manifest.template.yaml": "#poster-manifest-template",
    "references/poster-design-rules.md": "#poster-design-rules",
}


def split_frontmatter(text: str) -> tuple[str, str]:
    match = re.match(r"\A---\n(.*?)\n---\n(.*)\Z", text, flags=re.DOTALL)
    if not match:
        raise ValueError("SKILL.md must contain YAML frontmatter.")
    return match.group(1), match.group(2).rstrip() + "\n"


def build_text() -> str:
    source_text = SOURCE.read_text(encoding="utf-8").replace("\r\n", "\n")
    frontmatter, body = split_frontmatter(source_text)
    metadata = yaml.safe_load(frontmatter)
    version = metadata.get("metadata", {}).get("version")
    if not version:
        raise ValueError("SKILL.md metadata.version is required.")

    for relative, anchor in LINK_TARGETS.items():
        body = re.sub(
            rf"\[([^\]]+)\]\({re.escape(relative)}\)",
            rf"[\1]({anchor})",
            body,
        )

    parts = [
        "---\n" + frontmatter.rstrip() + "\n---\n",
        f"<!-- GENERATED FILE. DO NOT EDIT. Source version: {version}. -->\n\n",
        body,
    ]
    for relative, kind, title in RESOURCES:
        path = ROOT / relative
        if not path.is_file():
            raise FileNotFoundError(relative)
        content = path.read_text(encoding="utf-8").replace("\r\n", "\n").rstrip()
        parts.append(f"\n---\n\n## {title}\n\n")
        if kind == "yaml":
            parts.append(f"Source template: `{relative}`\n\n```yaml\n{content}\n```\n")
        else:
            content = re.sub(r"\A#\s+[^\n]+\n+", "", content)
            parts.append(content + "\n")

    result = "".join(parts)
    unresolved = [
        target
        for target in LINK_TARGETS
        if re.search(rf"\]\({re.escape(target)}\)", result)
    ]
    if unresolved:
        raise ValueError("Unresolved required resource links: " + ", ".join(unresolved))
    return result


def main() -> int:
    output = build_text()
    if "--stdout" in sys.argv[1:]:
        print(output, end="")
        return 0
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(output, encoding="utf-8", newline="\n")
    print(OUTPUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
