""" Setup.py """
from setuptools import setup


setup(
    name="Pybiro",
    author="Remy Rojas",
    install_requires=[
        "Click",
    ],
    entry_points={
        'console_scripts': [
            'pbr=pybiro:unlock'
        ]
    },
)
