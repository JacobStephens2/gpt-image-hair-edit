# GPT Image Hair Color Edit

Small Python CLI for using OpenAI's image edit API to change only a subject's hair color while preserving eyebrows and the rest of the photo.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Set your API key in the shell:

```bash
export OPENAI_API_KEY="sk-..."
```

Or keep it in a local file outside the repo and pass `--api-key-file`.

## Example

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

## Defaults

- Model: `gpt-image-2`
- Quality: `medium`
- Output format: `png`
- The prompt explicitly says not to change eyebrows.

No images or API keys should be committed to this repo.
