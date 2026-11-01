"""Coordinate Hub file downloads and render live Rich progress bars."""

from __future__ import annotations

from pathlib import Path

from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TaskProgressColumn,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)
from rich.text import Text
from tqdm.auto import tqdm

from api import RepositoryFile, download_repository_file


def _rich_tqdm(progress: Progress, task_id: int) -> type[tqdm]:
    """Create a tqdm-compatible adapter that updates one Rich task."""

    class RichTqdm(tqdm):
        def __init__(self, *args: object, **kwargs: object) -> None:
            kwargs["disable"] = False
            super().__init__(*args, **kwargs)
            progress.update(task_id, total=self.total)

        def display(self, msg: str | None = None, pos: int | None = None) -> None:
            # Rich owns terminal rendering; suppress tqdm's competing output.
            return None

        def update(self, n: int = 1) -> bool | None:
            updated = super().update(n)
            progress.update(task_id, completed=self.n, total=self.total)
            return updated

    return RichTqdm


def download_files(
    repo_id: str,
    files: list[RepositoryFile],
    destination: Path,
    *,
    revision: str | None = None,
    token: str | bool | None = None,
) -> list[Path]:
    """Download selected files, preserving paths and reporting live progress."""
    if not files:
        return []

    destination.mkdir(parents=True, exist_ok=True)
    progress = Progress(
        TextColumn("{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        DownloadColumn(),
        TransferSpeedColumn(),
        TimeRemainingColumn(),
        transient=False,
    )
    paths: list[Path] = []
    with progress:
        overall_id = progress.add_task("Files", total=len(files))
        for index, item in enumerate(files, start=1):
            label = Text(f"[{index}/{len(files)}] {item.path}")
            file_id = progress.add_task(label, total=item.size)
            try:
                local_path = download_repository_file(
                    repo_id,
                    item.path,
                    destination,
                    revision=revision,
                    token=token,
                    tqdm_class=_rich_tqdm(progress, file_id),
                )
            except BaseException:
                progress.update(file_id, description=Text(f"Failed: {item.path}"), visible=True)
                raise
            actual_size = local_path.stat().st_size if local_path.exists() else item.size
            progress.update(file_id, total=actual_size, completed=actual_size or 0)
            paths.append(local_path)
            progress.advance(overall_id)
    return paths
