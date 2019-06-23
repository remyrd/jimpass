""" Setup.py """
from setuptools import setup

setup(
    setup_requires=[
        "pytest-runner",
        "pbr"
    ],
    pbr=True,
    tests_require=[
        "pytest"
    ],
    py_modules=['jimpass'],
)
