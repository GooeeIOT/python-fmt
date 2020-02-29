import sys

import pyfmt

from .utils import FormattedHelpArgumentParser

SELECT_CHOICES = {
    "staged": "files in the index",
    "modified": "files in the index, working tree, and untracked files",
    "head": "files changed in HEAD",
    "local": "files changed locally but not upstream",
    "all": "all files",
}

COMMIT_CHOICES = {
    "all": "commit all files in tree, whether or not they were formatted",
    "patch": "commit formatted files with --patch",
    "amend": "commit formatted files with --amend",
}


def main():
    parser = FormattedHelpArgumentParser(prog="pyfmt")
    parser.add_argument(
        "path",
        nargs="?",
        envvar="BASE_CODE_DIR",
        default=".",
        metavar="PATH",
        help="path to base directory where pyfmt will be run",
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
    parser.add_argument(
        "--line-length",
        type=int,
        envvar="MAX_LINE_LENGTH",
        default=100,
        help="max characters per line",
    )
    parser.add_choices_argument(
        "--commit",
        choices=COMMIT_CHOICES,
        nargs="*",
        help="commit changes if any files were formatted",
    )
    parser.add_argument(
        "--commit-message",
        default="",
        help="if --commit=message, this is used as the commit message"
        " (WARNING: this will auto-commit any changes!)",
    )
    parser.add_argument("--extra-isort-args", default="", help="additional args to pass to isort")
    parser.add_argument("--extra-black-args", default="", help="additional args to pass to black")

    opts = parser.parse_args()

    exitcode = pyfmt.pyfmt(
        opts.path,
        opts.select,
        check=opts.check,
        line_length=opts.line_length,
        commit=opts.commit,
        commit_message=opts.commit_message,
        extra_isort_args=opts.extra_isort_args,
        extra_black_args=opts.extra_black_args,
    )
    sys.exit(exitcode)


if __name__ == "__main__":
    main()
