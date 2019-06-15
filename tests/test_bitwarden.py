from pybiro.controller import Controller
from pybiro.managers.bitwarden import Bitwarden
from pybiro.config import DEFAULTS


def test_flow():
    config = DEFAULTS
    controller = Controller(config, {'bitwarden': Bitwarden})
    controller.show_items()
