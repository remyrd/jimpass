""" Setup.py """
from setuptools import setup, find_packages

with open("README.md", "r") as f:
    ld = f.read()

setup(
    name="Jimpass",
    version="0.0.1-alpha",
    author="Remy Rojas",
    author_email="remy.rojas@pm.me",
    description="A universal password manager interface, powered by Rofi",
    long_description=ld,
    long_description_content_type="text/markdown",
    url="https://github.com/remyrd/jimpass",
    classifiers=[
        "Operating System :: Unix",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)"
    ],
    install_requires=[
        "Click",
        "Pyaml",
        "Parse",
        "Deepdiff"
    ],
    setup_requires=[
        "pytest-runner"
    ],
    tests_require=[
        "pytest"
    ],
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "jp=jimpass.cli:cli",
            "jimpass=jimpass.cli:cli"
        ]
    },
)
