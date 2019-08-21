# pyfmt

Python auto formatting using `isort` and `black`.

## Installation


### Dependencies

Install `isort` and `black`. 

```
pip3 install isort black
```

### Make command available system wide

You have a few options depending on your preference.

1. `/Absolute/Path/To/Directory/with/pyfmt` every time (eww)
1. `cp` [bin/pyfmt](bin/pyfmt) to `/usr/local/bin` or somewhere in `$PATH`. 
2. Check this repo out somewhere and add `bin/` to `$PATH`
   ```shell
   BASE_DIR=$(pwd)
   ln -sf ${BASE_DIR}/git_hooks/pre-push ${BASE_DIR}/.git/hooks
   ```

## Usage

```shell
USAGE: pyfmt [--check] [specific files]
You may also export BASE_CODE_DIR= to point at the code to be formatted
```

* `--check` returns non-zero exist status only and doesn't modify files. This is appropriate for 
  CI systems where you might want to fail a build if the code is not formatted correctly.
* if no specific files specified, all files in the current directory and all sub directories where
  you run the code will be formatted
* as a matter of convenience, you may set `$BASE_CODE_DIR` in your environment and run the script
  in the case this is better for your needs
