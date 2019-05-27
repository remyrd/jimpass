""" Calls Rofi on the system """
import os
from pybiro.util import srun


def run(**kwargs):
    """ Run Rofi """
    args = " ".join([f"-{k} {v}" for k, v in kwargs.items()])
    return srun(f"rofi {args}")
