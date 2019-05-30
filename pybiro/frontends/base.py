""" Abstract Frontend"""
from abc import ABCMeta, abstractmethod


class Frontend(metaclass=ABCMeta):
    """
    Frontends will be required to implement a unifying API and have no control over the flow
    """
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def display(self, type_: str, items: list, **kwargs):
        pass
