""" Calls Rofi on the system """
import os


def run(**kwargs):
    """ Run Rofi """
    args = " ".join([f"-{k} {v}" for k, v in kwargs.items()])
    os.system(f"rofi {args}")
