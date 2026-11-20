#!/usr/bin/env python3
"""Validate a Paper Signal project for structure, provenance, prompts, and images."""

from __future__ import annotations

import argparse
import json
import re
import struct
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


REQUIRED_COMMON_FILES = ("brief.md", "manifest.json")
LEGACY_PROMPT_LABELS = (
    "Use case and asset",
    "Canvas and attention geometry",
    "Text (verbatim)",
    "Typography",
    "Paper, ink, and reproduction process",
    "Constraints and avoid",
)
ALLOWED_ROUTES = {"new-series", "single-card", "restyle-existing"}
ALLOWED_STATUSES = {"draft", "planned", "prompted", "rendered", "validated"}
ALLOWED_SUBJECTS = {"landscape", "portrait", "object", "architecture", "concept", "evidence", "mixed-series"}
ALLOWED_COMPOSITIONS = {
    "airy-fragment",
    "photo-window",
    "panorama-strip",
    "dual-frame",
    "specimen-plate",
    "portrait-archive",
    "type-object",
}
CLAIM_STATUSES = {"verified", "inferred", "subjective", "unknown"}
PUBLIC_SOURCE_MARKERS = ("source:", "来源：", "来源:", "http://", "https://", "doi:", "foi")


@dataclass
class Report:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    def note(self, message: str) -> None:
        self.notes.append(message)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    parser.add_argument("--require-prompts", action="store_true")
    parser.add_argument("--require-images", action="store_true")
    parser.add_argument("--json", action="store_true", dest="json_output")
    return parser.parse_args()


def load_json(path: Path, report: Report) -> dict[str, Any] | None:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        report.error(f"missing file: {path.name}")
        return None
    except json.JSONDecodeError as exc:
        report.error(f"invalid JSON in {path.name}: {exc}")
        return None
    if not isinstance(value, dict):
        report.error(f"{path.name} must contain a JSON object")
        return None
    return value


def parse_ratio(value: Any, report: Report) -> float | None:
    if not isinstance(value, str) or not re.fullmatch(r"\d+:\d+", value):
        report.error("manifest aspect_ratio must use W:H, for example 3:4")
        return None
    width, height = (int(part) for part in value.split(":"))
    if width <= 0 or height <= 0:
        report.error("manifest aspect_ratio values must be positive")
        return None
    return width / height


def png_dimensions(path: Path) -> tuple[int, int] | None:
    with path.open("rb") as handle:
        header = handle.read(24)
    if len(header) >= 24 and header[:8] == b"\x89PNG\r\n\x1a\n":
        return struct.unpack(">II", header[16:24])
    return None


def jpeg_dimensions(path: Path) -> tuple[int, int] | None:
    with path.open("rb") as handle:
        if handle.read(2) != b"\xff\xd8":
            return None
        while True:
            byte = handle.read(1)
            if not byte:
                return None
            if byte != b"\xff":
                continue
            marker = handle.read(1)
            while marker == b"\xff":
                marker = handle.read(1)
            if marker in {b"\xd8", b"\xd9"}:
                continue
            length_bytes = handle.read(2)
            if len(length_bytes) != 2:
                return None
            length = struct.unpack(">H", length_bytes)[0]
            if marker and marker[0] in range(0xC0, 0xC4):
                payload = handle.read(5)
                if len(payload) != 5:
                    return None
                height, width = struct.unpack(">HH", payload[1:5])
                return width, height
            handle.seek(max(length - 2, 0), 1)


def image_dimensions(path: Path) -> tuple[int, int] | None:
    if path.suffix.lower() == ".png":
        return png_dimensions(path)
    if path.suffix.lower() in {".jpg", ".jpeg"}:
        return jpeg_dimensions(path)
    try:
        from PIL import Image  # type: ignore

        with Image.open(path) as image:
            return image.size
    except (ImportError, OSError):
        return None


def count_cjk(text: str) -> int:
    return len(re.findall(r"[\u3400-\u9fff]", text))


def validate_evidence(project: Path, manifest: dict[str, Any], report: Report) -> set[str]:
    evidence = load_json(project / "evidence.json", report)
    if evidence is None:
        return set()
    if evidence.get("public_source_labels") != manifest.get("public_source_labels"):
        report.error("public_source_labels differs between evidence.json and manifest.json")
    claims = evidence.get("claims")
    if not isinstance(claims, list):
        report.error("evidence claims must be a list")
        return set()
    claim_ids: set[str] = set()
    for position, claim in enumerate(claims, start=1):
        if not isinstance(claim, dict):
            report.error(f"claim {position} must be an object")
            continue
        claim_id = claim.get("id")
        if not isinstance(claim_id, str) or not claim_id:
            report.error(f"claim {position} has no id")
            continue
        if claim_id in claim_ids:
            report.error(f"duplicate claim id: {claim_id}")
        claim_ids.add(claim_id)
        if claim.get("status") not in CLAIM_STATUSES:
            report.error(f"claim {claim_id} has invalid status")
        if claim.get("status") == "verified" and not claim.get("source_title"):
            report.error(f"verified claim {claim_id} has no source_title")
        if claim.get("status") == "unknown":
            report.warn(f"claim {claim_id} remains unknown")
    return claim_ids


