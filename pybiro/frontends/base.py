""" Abstract Frontend"""
from abc import ABCMeta, abstractmethod


class Frontend(metaclass=ABCMeta):
    """
    Frontends will be required to implement a unifying API and have no control over the flow
    """
    def __init__(self, config):
        self.config = config

    @abstractmethod
    def user_input(self, **kwargs):
        pass

    @abstractmethod
    def display_one_item(self, item, **kwargs):
        pass

    @abstractmethod
    def display_multiple_items(self, items, **kwargs):
        pass
