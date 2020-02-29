# pyfmt

Python auto-formatting using [isort](https://isort.readthedocs.io/en/latest/) and
[black](https://black.readthedocs.io/en/latest/).

## Installation

### Using pip

```console
pip3 install git+https://github.com/GooeeIOT/pyfmt.git
```

### From source

```console
git clone https://github.com/GooeeIOT/pyfmt
cd pyfmt
python setup.py install
```

## Contrib

### Example Use in a Git Hook

Prevent a `git commit` if `pyfmt --check --select staged` comes back dirty:

```console
ln -sf contrib/git_hooks/pre-commit .git/hooks
```

Prevent a `git push` if `pyfmt --check --select local` comes back dirty:

```console
ln -sf contrib/git_hooks/pre-push .git/hooks
```

### Example Use in a Jenkinsfile

You can add [contrib/jenkins/pyfmt.groovy](contrib/jenkins/pyfmt.groovy) to your Jenkins pipeline
library so that you can use `pyfmt` as a function in your `Jenkinsfile`s. For example,
`pyfmt "src/tests/"`. Read more about how to set that up at
https://jenkins.io/doc/book/pipeline/shared-libraries/ in the "Using Libraries" section.

## Usage

*Just FYI*, `isort` works best when your virtual environment is active (if your src relies on one).
*This will then allow imports to sort in the correct way (system packages, 3rd party packages,
*local/project packages). If you are not in your virtual env, the global Python environment will be
*used which might place your local package imports in with the 3rd party package imports.

```console
usage: pyfmt [-h] [-s {staged,modified,head,local,all}] [-c]
             [--line-length LINE_LENGTH]
             [--commit [{all,patch,amend} [{all,patch,amend} ...]]]
             [--commit-message COMMIT_MESSAGE]
             [--extra-isort-args EXTRA_ISORT_ARGS]
             [--extra-black-args EXTRA_BLACK_ARGS]
             [PATH]

positional arguments:
  PATH                  path to base directory where pyfmt will be run
                        (default: $$BASE_CODE_DIR or '.')

optional arguments:
  -h, --help            show this help message and exit
  -s {staged,modified,head,local,all}, --select {staged,modified,head,local,all}
                        filter which files to format in PATH:
                        > staged    files in the index
                        > modified  files in the index, working tree, and
                                    untracked files
                        > head      files changed in HEAD
                        > local     files changed locally but not upstream
                        > all       (default) all files
  -c, --check           don't write changes, just print the files that would be
                        formatted
  --line-length LINE_LENGTH
                        max characters per line (default: $$MAX_LINE_LENGTH or
                        100)
  --commit [{all,patch,amend} [{all,patch,amend} ...]]
                        commit changes if any files were formatted:
                        > all     commit all files in tree, whether or not they
                                  were formatted
                        > patch   commit formatted files with --patch
                        > amend   commit formatted files with --amend
  --commit-message COMMIT_MESSAGE
                        if --commit=message, this is used as the commit message
                        (WARNING: this will auto-commit any changes!)
  --extra-isort-args EXTRA_ISORT_ARGS
                        additional args to pass to isort
  --extra-black-args EXTRA_BLACK_ARGS
                        additional args to pass to black
```

* `--check` returns non-zero exist status if files need formatting, but doesn't modify files. This
  is appropriate for CI systems where you might want to fail a build if the code is not formatted
  correctly.
* If no specific path is specified, all files in the current directory and all sub directories where
  you run the code will be formatted.
* As a matter of convenience, you may set `$BASE_CODE_DIR` in your environment and run the script
  in the case this is better for your needs.
