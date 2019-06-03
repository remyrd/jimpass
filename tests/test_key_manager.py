""" Unit tests live here"""
from pybiro.managers.bitwarden import SessionManager
from pybiro.util import srun
import json


class TestKeyManager(object):
    """Testing the Key Manager Class"""

    def test_get(self):
        mgr = SessionManager(auto_lock=False)
        session: str = mgr.get_session()
        assert(len(session) > 0)

    def test_fetch_items(self):
        mgr = SessionManager(auto_lock=False)
        session = mgr.get_session()
        resultcode, items_str = srun(f"bw list items --session {session} 2> /dev/null")
        items = json.loads(items_str)
        assert(len(items) > 0 and resultcode == 0)
