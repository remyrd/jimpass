""" Unit tests live here"""
from pybiro.backends.bitwarden import KeyManager
from pybiro.util import srun
import json


class TestKeyManager(object):
    """Testing the Key Manager Class"""

    def test_get(self):
        mgr = KeyManager(auto_lock=False)
        session: str = mgr.get_key()
        assert(len(session) > 0)

    def test_fetch_items(self):
        mgr = KeyManager(auto_lock=False)
        session = mgr.get_key()
        resultcode, items_str = srun(f"bw list items --session {session} 2> /dev/null")
        items = json.loads(items_str)
        assert(len(items) > 0 and resultcode == 0)
