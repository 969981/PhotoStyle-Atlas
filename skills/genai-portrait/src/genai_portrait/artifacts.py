from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from PIL import Image


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def image_record(path: Path, role: str, relative_to: Path) -> dict[str, Any]:
    with Image.open(path) as image:
        width, height = image.size
        mode = image.mode
    return {
        "role": role,
        "path": path.relative_to(relative_to).as_posix(),
        "sha256": sha256(path),
        "width": width,
        "height": height,
        "mode": mode,
    }


def write_manifest(
    run_dir: Path,
    provider: str,
    model: str,
    inputs: list[Path],
    prompt_path: Path,
    output: Path,
) -> Path:
    manifest = {
        "schema_version": "1.0",
        "tool": "genai-portrait",
        "command": "edit",
        "created_at": datetime.now(timezone.utc).isoformat(),
        "provider": provider,
        "model": model,
        "inputs": [image_record(path, f"input_{index + 1}", run_dir) for index, path in enumerate(inputs)],
        "prompt": {
            "path": prompt_path.relative_to(run_dir).as_posix(),
            "sha256": sha256(prompt_path),
        },
        "artifacts": [image_record(output, "candidate", run_dir)],
        "python_processing": {
            "alpha_compositing_applied": False,
            "rgb_modified_by_python": False,
        },
    }
    path = run_dir / "manifest.json"
    path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return path
