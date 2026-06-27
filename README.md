# GPT Image Hair Color Edit

Small Python CLI for using OpenAI's image edit API to change only a subject's hair color while preserving eyebrows and the rest of the photo.

The default prompt is tuned for realistic hair-color edits. It asks the model to keep the face, skin tone, expression, eyes, hands, jewelry, clothing, background, lighting, framing, and photo texture intact.

## What It Does

- Uses `gpt-image-2` through OpenAI's image edit API.
- Defaults to `quality=medium`.
- Writes a PNG output file.
- Lets you choose the target hair color.
- Explicitly instructs the model not to change eyebrows.
- Keeps images and local API key files out of git by default.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Set your API key in the shell:

```bash
export OPENAI_API_KEY="<your_openai_api_key>"
```

Or keep it in a local file outside the repo and pass `--api-key-file`.

## Usage

Basic usage:

```bash
python edit_hair_color.py /path/to/photo.jpg \
  --output /path/to/edited.png \
  --color "strawberry blonde"
```

Using a local key file:

```bash
python edit_hair_color.py /path/to/photo.jpg \
  --output /path/to/edited.png \
  --color "strawberry blonde" \
  --api-key-file ~/Documents/openai-key.txt
```

Changing the target color:

```bash
python edit_hair_color.py /path/to/photo.jpg \
  --output /path/to/auburn.png \
  --color "soft auburn"
```

Adding an extra prompt instruction:

```bash
python edit_hair_color.py /path/to/photo.jpg \
  --output /path/to/edited.png \
  --color "strawberry blonde" \
  --extra-instruction "Keep the color subtle and natural-looking."
```

## Defaults

- Model: `gpt-image-2`
- Quality: `medium`
- Output format: `png`
- The prompt explicitly says not to change eyebrows.

## Privacy

This repo is meant to stay code-only. Do not commit input photos, edited outputs, API keys, or raw API response files. The included `.gitignore` excludes common image formats, `inputs/`, `outputs/`, local key files, and response JSON by default.

## License

MIT
