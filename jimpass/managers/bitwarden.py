from jimpass.util import srun, rofi
from jimpass.managers.base import PasswordManager
from jimpass.parser import Parser
import json

item_types = {
    'LOGIN': 1,
    'NOTE': 2,
    'CARD': 3,
    'IDENTITY': 4
}

# How to find fields in the item
login_parser_mapping = {
    'name': 'name',
    'username': 'login.username',
    'id': 'id',
    'password': 'login.password'
}


class Bitwarden(PasswordManager):
    def __init__(self, config: dict):
        PasswordManager.__init__(self, config, 'bitwarden')
        self.session_mgr = BitwardenSession(self.config["timeout"], self.config["auto_lock"])
        self._parser = Parser(self.pm_config['template_str'], login_parser_mapping)
        self.session = self.session_mgr.get_session()
        self._items = self._fetch_all_items()
        self._full_template_str = "{name}: {username} ({id})"

    def _fetch_all_items(self) -> [dict]:
        """
        Get the items list and filter for logins
        :return: list of all items
        """
        item_str = srun(f"bw list items --session {self.session} 2>/dev/null")[1]
        return [item
                for item in json.loads(item_str, encoding='utf-8')
                if item['type'] == item_types['LOGIN']]


class BitwardenSession(object):
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
                prompt='Bitwarden Master Password',
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
