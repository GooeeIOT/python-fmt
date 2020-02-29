import shlex
import subprocess
import sys
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

    @classmethod
    def select(cls, selector: str, path: str) -> str:
        return getattr(cls, selector)(path)

    @classmethod
    def staged(cls, path: str) -> str:
        return " ".join(file for code, file in cls._iter_changed(path) if code[0] in "MARC")

    @classmethod
    def modified(cls, path: str) -> str:
        return " ".join(
            file
            for code, file in cls._iter_changed(path)
            if "D" not in code and (code[0] in "MARC" or code[1] in "MARC" or code == "??")
        )

    @classmethod
    def head(cls, path: str) -> str:
        return " ".join(cls._iter_committed(path, "HEAD^1..HEAD"))

    @classmethod
    def local(cls, path: str) -> str:
        return " ".join(cls._iter_committed(path, "@{upstream}.."))

    @classmethod
    def all(cls, path: str) -> str:
        return path

    @classmethod
    def _iter_changed(cls, path):
        output = cls._sh("git", "status", "--porcelain", path)
        for line in output.splitlines():
            code, line = line[:2], line[2:].strip()
            if code[0] == "R":
                _, _, file = line.split()
            else:
                file = line.strip()
            if code[1] != "D" and file.endswith(".py"):
                yield code, file

    @classmethod
    def _iter_committed(cls, path, refspec):
        output = cls._sh("git", "--no-pager", "diff", "--numstat", refspec, "--", path)
        for line in output.splitlines():
            file = line.strip().rsplit(maxsplit=1)[-1]
            if file.endswith(".py"):
                yield file

    @classmethod
    def _sh(cls, *args):
        return subprocess.run(args, stdout=subprocess.PIPE, text=True, check=True).stdout


def pyfmt(
    path, select, check=False, line_length=100, extra_isort_args="", extra_black_args=""
) -> int:
    """Run isort and black with the given params and print the results."""
    path = SELECTORS.select(select, path)
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
