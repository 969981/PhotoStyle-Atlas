from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv


def load_environment() -> None:
    load_dotenv(Path.cwd() / ".env", override=False)


def require_api_key(provider: str) -> str:
    if provider == "gemini":
        value = os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
        name = "GEMINI_API_KEY"
    else:
        value = os.getenv("OPENAI_API_KEY")
        name = "OPENAI_API_KEY"
    if not value:
        raise RuntimeError(f"Missing {name}. Configure it in the environment before a live edit.")
    return value


def default_model(provider: str) -> str:
    if provider == "gemini":
        return os.getenv("GEMINI_PRO_IMAGE_MODEL", "gemini-3-pro-image-preview")
    return os.getenv("OPENAI_IMAGE_MODEL", "gpt-image-2")
