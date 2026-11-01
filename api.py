"""Hugging Face Hub operations used by the command-line interface."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path, PurePosixPath

from huggingface_hub import HfApi, hf_hub_download


@dataclass(frozen=True, slots=True)
class RepositoryFile:
    """A repository file and its known size in bytes."""

    path: str
    size: int | None


def list_repository_files(
    repo_id: str,
    *,
    revision: str | None = None,
    token: str | bool | None = None,
) -> list[RepositoryFile]:
    """Return files in a model repository, including nested paths and sizes."""
    api = HfApi()
    entries = api.list_repo_tree(
        repo_id=repo_id,
        repo_type="model",
        revision=revision,
        token=token,
        recursive=True,
        expand=True,
    )
    files: list[RepositoryFile] = []
    for entry in entries:
        path = getattr(entry, "path", None)
        if not path or not isinstance(path, str):
            continue
        size = getattr(entry, "size", None)
        if size is None:
            size = getattr(getattr(entry, "lfs", None), "size", None)
        files.append(RepositoryFile(path=path, size=size if isinstance(size, int) else None))
    return sorted(files, key=lambda item: item.path.casefold())


def download_repository_file(
    repo_id: str,
    file_path: str,
    destination: Path,
    *,
    revision: str | None = None,
    token: str | bool | None = None,
    tqdm_class: type | None = None,
) -> Path:
    """Download one file into destination while retaining its repository path."""
    relative_path = PurePosixPath(file_path)
    if relative_path.is_absolute() or ".." in relative_path.parts:
        raise ValueError(f"Unsafe repository path: {file_path!r}")

    result = hf_hub_download(
        repo_id=repo_id,
        filename=relative_path.as_posix(),
        repo_type="model",
        revision=revision,
        token=token,
        local_dir=destination,
        tqdm_class=tqdm_class,
    )
    return Path(result)
