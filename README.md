# hf-autodownloader

An interactive command-line tool for choosing files from a Hugging Face Hub repository and downloading them into a local repository folder.

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Usage

```bash
python3 main.py [repo_id]
```

Pass a repository ID such as `openai-community/gpt2`, or omit it to enter one interactively. The tool prompts for a parent directory, lets you choose files from a paginated list, summarizes the selection, and asks for confirmation before downloading. Files are placed under `<parent>/<owner>_<repository>` by default, preserving their paths inside that directory. For example, `meta-llama/Llama-3-8B` is stored in a `meta-llama_Llama-3-8B` folder.

Optional arguments let scripts or repeat users skip the repository and/or parent-directory prompt:

```bash
python3 main.py openai-community/gpt2 --parent-dir ~/Downloads --revision main
```

Use `python3 main.py --help` to see all options. Downloads start only after you confirm the file summary. Press Ctrl+C to stop; files already completed remain in place.

Private or gated repositories require an available Hugging Face token (for example, one configured with `hf auth login`). No files are downloaded until the final confirmation is accepted.

## Project layout

- `main.py` parses arguments and coordinates the workflow.
- `api.py` lists repository files and metadata and wraps `hf_hub_download`.
- `tui.py` contains the Questionary prompts and paginated file selection.
- `downloader.py` coordinates downloads and adapts Hub transfer updates to Rich progress bars.

## Development history

Each project component was committed as a separate milestone: project setup, Hub API access, the interactive TUI, Rich transfer progress, and CLI integration. Review those commits with:

```bash
git log --oneline
git status
```

Runtime dependencies use minimum supported versions in `requirements.txt`.
