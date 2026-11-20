#!/usr/bin/env python3
"""Migrate a legacy schema_version 1 mixed series lock without overwriting files."""

from __future__ import annotations

import argparse
import copy
import hashlib
import sys
from pathlib import Path
from typing import Any

import yaml


SUPPORTED_PRESET = "museum-ivory-v1"
SERIES_KEYS = (
    "canvas",
    "input_normalization",
    "poster_layout",
    "background",
    "palette",
    "abstraction",
    "typography",
)


class MigrationError(Exception):
    """Raised when migration cannot be completed safely."""


def load_yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, yaml.YAMLError) as exc:
        raise MigrationError(f"Cannot read YAML: {exc}") from exc
    if not isinstance(data, dict):
        raise MigrationError("The input must be a YAML mapping.")
    return data


def deep_fill(target: dict[str, Any], defaults: dict[str, Any], prefix: str, restored: list[str]) -> None:
    for key, value in defaults.items():
        field = f"{prefix}.{key}" if prefix else key
        if key not in target:
            target[key] = copy.deepcopy(value)
            restored.append(field)
        elif isinstance(value, dict) and isinstance(target[key], dict):
            deep_fill(target[key], value, field, restored)


def migrate(legacy: dict[str, Any], template: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any] | None, dict[str, Any]]:
    if legacy.get("document_type") is not None:
        raise MigrationError("Input already has document_type and is not a legacy mixed lock.")
    if legacy.get("schema_version") != 1:
        raise MigrationError("Only legacy schema_version: 1 is supported.")
    if legacy.get("preset_id") != SUPPORTED_PRESET:
        raise MigrationError(f"Unsupported preset_id: {legacy.get('preset_id')!r}.")

    lock = {
        "document_type": "series-lock",
        "schema_version": 2,
        "preset_id": SUPPORTED_PRESET,
    }
    restored: list[str] = []
    for key in SERIES_KEYS:
        if key in legacy:
            lock[key] = copy.deepcopy(legacy[key])

    palette = lock.get("palette", {})
    abstraction = lock.get("abstraction", {})
    typography = lock.get("typography", {})
    resolved_palette = palette.pop("resolved_palette", None) if isinstance(palette, dict) else None
    resolved_motifs = abstraction.pop("resolved_motifs", None) if isinstance(abstraction, dict) else None
    resolved_title = typography.pop("resolved_title", None) if isinstance(typography, dict) else None
    resolved_year = typography.pop("resolved_year", None) if isinstance(typography, dict) else None
    crop_log = copy.deepcopy(legacy.get("crop_log", []))

    deep_fill(lock, template, "", restored)
    lock["document_type"] = "series-lock"
    lock["schema_version"] = 2

    has_runtime = any(
        value not in (None, {}, [])
        for value in (resolved_palette, resolved_motifs, resolved_title, resolved_year, crop_log)
    )
    manifest = None
    if has_runtime:
        manifest = {
            "document_type": "poster-manifest",
            "schema_version": 1,
            "source": {"label": "legacy-import", "orientation": None},
            "series": {"preset_id": SUPPORTED_PRESET, "lock_schema_version": 2},
            "crop": {
                "target_ratio": lock["input_normalization"]["target_photo_ratio"],
                "description": None,
                "protected_content": [],
                "discarded_secondary_content": [],
            },
            "resolved_palette": resolved_palette or {},
            "resolved_motifs": resolved_motifs or {},
            "typography": {"title": resolved_title, "year": resolved_year},
            "generation": {"status": "legacy-import", "retry_count": 0, "retry_defect": None},
            "quality_checks": {},
            "notes": [],
        }
        if crop_log:
            manifest["notes"].append({"legacy_crop_log": crop_log})
            if len(crop_log) > 1:
                manifest["notes"].append(
                    "Multiple legacy crop entries could not be assigned to individual poster values."
                )

    known = {"schema_version", "preset_id", "crop_log", *SERIES_KEYS}
    report = {
        "migration": "legacy-series-lock-v1-to-split-state",
        "status": "success",
        "restored_from_preset": sorted(set(restored)),
        "unrecognized_top_level_fields": sorted(set(legacy) - known),
        "outputs": ["series-lock.yaml"] + (["poster-manifest.legacy-import.yaml"] if manifest else []),
    }
    return lock, manifest, report


def dump_yaml(data: dict[str, Any]) -> str:
    return yaml.safe_dump(data, sort_keys=False, allow_unicode=True, default_flow_style=False)


def write_outputs(input_path: Path, output_dir: Path) -> list[Path]:
    legacy_bytes = input_path.read_bytes()
    legacy_hash = hashlib.sha256(legacy_bytes).hexdigest()
    legacy = load_yaml(input_path)
    template_path = Path(__file__).resolve().parents[1] / "assets" / "series-lock.template.yaml"
    template = load_yaml(template_path)
    lock, manifest, report = migrate(legacy, template)
    report["source_sha256"] = legacy_hash

    targets = [output_dir / "series-lock.yaml", output_dir / "migration-report.yaml"]
    if manifest is not None:
        targets.append(output_dir / "poster-manifest.legacy-import.yaml")
    existing = [str(path) for path in targets if path.exists()]
    if existing:
        raise MigrationError("Refusing to overwrite existing output: " + ", ".join(existing))

    output_dir.mkdir(parents=True, exist_ok=True)
    payloads = [(output_dir / "series-lock.yaml", lock), (output_dir / "migration-report.yaml", report)]
    if manifest is not None:
        payloads.append((output_dir / "poster-manifest.legacy-import.yaml", manifest))
    for path, data in payloads:
        path.write_text(dump_yaml(data), encoding="utf-8", newline="\n")

    if hashlib.sha256(input_path.read_bytes()).hexdigest() != legacy_hash:
        raise MigrationError("The legacy input changed during migration.")
    return [path for path, _ in payloads]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Legacy schema_version 1 YAML file")
    parser.add_argument("--output-dir", type=Path, required=True, help="New directory for migrated files")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        outputs = write_outputs(args.input.resolve(), args.output_dir.resolve())
    except (MigrationError, OSError) as exc:
        print(f"Migration failed: {exc}", file=sys.stderr)
        return 1
    for path in outputs:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
