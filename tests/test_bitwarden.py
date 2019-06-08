from pybiro.managers.bitwarden import Bitwarden
from pybiro.config import defaults


def test_flow():
    Bitwarden(defaults)
