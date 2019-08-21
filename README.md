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
