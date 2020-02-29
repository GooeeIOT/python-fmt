import os
import sys

import pyfmt

from .utils import FormattedHelpArgumentParser

DEFAULT_PATH = os.getenv("BASE_CODE_DIR", ".")
DEFAULT_LINE_LENGTH = int(os.getenv("MAX_LINE_LENGTH", "100"))

SELECT_CHOICES = {
    "staged": "files in the index",
    "modified": "files in the index, working tree, and untracked files",
    "head": "files changed in HEAD",
    "local": "files changed locally but not upstream",
    "all": "all files",
}

COMMIT_CHOICES = {
    "no": "do not commit changes",
    "yes": "call `git commit -a` on changes",
    "amend": "call `git commit -a --amend` on changes",
}


def main():
    parser = FormattedHelpArgumentParser(prog="pyfmt")
    parser.add_argument(
        "path",
        nargs="?",
        default=DEFAULT_PATH,
        metavar="PATH",
        help="path to base directory where pyfmt will be run;"
        " defaults to $BASE_CODE_DIR or the current directory",
    )
    parser.add_choices_argument(
        "-s",
        "--select",
        choices=SELECT_CHOICES,
        default="all",
        help="filter which files to format in PATH:",
    )
    parser.add_argument(
        "-c",
        "--check",
        action="store_true",
        help="don't write changes, just print the files that would be formatted",
    )
    parser.add_choices_argument(
        "--commit",
        choices=COMMIT_CHOICES,
        default="no",
        help="commit changes if any files were formatted",
    )
    parser.add_argument(
        "--line-length",
        type=int,
        default=DEFAULT_LINE_LENGTH,
        help="max characters per line; defaults to $MAX_LINE_LENGTH or 100",
    )
    parser.add_argument("--extra-isort-args", default="", help="additional args to pass to isort")
    parser.add_argument("--extra-black-args", default="", help="additional args to pass to black")

    opts = parser.parse_args()
    if opts.commit == "no":
        opts.commit = None

    exitcode = pyfmt.pyfmt(
        opts.path,
        opts.select,
        check=opts.check,
        commit=opts.commit,
        line_length=opts.line_length,
        extra_isort_args=opts.extra_isort_args,
        extra_black_args=opts.extra_black_args,
    )
    sys.exit(exitcode)


if __name__ == "__main__":
    main()
