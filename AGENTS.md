# Repository Guidelines

## Project Structure & Module Organization

This is a small Python CLI with modules in the repository root:

- `main.py` parses arguments and coordinates the interactive workflow.
- `api.py` lists Hugging Face model repository files and downloads individual files.
- `tui.py` contains Questionary prompts, pagination, selection summaries, and confirmation.
- `downloader.py` connects Hub transfer updates to Rich progress displays.
- `requirements.txt` lists runtime dependencies; `README.md` documents setup and usage.

There is no separate test or asset directory. Keep responsibilities in their existing modules; put shared workflow decisions in `main.py` rather than coupling API code to terminal prompts.

## Build, Test, and Development Commands

Create and activate a local environment, then install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
python -m pip install -r requirements.txt -r requirements-lint.txt -r requirements-docs.txt
ruff check .
ruff format --check .
mkdocs build --strict
```

Run interactively with `python3 main.py`, or provide a repository ID, for example `python3 main.py openai-community/gpt2 --parent-dir ~/Downloads`. Use `python3 main.py --help` to inspect options. For a local syntax/import smoke check, run `python -m compileall main.py api.py tui.py downloader.py`. Do not run real repository downloads as a routine check; downloading requires explicit selection and confirmation in the CLI.

## Coding Style & Naming Conventions

Use Python 3.10+ syntax, four-space indentation, type hints on public interfaces, `snake_case` for functions and variables, and descriptive names for user-visible operations. Keep third-party imports separate from standard-library imports. Ruff is configured in `pyproject.toml`; run `ruff check .` and `ruff format --check .` before submitting changes.

## Testing Guidelines

The repository currently has no test framework or test suite. For behavior changes, add focused automated coverage if a test framework is introduced; avoid tests that depend on network access or a particular remote repository. Verify CLI parsing and imports locally without downloading Hub content.

## Commit & Pull Request Guidelines

Recent commits use concise Conventional Commit-style subjects, such as `feat(tui): ...`, `fix(api): ...`, and `docs: ...`. Keep commits focused. Pull requests should describe user-visible changes, list verification commands and results, and note any authentication or network assumptions. Terminal screenshots are optional unless they clarify a meaningful TUI change.

## Security & Configuration

Use Hugging Face’s configured token mechanism for private or gated repositories; never print or commit tokens. Treat repository paths as untrusted, preserve the API module’s path checks, and avoid interpolating user input into shell commands. Keep `venv/`, bytecode, and local system files out of commits as configured in `.gitignore`.
