"""Questionary prompts for repository and file selection."""

from __future__ import annotations

from pathlib import Path

import questionary
from questionary import Choice
from rich.console import Console

from api import RepositoryFile

console = Console()
PAGE_SIZE = 25


def format_size(size: int | None) -> str:
    if size is None:
        return "size unknown"
    units = ("B", "KiB", "MiB", "GiB", "TiB")
    value = float(size)
    for unit in units:
        if value < 1024 or unit == units[-1]:
            return f"{value:.1f} {unit}" if unit != "B" else f"{size} B"
        value /= 1024
    return f"{size} B"


def ask_for_repository(initial_value: str | None = None) -> str | None:
    """Ask for a repository ID when it was not supplied on the CLI."""
    if initial_value:
        return initial_value.strip()
    return questionary.text(
        "Hugging Face model repository ID (owner/name):",
        validate=lambda value: True if value.strip() else "Enter a repository ID.",
    ).ask()


def ask_for_parent_directory(default: Path | None = None) -> Path | None:
    """Ask for a writable parent directory, defaulting to the current folder."""
    default = default or Path.cwd()
    value = questionary.text(
        "Parent directory for downloaded files:",
        default=str(default),
        validate=lambda path: True if path.strip() else "Enter a directory path.",
    ).ask()
    if value is None:
        return None
    return Path(value).expanduser().resolve()


def select_repository_files(files: list[RepositoryFile]) -> list[RepositoryFile] | None:
    """Select files using paginated checkbox menus; None means cancelled."""
    if not files:
        console.print("[yellow]This repository contains no selectable files.[/yellow]")
        return []

    selected_paths: set[str] = set()
    page_count = (len(files) + PAGE_SIZE - 1) // PAGE_SIZE
    page = 0
    while True:
        start = page * PAGE_SIZE
        page_files = files[start : start + PAGE_SIZE]
        console.print(
            f"\n[bold]Files {start + 1}–{start + len(page_files)} of {len(files)}[/bold] "
            f"(page {page + 1}/{page_count})"
        )
        choices = [
            Choice(
                title=f"{item.path}  ({format_size(item.size)})",
                value=item.path,
                checked=item.path in selected_paths,
            )
            for item in page_files
        ]
        page_selection = questionary.checkbox(
            "Toggle files to include, then press Enter:",
            choices=choices,
            instruction="(space to toggle, a to select all, i to invert)",
        ).ask()
        if page_selection is None:
            return None

        current_page_paths = {item.path for item in page_files}
        selected_paths.difference_update(current_page_paths)
        selected_paths.update(page_selection)

        actions = []
        if page > 0:
            actions.append(Choice("Previous page", value="previous"))
        if page + 1 < page_count:
            actions.append(Choice("Next page", value="next"))
        actions.append(Choice(f"Finish selection ({len(selected_paths)} selected)", value="finish"))
        action = questionary.select("Continue:", choices=actions).ask()
        if action is None:
            return None
        if action == "previous":
            page -= 1
        elif action == "next":
            page += 1
        else:
            selected = [item for item in files if item.path in selected_paths]
            return selected


def confirm_download(
    files: list[RepositoryFile],
    destination: Path,
) -> bool | None:
    """Show a selection summary and ask before any download begins."""
    known_total = sum(item.size for item in files if item.size is not None)
    unknown_count = sum(item.size is None for item in files)
    total_label = format_size(known_total)
    if unknown_count:
        total_label += f" + {unknown_count} file(s) with unknown size"
    console.print("\n[bold]Download summary[/bold]")
    console.print(f"  Files: {len(files)}")
    console.print(f"  Known total size: {total_label}")
    console.print(f"  Destination: {destination}")
    return questionary.confirm("Start downloading these files?", default=False).ask()
