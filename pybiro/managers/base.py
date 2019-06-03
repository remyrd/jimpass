""" Abstract backend """
from abc import ABCMeta


class Backend(metaclass=ABCMeta):
    """
    Since there is only one backend for now, we will let concrete managers define the flow.
    In the future though, flow should be guided by abstract methods
    """
    def __init__(self, config: dict):
        """
        :param config:  must include: `frontend`
        """
        self.config = config
