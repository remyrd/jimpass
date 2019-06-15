from pybiro.controller import Controller
from pybiro.managers.bitwarden import Bitwarden
from pybiro.config import defaults


def test_flow():
    config = defaults
    controller = Controller(config, {'bitwarden': Bitwarden})
    controller.show_items()
