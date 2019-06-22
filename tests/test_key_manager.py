""" Unit tests live here"""
from jimpass.managers.bitwarden import BitwardenSession
from jimpass.util import srun
import time
import os
import json


class TestKeyManager(object):
    """Testing the Key Manager Class"""

    @property
    def password(self):
        return os.environ["BITWARDEN_PASSWORD"]

    def generate_session(self):
        """
        Generates a new session_key
        :return: the session_key and the key_id for keyctl to find it
        """
        srun("keyctl purge user bw_session &> /dev/null", no_output=True)
        exit_code, session_key = srun("bw unlock --raw", stdin=self.password)
        assert(exit_code == 0)
        assert(len(session_key) > 0)
        exit_code, key_id = srun("keyctl padd user bw_session @u", stdin=session_key)
        assert(exit_code == 0)
        return session_key, key_id

    def test_get_no_autolock(self):
        session, _ = self.generate_session()
        mgr = BitwardenSession(auto_lock=False)
        session_from_mgr: str = mgr.get_session()
        # Since the session was already generated, simply retrieve it
        assert(session_from_mgr == session)

    def test_set_with_autolock(self):
        timeout = 3
        session, _ = self.generate_session()
        mgr = BitwardenSession(auto_lock=True, timeout=timeout)
        srun("keyctl purge user bw_session &> /dev/null", no_output=True)
        mgr.set_session(session)
        time.sleep(timeout+1)
        exit_code, _ = srun("keyctl request user bw_session")
        assert(exit_code != 0)
        # reset keyctl for other functions
        self.generate_session()

    def test_fetch_items(self):
        mgr = BitwardenSession(auto_lock=False)
        session = mgr.get_session()
        resultcode, items_str = srun(f"bw list items --session '{session}' 2> /dev/null")
        items = json.loads(items_str)
        assert(len(items) > 0 and resultcode == 0)
