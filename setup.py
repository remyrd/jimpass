""" Setup.py """
from setuptools import setup, find_packages


setup(
    name="Jimpass",
    author="Remy Rojas",
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
        'console_scripts': [
            'jp=jimpass.cli:cli',
            'jimpass=jimpass.cli:cli'
        ]
    },
)
