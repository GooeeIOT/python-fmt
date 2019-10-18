#!/usr/bin/env python3
import argparse
import os
import shlex
import sys
from subprocess import PIPE, Popen
from subprocess import run as run_sh

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
    "--target-version={target_version}",
    "{args.extra_black_args}",
    "{args.PATH}",
]


def main():
    parser = argparse.ArgumentParser(prog="pyfmt")
    parser.add_argument(
        "PATH",
        default=os.getenv("BASE_CODE_DIR", "."),
        help="path to base directory where pyfmt will be run;"
        " defaults to $BASE_CODE_DIR or the current directory",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="do a dry run and print the files that would be formatted",
    )
    parser.add_argument(
        "--line-length",
        type=int,
        default=int(os.getenv("MAX_LINE_LENGTH", 100)),
        help="wrap lines longer than this value; defaults to $MAX_LINE_LENGTH or 100",
    )
    parser.add_argument("--extra-isort-args", default="", help="additional args to pass to isort")
    parser.add_argument("--extra-black-args", default="", help="additional args to pass to black")

    args = parser.parse_args()

    if args.check:
        args.extra_isort_args += " --check-only"
        args.extra_black_args += " --check"

    isort_cmd = shlex.split(" ".join(ISORT_CMD).format(args=args))
    result = run_sh(isort_cmd, stdout=PIPE)
    print(f"isort: {result.stdout.decode().strip()}\n")

    target_version = f"py{sys.version_info.major}{sys.version_info.minor}"
    black_cmd = shlex.split(" ".join(BLACK_CMD).format(args=args, target_version=target_version))
    result = run_sh(black_cmd, stderr=PIPE)
    print("black: {}".format("\n       ".join(result.stderr.decode().splitlines())))


if __name__ == "__main__":
    main()
