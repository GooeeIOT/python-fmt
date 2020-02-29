import shlex
import subprocess
import sys
from dataclasses import dataclass
from subprocess import PIPE

TARGET_VERSION = f"py{sys.version_info.major}{sys.version_info.minor}"

ISORT_CMD = [
    "isort",
    "--force-grid-wrap=0",
    "--line-width={line_length}",
    "--multi-line=3",
    "--use-parentheses",
    "--recursive",
    "--trailing-comma",
    "{extra_isort_args}",
    "{path}",
]
BLACK_CMD = [
    "black",
    "--line-length={line_length}",
    f"--target-version={TARGET_VERSION}",
    "{extra_black_args}",
    "{path}",
]


class SELECTORS:
    """Container for selector functions."""

    @dataclass
    class Code:
        code: str

        _str_mapping = {
            " ": "unmodified",
            "M": "modified",
            "A": "added",
            "D": "deleted",
            "R": "renamed",
            "C": "copied",
            "U": "updated",
            "?": "untracked",
            "!": "ignored",
        }

        def __str__(self):
            return self.code

        def __bool__(self):
            return not self.is_unmodified()

        def description(self):
            return self._str_mapping[self.code]

        def has_changes(self):
            return self.is_modified() or self.is_renamed() or self.is_copied()

        def is_new(self):
            return self.is_added() or self.is_untracked()

        def is_unmodified(self):
            return self.code == " "

        def is_modified(self):
            return self.code == "M"

        def is_added(self):
            return self.code == "A"

        def is_deleted(self):
            return self.code == "D"

        def is_renamed(self):
            return self.code == "R"

        def is_copied(self):
            return self.code == "C"

        def is_updated(self):
            return self.code == "U"

        def is_untracked(self):
            return self.code == "?"

        def is_ignored(self):
            return self.code == "!"

    class Status:
        def __init__(self, status_code: str):
            x, y = status_code
            self.index = SELECTORS.Code(x)
            self.work_tree = SELECTORS.Code(y)

        def __str__(self):
            return f"{self.index.code}{self.work_tree.code}"

        def is_deleted(self):
            return self.index.is_deleted() or self.work_tree.is_deleted()

        def is_renamed(self):
            return self.index.is_renamed()

        def has_changes(self):
            return self.index.has_changes() or self.work_tree.has_changes()

        def is_untracked(self):
            return self.index.is_untracked()

    @classmethod
    def select(cls, selector: str, path: str) -> str:
        return getattr(cls, selector)(path)

    @classmethod
    def _sh(cls, *args):
        return subprocess.run(args, stdout=subprocess.PIPE, text=True, check=True).stdout

    @classmethod
    def _iter_changed(cls, path):
        output = cls._sh("git", "status", "--porcelain", path)
        for line in output.splitlines():
            status_code, line = line[:2], line[2:].strip()
            status = cls.Status(status_code)
            if status.is_renamed():
                _, _, file = line.split()
            else:
                file = line.strip()
            if file.endswith(".py"):
                yield status, file

    @classmethod
    def staged(cls, path: str) -> str:
        return " ".join(
            file for status, file in cls._iter_changed(path) if status.index.has_changes()
        )

    @classmethod
    def modified(cls, path: str) -> str:
        return " ".join(
            file
            for status, file in cls._iter_changed(path)
            if status.has_changes() or status.is_untracked()
        )

    @classmethod
    def _iter_committed(cls, path, refspec):
        output = cls._sh("git", "--no-pager", "diff", "--numstat", refspec, "--", path)
        for line in output.splitlines():
            file = line.strip().rsplit(maxsplit=1)[-1]
            if file.endswith(".py"):
                yield file

    @classmethod
    def head(cls, path: str) -> str:
        return " ".join(cls._iter_committed(path, "HEAD^1..HEAD"))

    @classmethod
    def local(cls, path: str) -> str:
        return " ".join(cls._iter_committed(path, "@{upstream}.."))

    @classmethod
    def all(cls, path: str) -> str:
        return path


def pyfmt(
    path, select, check=False, line_length=100, extra_isort_args="", extra_black_args=""
) -> int:
    """Run isort and black with the given params and print the results."""
    path = SELECTORS.select(select, path)
    print(path)
    if not path:
        print("Nothing to do.")
        return 0

    if check:
        extra_isort_args += " --check-only"
        extra_black_args += " --check"

    isort_exitcode = run_formatter(
        ISORT_CMD, path, line_length=line_length, extra_isort_args=extra_isort_args
    )
    black_exitcode = run_formatter(
        BLACK_CMD, path, line_length=line_length, extra_black_args=extra_black_args
    )

    return isort_exitcode or black_exitcode


def run_formatter(cmd, path, **kwargs) -> int:
    """Helper to run a shell command and print prettified output."""
    cmd = shlex.split(" ".join(cmd).format(path=path, **kwargs))
    result = subprocess.run(cmd, stdout=PIPE, stderr=PIPE)

    prefix = f"{cmd[0]}: "
    sep = "\n" + (" " * len(prefix))
    lines = result.stdout.decode().splitlines() + result.stderr.decode().splitlines()
    if "".join(lines) == "":
        print(f"{prefix}No changes.")
    else:
        print(f"{prefix}{sep.join(lines)}")

    return result.returncode