def validate_card(
    project: Path,
    card: dict[str, Any],
    position: int,
    expected_ratio: float | None,
    claim_ids: set[str],
    require_prompts: bool,
    require_images: bool,
    public_source_labels: bool,
    report: Report,
) -> None:
    if card.get("index") != position:
        report.error(f"card at position {position} must have index {position}")
    role = card.get("role")
    if not isinstance(role, str) or not role:
        report.error(f"card {position} has no role")

    on_card_text = card.get("on_image_text", card.get("on_card_text", []))
    if not isinstance(on_card_text, list) or not all(isinstance(item, str) for item in on_card_text):
        report.error(f"card {position} on_card_text must be a list of strings")
        on_card_text = []
    cjk_total = sum(count_cjk(item) for item in on_card_text)
    if cjk_total > 70:
        report.warn(f"card {position} carries {cjk_total} CJK characters; move prose to caption.md")
    if role == "cover" and cjk_total > 30:
        report.warn(f"cover card {position} has a high text burden")
    if not public_source_labels:
        joined = " ".join(on_card_text).lower()
        if any(marker in joined for marker in PUBLIC_SOURCE_MARKERS):
            report.warn(f"card {position} appears to expose a source label while policy is hidden")

    for claim_id in card.get("claim_ids", []):
        if claim_id not in claim_ids:
            report.error(f"card {position} references unknown claim id: {claim_id}")

    prompt_value = card.get("prompt")
    prompt_path = project / str(prompt_value) if prompt_value else None
    if not prompt_path or not prompt_path.is_file():
        if require_prompts:
            report.error(f"missing prompt for card {position}: {prompt_value}")
        else:
            report.warn(f"prompt not written yet for card {position}: {prompt_value}")
    else:
        prompt_text = prompt_path.read_text(encoding="utf-8")
        paragraphs = [part.strip() for part in re.split(r"\n\s*\n", prompt_text.strip()) if part.strip()]
        if len(paragraphs) != 4:
            report.error(f"prompt for card {position} must contain exactly four compact paragraphs")
        if prompt_text.lstrip().startswith("---"):
            report.error(f"prompt for card {position} contains YAML; keep metadata in manifest.json")
        if any(label in prompt_text for label in LEGACY_PROMPT_LABELS):
            report.error(f"prompt for card {position} contains planning labels instead of the final image prompt")
        lower_prompt = prompt_text.lower()
        if not any(
            term in lower_prompt
            for term in ("aged paper", "aged-paper", "scanned paper", "scanned-page", "old paper", "旧纸", "老纸")
        ):
            report.warn(f"prompt for card {position} does not explicitly require aged/scanned paper")
        if not re.search(r"\b\d{1,2}(?:\.\d+)?%", lower_prompt):
            report.warn(f"prompt for image {position} does not quantify its paper, image, or color-area geometry")
        if len(prompt_text) > 4200:
            report.warn(f"prompt for card {position} is long; compile only pixel-relevant instructions")
        for literal in on_card_text:
            if literal and literal not in prompt_text:
                report.error(f"prompt for card {position} omits exact text: {literal!r}")

    output_value = card.get("output")
    output_path = project / str(output_value) if output_value else None
    if not output_path or not output_path.is_file():
        if require_images:
            report.error(f"missing output for card {position}: {output_value}")
        else:
            report.warn(f"image not rendered yet for card {position}: {output_value}")
        return

    dimensions = image_dimensions(output_path)
    if dimensions is None:
        report.warn(f"could not inspect dimensions for {output_path.name}")
        return
    width, height = dimensions
    if width <= 0 or height <= 0:
        report.error(f"invalid dimensions for {output_path.name}")
    elif expected_ratio is not None and abs((width / height) - expected_ratio) > 0.025:
        report.error(
            f"wrong aspect ratio for {output_path.name}: {width}x{height}, expected near {expected_ratio:.3f}"
        )


