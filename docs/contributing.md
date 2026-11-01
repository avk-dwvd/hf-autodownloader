# Contributing

Keep changes focused in the module responsible for that behavior. Use Python 3.10+ syntax, four-space indentation, type hints on public interfaces, and `snake_case` names. Ruff is configured in `pyproject.toml`; run both `ruff check .` and `ruff format --check .` before opening a pull request.

Use concise Conventional Commit-style subjects consistent with the history, such as `feat(tui): add keyboard shortcut` or `fix(api): handle missing file sizes`. Pull requests should explain the user-visible change, list verification commands and their results, and mention authentication or network assumptions. Screenshots are useful for substantial TUI changes but are not required for CLI-only changes.

## Documentation and GitHub Pages

Edit the relevant Markdown page under `docs/` and keep navigation in `mkdocs.yml` current. Check the rendered site locally with:

```bash
python -m pip install -r requirements-docs.txt
mkdocs build --strict
```

The GitHub Actions workflow builds docs on pull requests and deploys them from `main`. Before the first deployment, enable GitHub Pages for the repository with **Build and deployment → Source → GitHub Actions**. The workflow uses the `github-pages` environment and does not require repository secrets.
