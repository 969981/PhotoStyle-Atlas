#!/usr/bin/env python3
"""Validate portable packaging, state templates, links, and generated output."""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    "SKILL.md",
    "LICENSE",
    "agents/openai.yaml",
    "assets/series-lock.template.yaml",
    "assets/poster-manifest.template.yaml",
    "references/style-presets.md",
    "references/series-lock.md",
    "references/poster-design-rules.md",
    "scripts/build-standalone.py",
    "scripts/migrate-series-lock.py",
    "dist/standalone/SKILL.md",
    "docs/install-agent-skills.md",
    "docs/install-codex.md",
    "docs/install-trae.md",
)
CORE_TEXT = (
    "SKILL.md",
    "references/style-presets.md",
    "references/series-lock.md",
    "references/poster-design-rules.md",
)
PROTOCOL_MARKERS = (
    "museum-ivory-v1",
    "3:2",
    "50:50",
    "#F3EBDD",
    "five",
    "four",
    "poster manifest",
)
PALETTE_ROLES = {"subject", "dark-anchor", "natural", "sky-or-water", "accent"}
MOTIF_ROLES = {"primary-structure", "secondary-structure", "organic", "spatial"}


def load_yaml(path: Path) -> Any:
    return yaml.safe_load(path.read_text(encoding="utf-8"))


def frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    match = re.match(r"\A---\n(.*?)\n---\n", text, flags=re.DOTALL)
    if not match:
        raise ValueError(f"Missing frontmatter: {path}")
    data = yaml.safe_load(match.group(1))
    if not isinstance(data, dict):
        raise ValueError(f"Invalid frontmatter mapping: {path}")
    return data


def validate_links(relative: str, errors: list[str]) -> None:
    path = ROOT / relative
    text = path.read_text(encoding="utf-8")
    for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", text):
        if target.startswith(("http://", "https://", "#")):
            continue
        clean = target.split("#", 1)[0]
        if clean and not (path.parent / clean).resolve().exists():
            errors.append(f"Broken link in {relative}: {target}")


def load_builder():
    path = ROOT / "scripts" / "build-standalone.py"
    spec = importlib.util.spec_from_file_location("build_standalone", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def validate() -> list[str]:
    errors: list[str] = []
    for relative in REQUIRED:
        if not (ROOT / relative).is_file():
            errors.append(f"Missing required file: {relative}")
    if errors:
        return errors

    root_meta = frontmatter(ROOT / "SKILL.md")
    standalone_meta = frontmatter(ROOT / "dist" / "standalone" / "SKILL.md")
    if root_meta.get("name") != ROOT.name:
        errors.append("Frontmatter name must match the skill folder name.")
    if not isinstance(root_meta.get("description"), str) or len(root_meta["description"]) > 1024:
        errors.append("description must be a string of at most 1024 characters.")
    if root_meta.get("license") != "MIT":
        errors.append("license must be MIT.")
    if root_meta.get("metadata", {}).get("version") != "1.2.0":
        errors.append("metadata.version must be 1.2.0.")
    if standalone_meta != root_meta:
        errors.append("Standalone frontmatter differs from root SKILL.md.")

    lock = load_yaml(ROOT / "assets" / "series-lock.template.yaml")
    manifest = load_yaml(ROOT / "assets" / "poster-manifest.template.yaml")
    if (lock.get("document_type"), lock.get("schema_version")) != ("series-lock", 2):
        errors.append("Series lock template must be document_type series-lock, schema_version 2.")
    if (manifest.get("document_type"), manifest.get("schema_version")) != ("poster-manifest", 1):
        errors.append("Poster manifest template must be document_type poster-manifest, schema_version 1.")
    if "resolved_palette" in lock.get("palette", {}) or "resolved_motifs" in lock.get("abstraction", {}):
        errors.append("Series lock must not contain poster-specific resolved values.")
    if set(lock.get("palette", {}).get("roles", [])) != PALETTE_ROLES:
        errors.append("Series lock palette roles do not match museum-ivory-v1.")
    if set(lock.get("abstraction", {}).get("motif_roles", [])) != MOTIF_ROLES:
        errors.append("Series lock motif roles do not match museum-ivory-v1.")
    if set(manifest.get("resolved_palette", {})) != PALETTE_ROLES:
        errors.append("Poster manifest must expose exactly five resolved palette roles.")
    if set(manifest.get("resolved_motifs", {})) != MOTIF_ROLES:
        errors.append("Poster manifest must expose exactly four resolved motif roles.")
    if "path" in manifest.get("source", {}):
        errors.append("Poster manifest source must not contain a local path field.")

    for relative in (
        *CORE_TEXT,
        "README.md",
        "README.zh-CN.md",
        "docs/install-agent-skills.md",
        "docs/install-codex.md",
        "docs/install-trae.md",
    ):
        validate_links(relative, errors)

    core = "\n".join((ROOT / path).read_text(encoding="utf-8") for path in CORE_TEXT)
    for forbidden in ("image_gen__imagegen", "mcp__", "codex.exec", "trae."):
        if forbidden.lower() in core.lower():
            errors.append(f"Platform-private tool name in portable core: {forbidden}")
    if re.search(r"(?:[A-Za-z]:\\|/Users/|/home/)", core):
        errors.append("Local absolute path found in portable core.")

    standalone = (ROOT / "dist" / "standalone" / "SKILL.md").read_text(encoding="utf-8")
    expected = load_builder().build_text()
    if standalone.replace("\r\n", "\n") != expected:
        errors.append("Standalone output is stale; run scripts/build-standalone.py.")
    for marker in PROTOCOL_MARKERS:
        if marker.lower() not in standalone.lower():
            errors.append(f"Standalone is missing protocol marker: {marker}")
    for target in re.findall(r"\[[^\]]+\]\(([^)]+)\)", standalone):
        if not target.startswith(("http://", "https://", "#")):
            errors.append(f"Standalone has unresolved relative link: {target}")
    return errors


def main() -> int:
    try:
        errors = validate()
    except (OSError, UnicodeError, yaml.YAMLError, ValueError) as exc:
        errors = [str(exc)]
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print("Portable skill validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
