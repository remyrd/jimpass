""" Abstract backend """
from abc import ABCMeta
from pybiro.frontends.rofi import Rofi


class Backend(metaclass=ABCMeta):
    """
    Since there is only one backend for now, we will let concrete backends define the flow.
    In the future though, we might want to enforce flow through a unifying API and abstract methods
    """
    def __init__(self, config: dict):
        """
        :param config:  must include: `frontend`
        """
        self.config = config
        # TODO move this dict up to the CLI level so that we don't have the import here
        frontends = {
            'rofi': Rofi
        }
        self.frontend = frontends[config['frontend']]()
        self.timeout = config["timeout"]
        self.auto_lock = config["auto_lock"]
