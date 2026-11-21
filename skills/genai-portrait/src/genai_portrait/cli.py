from __future__ import annotations

import argparse
from pathlib import Path
from typing import Sequence

from .compositing import apply_alpha
from .config import load_environment
from .core import edit
from .inspection import contact_sheet


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="genai-portrait", description="Agent-driven portrait editing tools")
    commands = parser.add_subparsers(dest="command", required=True)

    edit_parser = commands.add_parser("edit", help="Run a generative portrait edit")
    edit_parser.add_argument("--provider", choices=["gemini", "openai"], required=True)
    edit_parser.add_argument("--input", action="append", type=Path, required=True)
    prompt_group = edit_parser.add_mutually_exclusive_group(required=True)
    prompt_group.add_argument("--prompt")
    prompt_group.add_argument("--prompt-file", type=Path)
    edit_parser.add_argument("--output-dir", type=Path, required=True)
    edit_parser.add_argument("--model")
    edit_parser.add_argument("--size", default="2048x2048")

    alpha_parser = commands.add_parser("apply-alpha", help="Apply a grayscale mask without changing RGB")
    alpha_parser.add_argument("--image", type=Path, required=True)
    alpha_parser.add_argument("--mask", type=Path, required=True)
    alpha_parser.add_argument("--output", type=Path, required=True)

    inspect_parser = commands.add_parser("inspect", help="Build a visual comparison sheet")
    inspect_parser.add_argument("images", nargs="+", type=Path)
    inspect_parser.add_argument("--output", type=Path, required=True)
    inspect_parser.add_argument("--tile-size", type=int, default=640)
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "apply-alpha":
        apply_alpha(args.image, args.mask, args.output)
        print(args.output)
        return 0
    if args.command == "inspect":
        contact_sheet(args.images, args.output, args.tile_size)
        print(args.output)
        return 0

    load_environment()
    prompt = args.prompt_file.read_text(encoding="utf-8") if args.prompt_file else args.prompt
    output = edit(args.provider, args.input, prompt, args.output_dir, args.model, args.size)
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
