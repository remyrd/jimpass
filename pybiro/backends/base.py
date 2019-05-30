""" Abstract backend """
from abc import ABCMeta
from pybiro.frontends.base import Frontend


class Backend(metaclass=ABCMeta):
    """
    Since there is only one backend for now, we will let concrete backends define the flow.
    In the future though, we might want to enforce flow through a unifying API and abstract methods
    """
    def __init__(self, config: dict, frontend: Frontend):
        self.config = config
        self.frontend = frontend
