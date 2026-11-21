from __future__ import annotations

import shutil
from pathlib import Path

from .artifacts import write_manifest
from .config import default_model, require_api_key
from .providers import edit_gemini, edit_openai


def edit(
    provider: str,
    input_paths: list[Path],
    prompt: str,
    output_dir: Path,
    model: str | None = None,
    size: str = "2048x2048",
) -> Path:
    if not input_paths:
        raise ValueError("At least one --input image is required")
    for path in input_paths:
        if not path.is_file():
            raise FileNotFoundError(path)
    run_dir = output_dir.resolve()
    input_dir = run_dir / "inputs"
    prompt_dir = run_dir / "prompts"
    output_subdir = run_dir / "outputs"
    for directory in (input_dir, prompt_dir, output_subdir):
        directory.mkdir(parents=True, exist_ok=True)

    copied_inputs: list[Path] = []
    for index, path in enumerate(input_paths, start=1):
        copied = input_dir / f"{index:02d}_{path.name}"
        shutil.copy2(path, copied)
        copied_inputs.append(copied)
    prompt_path = prompt_dir / "prompt.txt"
    prompt_path.write_text(prompt.rstrip() + "\n", encoding="utf-8")
    output_path = output_subdir / "candidate.png"
    selected_model = model or default_model(provider)
    key = require_api_key(provider)
    if provider == "gemini":
        edit_gemini(key, selected_model, copied_inputs, prompt, output_path, size)
    else:
        edit_openai(key, selected_model, copied_inputs, prompt, output_path, size)
    write_manifest(run_dir, provider, selected_model, copied_inputs, prompt_path, output_path)
    return output_path
