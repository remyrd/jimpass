"""Test functions in util.py"""
from jimpass.util import get_config


def test_get_file_config():
    config = get_config()
    assert('managers' in config)
    # TODO: test the contents of {result}
