"""Command-line entry point for hf-autodownloader."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from huggingface_hub.utils import HfHubHTTPError
from rich.console import Console

from api import list_repository_files
from downloader import download_files
from tui import (
    ask_for_parent_directory,
    ask_for_repository,
    confirm_download,
    select_repository_files,
)

console = Console()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="hf-autodownloader",
        description=(
            "Interactively select files to download from a "
            "Hugging Face model repository."
        ),
    )
    parser.add_argument(
        "repo_id",
        nargs="?",
        help="Hugging Face model repository ID (for example: openai-community/gpt2)",
    )
    parser.add_argument("--revision", help="Repository branch, tag, or commit to read")
    parser.add_argument(
        "--parent-dir",
        type=Path,
        help="Parent directory for downloads (prompted for when omitted)",
    )
    return parser


def destination_for(parent: Path, repo_id: str) -> Path:
    """Resolve a repository ID into a safe, readable child directory name."""
    directory_name = re.sub(r"[^A-Za-z0-9._-]+", "_", repo_id.strip().replace("/", "_"))
    directory_name = directory_name.strip("._-")
    if not directory_name or directory_name in {".", ".."}:
        raise ValueError(
            "Repository ID cannot be used as a destination directory name."
        )
    return parent.expanduser().resolve() / directory_name


def run(args: argparse.Namespace) -> int:
    repo_id = ask_for_repository(args.repo_id)
    if repo_id is None:
        console.print("[yellow]Cancelled.[/yellow]")
        return 130
    repo_id = repo_id.strip()
    if (
        not repo_id
        or "/" not in repo_id
        or any(part in {"", ".", ".."} for part in repo_id.split("/"))
    ):
        console.print(
            "[red]Enter a repository ID in owner/name form.[/red]", stderr=True
        )
        return 2

    parent = args.parent_dir
    if parent is None:
        parent = ask_for_parent_directory()
    elif not parent.is_absolute():
        parent = (Path.cwd() / parent).resolve()
    if parent is None:
        console.print("[yellow]Cancelled.[/yellow]")
        return 130
    parent = parent.expanduser().resolve()
    destination = destination_for(parent, repo_id)

    console.print(f"[bold]Reading file list for {repo_id}[/bold]")
    files = list_repository_files(repo_id, revision=args.revision)
    if not files:
        console.print("[yellow]No files were found in this repository.[/yellow]")
        return 0

    selected = select_repository_files(files)
    if selected is None:
        console.print("[yellow]Cancelled.[/yellow]")
        return 130
    if not selected:
        console.print("[yellow]No files selected.[/yellow]")
        return 0

    approved = confirm_download(selected, destination)
    if approved is not True:
        console.print("[yellow]Download cancelled.[/yellow]")
        return 0

    downloaded = download_files(
        repo_id,
        selected,
        destination,
        revision=args.revision,
    )
    console.print(
        f"[green]Downloaded {len(downloaded)} file(s) to {destination}[/green]"
    )
    return 0


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return run(args)
    except KeyboardInterrupt:
        console.print(
            "\n[yellow]Interrupted. Already completed files were kept.[/yellow]"
        )
        return 130
    except (HfHubHTTPError, OSError, ValueError) as error:
        console.print(f"[red]Error: {error}[/red]", stderr=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
