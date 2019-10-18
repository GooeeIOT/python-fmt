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


def pyfmt(path, line_length=100, extra_isort_args="", extra_black_args=""):
    """Run isort and black with the given params and return the results."""
    isort_output = run_formatter(
        ISORT_CMD, path, line_length=line_length, extra_isort_args=extra_isort_args
    )
    black_output = run_formatter(
        BLACK_CMD, path, line_length=line_length, extra_black_args=extra_black_args
    )
    return isort_output, black_output


def run_formatter(cmd, path, **kwargs):
    """Helper to run a shell command and return prettified output."""
    cmd = shlex.split(" ".join(cmd).format(path=path, **kwargs))
    result = subprocess.run(cmd, stdout=PIPE, stderr=PIPE)

    prefix = f"{cmd[0]}: "
    sep = "\n" + (" " * len(prefix))
    lines = result.stdout.decode().splitlines() + result.stderr.decode().splitlines()
    return f"{prefix}{sep.join(lines)}"
