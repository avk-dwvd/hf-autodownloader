# Getting started

## Requirements

Use Python 3.10 or newer. For private or gated repositories, configure a Hugging Face token with `hf auth login` before running the tool.

## Install

From the repository root:

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Run

Start with interactive repository entry:

```bash
python3 main.py
```

Or provide the repository ID and optional parent directory and revision:

```bash
python3 main.py openai-community/gpt2 --parent-dir ~/Downloads --revision main
```

Use `python3 main.py --help` to see all options. When the parent directory is omitted, the CLI prompts for it and defaults to the current directory. The file chooser shows repository paths and available sizes in pages. Confirm the summary to begin downloading; declining confirmation exits without downloading.
