from setuptools import setup
from codecs import open
from os import path

VERSION = "1.0"
DESCRIPTION = "PV-Simulator"

here = path.abspath(path.dirname(__file__))

with open(path.join(here, "README.md"), encoding="utf-8") as filein:
    long_description = filein.read()

with open(path.join(here, "requirements.txt"), encoding="utf-8") as filein:
    requirements = [line.strip() for line in filein.readlines()]

setup(
    name="pvsimulator",
    version=VERSION,
    description=DESCRIPTION,
    long_description=long_description,
    url="https://github.com/mianamir/",
    author="Muhammad Amir",
    author_email="mianamirlahore@gmail.com",
    classifiers=["Programming Language :: Python :: 3"],
    packages=["pvsimulator"],
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "pvsimulator=pvsimulator.app:main"
        ]
    }
)
