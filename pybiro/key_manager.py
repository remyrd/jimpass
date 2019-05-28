""" Singleton managing session key"""
from pybiro.util import srun
from pybiro.commands import rofi


class KeyManager(object):
    """Manages session key by calling keyctl through subprocess"""
    def __init__(self, timeout: int, auto_lock: bool):
        self.auto_lock = auto_lock
        self.timeout = timeout if auto_lock else -1
        self._key = None

    @property
    def key(self) -> str:
        """ Get the key holding the session hash """
        code, stdout = srun("keyctl request user bw_session")
        if code != 0 or not stdout:
            code, passwd = rofi.run(
                dmenu='',
                p='"Master Password"',
                password='',
                lines=0
            )
            code, session_key = srun(f"bw unlock 2> /dev/null "
                                     "| grep 'export' "
                                     "| sed -E 's/.*export BW_SESSION=\"(.*==)\"$/\\1/'",
                                     stdin=passwd)
            self._key = session_key
        else:
            self._key = stdout
            return self._key

    @key.setter
    def key(self, session_key: str):
        """ Set the key holding the session hash """
        if session_key:
            code, key_id = srun("keyctl padd user bw_session @u", stdin=session_key)
            if self.timeout > 0:
                if srun(f"keyctl timeout \"{key_id}\" {self.timeout}")[0] != 0:
                    raise Exception(f"Couldn't set timeout for key_id {key_id}")
            elif self.timeout == 0:
                if srun("keyctl purge user bw_session")[0] != 0:
                    raise Exception(f"Couldn't purge key_id {key_id}")