def validate_project(project: Path, require_prompts: bool = False, require_images: bool = False) -> Report:
    report = Report()
    project = project.expanduser().resolve()
    if not project.is_dir():
        report.error(f"project directory does not exist: {project}")
        return report
    for filename in REQUIRED_COMMON_FILES:
        if not (project / filename).is_file():
            report.error(f"missing required file: {filename}")

    manifest = load_json(project / "manifest.json", report)
    if manifest is None:
        return report
    schema_version = manifest.get("schema_version")
    if schema_version not in {"1.0", "1.1"}:
        report.error("manifest schema_version must be 1.0 or 1.1")
    if manifest.get("route") not in ALLOWED_ROUTES:
        report.error("manifest route is invalid")
    if schema_version == "1.1" and manifest.get("subject_route") not in ALLOWED_SUBJECTS:
        report.error("manifest subject_route is invalid")
    status = manifest.get("status")
    if status not in ALLOWED_STATUSES:
        report.error("manifest status is invalid")
    if status in {"prompted", "rendered", "validated"}:
        require_prompts = True
    if status in {"rendered", "validated"}:
        require_images = True

    project_meta = manifest.get("project")
    if not isinstance(project_meta, dict):
        report.error("manifest project must be an object")
    else:
        slug = project_meta.get("slug")
        if not isinstance(slug, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+){1,4}", slug):
            report.error("project slug must contain 2-5 lowercase kebab-case words")

    expected_ratio = parse_ratio(manifest.get("aspect_ratio"), report)
    public_source_labels = manifest.get("public_source_labels")
    if not isinstance(public_source_labels, bool):
        report.error("manifest public_source_labels must be boolean")
        public_source_labels = False

    claim_ids = (
        validate_evidence(project, manifest, report)
        if (project / "evidence.json").is_file()
        else set()
    )
    if manifest.get("route") == "new-series":
        for filename in ("analysis.md", "outline.md"):
            if not (project / filename).is_file():
                report.error(f"missing required series file: {filename}")
    if manifest.get("route") == "restyle-existing" and not (project / "preservation.md").is_file():
        report.error("missing required restyle file: preservation.md")

    cards = manifest.get("images", manifest.get("cards"))
    if not isinstance(cards, list) or not cards:
        report.error("manifest cards must be a non-empty list")
        return report
    if len(cards) > 10:
        report.error("manifest cannot contain more than 10 cards")

    prompt_paths: set[str] = set()
    output_paths: set[str] = set()
    layout_families: list[str] = []
    for position, card in enumerate(cards, start=1):
        if not isinstance(card, dict):
            report.error(f"card {position} must be an object")
            continue
        prompt_value = str(card.get("prompt", ""))
        output_value = str(card.get("output", ""))
        if prompt_value in prompt_paths:
            report.error(f"duplicate prompt path: {prompt_value}")
        if output_value in output_paths:
            report.error(f"duplicate output path: {output_value}")
        prompt_paths.add(prompt_value)
        output_paths.add(output_value)
        mode = card.get("composition_mode", card.get("layout_family"))
        if isinstance(mode, str):
            layout_families.append(mode)
        if schema_version == "1.1" and mode not in ALLOWED_COMPOSITIONS:
            report.error(f"image {position} has invalid composition_mode: {mode}")
        if schema_version == "1.1" and card.get("subject_route") not in ALLOWED_SUBJECTS:
            report.error(f"image {position} has invalid subject_route")
        validate_card(
            project,
            card,
            position,
            expected_ratio,
            claim_ids,
            require_prompts,
            require_images,
            public_source_labels,
            report,
        )

    if len(cards) >= 5 and len(set(layout_families)) < 3:
        report.warn("five-image series uses fewer than three composition modes")
    for left, right, third in zip(layout_families, layout_families[1:], layout_families[2:]):
        if left == right == third:
            report.warn(f"three consecutive images reuse composition mode: {left}")
            break

    if not report.errors:
        report.note(f"validated {len(cards)} image(s)")
    return report


def emit(report: Report, json_output: bool) -> None:
    if json_output:
        print(json.dumps({"errors": report.errors, "warnings": report.warnings, "notes": report.notes}, indent=2))
        return
    for label, values in (("ERROR", report.errors), ("WARN", report.warnings), ("NOTE", report.notes)):
        for value in values:
            print(f"{label}: {value}")
    print(f"SUMMARY: {len(report.errors)} error(s), {len(report.warnings)} warning(s)")


def main() -> int:
    args = parse_args()
    report = validate_project(args.project, args.require_prompts, args.require_images)
    emit(report, args.json_output)
    return 1 if report.errors else 0


if __name__ == "__main__":
    sys.exit(main())
