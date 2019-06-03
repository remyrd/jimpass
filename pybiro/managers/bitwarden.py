""" Singleton managing session key"""
from pybiro.util import srun
from pybiro.managers.base import Backend
from pybiro.util import rofi
import json


class Bitwarden(Backend):
    def __init__(self, config: dict):
        Backend.__init__(self, config)
        self.session_mgr = SessionManager(self.config["timeout"], self.config["auto_lock"])
        self.session = self.session_mgr.get_session()
        self.items = self._get_items()
        # TODO figure out methods to format items in/out for rofi
        self._show_items()

    def _get_items(self) -> list:
        """
        Get the items list
        :return: list of all items
        """
        return json.loads(srun(f"bw list items --session {self.session} 2>/dev/null")[1])

    def _items_to_string(self) -> str:
        """
        TODO
        Uses the display format if configured to render items.
        :return: line-separated items to display
        """
        pass

    def _show_items(self):
        return_code, response = rofi(prompt="Name",
                                     keybindings=self.config["keybindings"],
                                     options=['i', 'no-custom'],
                                     args={'mesg': self.config["message"]},
                                     stdin=self._items_to_string())


class SessionManager(object):
    """
    Manages session key by calling keyctl through subprocess
    """
    def __init__(self, timeout: int = 0, auto_lock: bool = True):
        self.auto_lock = auto_lock
        self.timeout = timeout if auto_lock else -1

    def get_session(self) -> str:
        """ Get the key holding the session hash """
        code, stdout = srun("keyctl request user bw_session")
        if code != 0 or not stdout:
            code, passwd = rofi(
                prompt='Master Password',
                options=[
                    'password'
                ],
                args={
                   'lines': 0
                }
            )
            code, session_key = srun(f"bw unlock 2> /dev/null "
                                     "| grep 'export' "
                                     "| sed -E 's/.*export BW_SESSION=\"(.*==)\"$/\\1/'",
                                     stdin=passwd)
            self.set_session(session_key)
            return session_key
        else:
            return srun(f"keyctl pipe {stdout}")[1]

    def set_session(self, session_key: str):
        """ Set the key holding the session hash """
        if session_key:
            print(session_key)
            code, key_id = srun("keyctl padd user bw_session @u", stdin=session_key)
            if self.timeout > 0:
                if srun(f"keyctl timeout \"{key_id}\" {self.timeout}")[0] != 0:
                    raise Exception(f"Couldn't set timeout for key_id {key_id}")
            elif self.timeout == 0:
                if srun("keyctl purge user bw_session")[0] != 0:
                    raise Exception(f"Couldn't purge key_id {key_id}")
