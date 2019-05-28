""" Unit tests live here"""
from pybiro.key_manager import KeyManager
import pytest


class TestKeyManager(object):
    """Testing the Key Manager Class"""
    def test_get(self):
        mgr = KeyManager(auto_lock=False)
        session: str = mgr.key
        assert(len(session) > 0)
        pass

    def test_set(self):
        pass
