# Architecture

The CLI is split into focused modules in the repository root:

| Module | Responsibility |
| --- | --- |
| `main.py` | Parses arguments and coordinates prompts, API calls, confirmation, and downloads. |
| `api.py` | Lists model repository files and sizes; validates paths and wraps `hf_hub_download`. |
| `tui.py` | Handles Questionary prompts, paginated checkboxes, size summaries, and confirmation. |
| `downloader.py` | Connects Hub transfer progress to Rich bars, speed, and ETA displays. |

Runtime dependencies are listed in `requirements.txt`. Developer tooling has separate files: `requirements-lint.txt` for Ruff and `requirements-docs.txt` for MkDocs.

## Development commands

```bash
source venv/bin/activate
python -m pip install -r requirements.txt -r requirements-lint.txt -r requirements-docs.txt
ruff check .
ruff format --check .
mkdocs build --strict
```

The CLI currently has no automated test suite. Smoke checks such as `python3 main.py --help` and `python -m compileall main.py api.py tui.py downloader.py` do not contact Hugging Face. Avoid invoking real downloads as a routine check.
