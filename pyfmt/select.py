import subprocess
from dataclasses import dataclass
from typing import Iterator, Tuple

__all__ = ["select_staged", "select_modified", "select_head", "select_local", "select_all"]


def select_staged(path: str) -> Iterator[str]:
    return (file for code, file in _iter_changed(path) if code.index_has_changes())


def select_modified(path: str) -> Iterator[str]:
    return (file for code, file in _iter_changed(path) if code.has_changes() or code.is_untracked())


def select_head(path: str) -> Iterator[str]:
    return _iter_committed(path, "HEAD^1..HEAD")


def select_local(path: str) -> Iterator[str]:
    return _iter_committed(path, "@{upstream}..")


def select_all(path: str) -> Iterator[str]:
    return [path]


@dataclass
class GitStatusCode:
    index: str
    work_tree: str

    def index_has_changes(self) -> bool:
        return self.index in "MARC"

    def has_changes(self) -> bool:
        return self.index_has_changes() or self.work_tree in "MAC"

    def is_untracked(self) -> bool:
        return self.index == self.work_tree == "?"

    def is_deleted(self) -> bool:
        return self.work_tree == "D"

    def is_renamed(self) -> bool:
        return self.index == "R"


def _iter_changed(path) -> Iterator[Tuple[GitStatusCode, str]]:
    output = _sh("git", "status", "--porcelain", path)
    for line in output.splitlines():
        xy, line = line[:2], line[2:].strip()
        code = GitStatusCode(*xy)
        if code.is_renamed():
            _, _, file = line.split()
        else:
            file = line.strip()
        if not code.is_deleted() and file.endswith(".py"):
            yield code, file


def _iter_committed(path, refspec) -> Iterator[str]:
    output = _sh("git", "--no-pager", "diff", "--numstat", refspec, "--", path)
    for line in output.splitlines():
        file = line.strip().rsplit(maxsplit=1)[-1]
        if file.endswith(".py"):
            yield file


def _sh(*args: str) -> str:
    return subprocess.run(args, stdout=subprocess.PIPE, text=True, check=True).stdout
