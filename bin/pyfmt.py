#!/usr/bin/env python3
import argparse
import os
import shlex
import subprocess
import sys
from subprocess import PIPE, Popen

TARGET_VERSION = f"py{sys.version_info.major}{sys.version_info.minor}"

DEFAULT_PATH = os.getenv("BASE_CODE_DIR", ".")
DEFAULT_LINE_LENGTH = int(os.getenv("MAX_LINE_LENGTH", "100"))

ISORT_CMD = [
    "isort",
    "--force-grid-wrap=0",
    "--line-width={args.line_length}",
    "--multi-line=3",
    "--use-parentheses",
    "--recursive",
    "--trailing-comma",
    "{args.extra_isort_args}",
    "{args.PATH}",
]
BLACK_CMD = [
    "black",
    "--line-length={args.line_length}",
    f"--target-version={TARGET_VERSION}",
    "{args.extra_black_args}",
    "{args.PATH}",
]


def run_cmd(cmd, args):
    """Run a shell command and print the output."""
    cmd = shlex.split(" ".join(cmd).format(args=args))
    result = subprocess.run(cmd, stdout=PIPE, stderr=PIPE)

    prefix = f"{cmd[0]}: "
    sep = "\n" + (" " * len(prefix))
    lines = result.stdout.decode().splitlines() + result.stderr.decode().splitlines()
    print(f"{prefix}{sep.join(lines)}")


def main():
    parser = argparse.ArgumentParser(prog="pyfmt")
    parser.add_argument(
        "PATH",
        nargs="?",
        default=DEFAULT_PATH,
        help="path to base directory where pyfmt will be run;"
        " defaults to $BASE_CODE_DIR or the current directory",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="don't write changes, just print the files that would be formatted",
    )
    parser.add_argument(
        "--line-length",
        type=int,
        default=DEFAULT_LINE_LENGTH,
        help="max characters per line; defaults to $MAX_LINE_LENGTH or 100",
    )
    parser.add_argument("--extra-isort-args", default="", help="additional args to pass to isort")
    parser.add_argument("--extra-black-args", default="", help="additional args to pass to black")

    args = parser.parse_args()

    if args.check:
        args.extra_isort_args += " --check-only"
        args.extra_black_args += " --check"

    run_cmd(ISORT_CMD, args)
    run_cmd(BLACK_CMD, args)


if __name__ == "__main__":
    main()
