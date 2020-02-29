import shlex
import subprocess
import sys
from subprocess import PIPE

from . import select

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

SELECTOR_MAP = {
    "staged": select.select_staged,
    "modified": select.select_modified,
    "head": select.select_head,
    "local": select.select_local,
    "all": select.select_all,
}


def pyfmt(
    path, selector, check=False, line_length=100, extra_isort_args="", extra_black_args=""
) -> int:
    """Run isort and black with the given params and print the results."""
    select_files = SELECTOR_MAP[selector]
    path = " ".join(select_files(path))
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
