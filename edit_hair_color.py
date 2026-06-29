#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import os
from pathlib import Path

from openai import OpenAI


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Edit a photo with gpt-image-2."
    )
    parser.add_argument("image", type=Path, help="Input image path.")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("edited.png"),
        help="Output PNG path.",
    )
    parser.add_argument(
        "--prompt",
        default="",
        help="Custom edit prompt. Overrides the default hair-color prompt.",
    )
    parser.add_argument(
        "--color",
        default="strawberry blonde",
        help='Target hair color (used only when --prompt is not set).',
    )
    parser.add_argument(
        "--model",
        default="gpt-image-2",
        help="OpenAI image model to use.",
    )
    parser.add_argument(
        "--quality",
        default="medium",
        choices=("low", "medium", "high", "auto"),
        help="Image edit quality.",
    )
    parser.add_argument(
        "--output-format",
        default="png",
        choices=("png", "jpeg", "webp"),
        help="Generated image format.",
    )
    parser.add_argument(
        "--api-key-file",
        type=Path,
        help="Optional file containing the OpenAI API key. Prefer keeping it outside the repo.",
    )
    parser.add_argument(
        "--extra-instruction",
        default="",
        help="Optional extra instruction appended to the edit prompt.",
    )
    return parser.parse_args()


def read_api_key(api_key_file: Path | None) -> str | None:
    if api_key_file:
        return api_key_file.expanduser().read_text().strip()
    return os.environ.get("OPENAI_API_KEY")


def build_prompt(custom_prompt: str, color: str, extra_instruction: str) -> str:
    if custom_prompt:
        prompt = custom_prompt
    else:
        prompt = (
            "Edit this photo realistically. Change only the subject's hair color "
            f"to natural {color} with believable highlights, roots, shadows, and "
            "strand detail. Do not change eyebrows. Preserve the face, eyes, skin "
            "tone, expression, hands, jewelry, clothing, background, lighting, "
            "framing, and photo-realistic texture."
        )
    if extra_instruction:
        prompt = f"{prompt} {extra_instruction.strip()}"
    return prompt


def main() -> None:
    args = parse_args()
    image_path = args.image.expanduser()
    output_path = args.output.expanduser()

    if not image_path.is_file():
        raise SystemExit(f"Input image not found: {image_path}")

    api_key = read_api_key(args.api_key_file)
    if not api_key:
        raise SystemExit(
            "Missing API key. Set OPENAI_API_KEY or pass --api-key-file /path/to/key.txt"
        )

    client = OpenAI(api_key=api_key)

    custom_prompt = args.prompt
    if not custom_prompt:
        custom_prompt = input("Edit prompt (Enter to use default hair-color edit): ").strip()

    prompt = build_prompt(custom_prompt, args.color, args.extra_instruction)

    with image_path.open("rb") as image_file:
        result = client.images.edit(
            model=args.model,
            image=image_file,
            prompt=prompt,
            quality=args.quality,
            output_format=args.output_format,
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_bytes(base64.b64decode(result.data[0].b64_json))
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
