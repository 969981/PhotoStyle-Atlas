from __future__ import annotations

import base64
from contextlib import ExitStack
import mimetypes
from pathlib import Path
from typing import Any


def edit_openai(api_key: str, model: str, inputs: list[Path], prompt: str, output: Path, size: str) -> None:
    from openai import OpenAI

    client = OpenAI(api_key=api_key)
    with ExitStack() as stack:
        handles = [stack.enter_context(path.open("rb")) for path in inputs]
        result = client.images.edit(
            model=model,
            image=handles,
            prompt=prompt,
            quality="high",
            output_format="png",
            extra_body={"size": size},
        )
    encoded = result.data[0].b64_json
    if not encoded:
        raise RuntimeError("OpenAI returned no image data")
    output.write_bytes(base64.b64decode(encoded))


def edit_gemini(api_key: str, model: str, inputs: list[Path], prompt: str, output: Path, size: str) -> None:
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)
    contents: list[Any] = [prompt]
    for path in inputs:
        contents.append(types.Part.from_bytes(data=path.read_bytes(), mime_type=_mime_type(path)))
    response = client.models.generate_content(
        model=model,
        contents=contents,
        config=types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"],
            image_config=types.ImageConfig(
                image_size=_gemini_size(size),
                aspect_ratio=_aspect_ratio(size),
            ),
        ),
    )
    for candidate in response.candidates or []:
        for part in candidate.content.parts or []:
            if part.inline_data and part.inline_data.data:
                output.write_bytes(part.inline_data.data)
                return
    raise RuntimeError("Gemini returned no image data")


def _mime_type(path: Path) -> str:
    mime_type, _ = mimetypes.guess_type(path)
    if mime_type not in {"image/jpeg", "image/png", "image/webp"}:
        raise ValueError(f"Unsupported Gemini input image type: {path.suffix or '<none>'}")
    return mime_type


def _gemini_size(size: str) -> str:
    edge = int(size.split("x", maxsplit=1)[0])
    if edge >= 3000:
        return "4K"
    if edge >= 1800:
        return "2K"
    return "1K"


def _aspect_ratio(size: str) -> str:
    width, height = (int(value) for value in size.lower().split("x", maxsplit=1))
    if width <= 0 or height <= 0:
        raise ValueError("Image dimensions must be positive")
    from math import gcd

    divisor = gcd(width, height)
    return f"{width // divisor}:{height // divisor}"
