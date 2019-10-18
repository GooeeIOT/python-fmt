import os
from pathlib import Path

from setuptools import setup


def readme():
    with open(os.path.join(os.path.dirname(__file__), "README.md")) as handle:
        return handle.read()


setup(
    name="pyfmt",
    version="1.0.0",
    license="MIT",
    url="https://github.com/GooeeIOT/pyfmt",
    description="Python auto-formatting using isort and black.",
    long_description=readme(),
    packages=["pyfmt"],
    entry_points={"console_scripts": ["pyfmt = pyfmt.__main__:main"]},
)
