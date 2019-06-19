"""
Controller.
Interface with both Password Managers and Rofi
"""
import time
from typing import NamedTuple
from jimpass.managers.base import PasswordManager
from jimpass.util import rofi, srun

COPY_COMMANDS = {
    'xclip': {
        'get': 'xclip -selection clipboard -o',
        'set': 'xclip -selection clipboard -r',
        'clear': 'echo -n "" | xclip -selection clipboard -r'
    },
    'xsel': {
        'get': 'xsel --clipboard',
        'set': 'xsel --clipboard --input',
        'clear': 'xsel --clipboard --clear'
    },
    'wayland': {
        'get': 'wl-paste',
        'set': 'wl-copy',
        'clear': 'wl-copy --clear'
    }
}


class Controller:
    """
    Instantiates password managers and handles user interaction
    """
    def __init__(self, config: dict, managers: dict):
        self.managers = {}
        self.config = config
        self.context = 'base'
        self.keybindings: [KeyBinding] = [
            KeyBinding(exit_code=0, callback='copy_pass')
        ]
        for callback, mapping in config['keybindings'].items():
            non_overlapping_exit_code = len(self.keybindings)
            self.keybindings.append(
                KeyBinding(exit_code=non_overlapping_exit_code,
                           mapping=mapping,
                           callback=callback)
            )
        for name in self.config['managers']:
            self.managers[name] = managers[name](self.config)

    def _get_keybinding(self, exit_code: int) -> int:
        for k in self.keybindings:
            if k.exit_code == exit_code:
                return self.keybindings.index(k)
        # Default to 0 in case of doubt
        return 0

    def _output_switcher(self,
                         exit_code: int,
                         item_list: [dict],
                         mgr: PasswordManager):
        """
        Choose the method to execute based on its name
        When not 0, rofi can be configured to return exit codes from 10 - 18
        corresponding to kb-custom-1 - 9
        :param exit_code: the exit code returned by rofi
        :param item_list: database items from a single password manager
        :param mgr: the Password Manager
        :return:
        """
        if exit_code > 0:
            exit_code -= 9

        key_bind = self.keybindings[self._get_keybinding(exit_code)]
        callback = getattr(self,
                           f"_{key_bind.callback}",
                           lambda: 'Method does not exist!')
        if len(item_list) == 1:
            return callback(item_list[0], mgr)
        return callback(
            self._deduplicate(item_list, mgr)[1] if item_list else None,
            mgr)

    def _type_all(self, item, mgr):
        self._type_user(item, mgr)
        srun("xdotool key Tab")
        self._type_pass(item, mgr)

    @staticmethod
    def _type_user(item, mgr):
        time.sleep(0.2)
        username = mgr.parser.fetch_param_from_dict(item, "username")
        srun(f"xdotool type \"{username}\"")

    def _type_pass(self, item, mgr):
        time.sleep(0.2)
        password = mgr.parser.fetch_param_from_dict(item, "password")
        srun(f"xdotool type \"{password}\"")
        if self.config['danger_mode']:
            srun("xdotool key Return")

    def _copy_pass(self, item, mgr):
        copy_command = COPY_COMMANDS[self.config['copy_command']]
        password = mgr.parser.fetch_param_from_dict(item, "password")
        srun(f"echo -n \"{password}\" | {copy_command['set']}", no_output=True)
        time.sleep(self.config['clipboard_timeout'])
        if srun(copy_command['get'])[1] == password:
            srun(copy_command['clear'], no_output=True)

    def _generate_instructions(self) -> str:
        return " | ".join(
            [f"{kb.callback}: {kb.mapping}" for kb in self.keybindings]
        )

    def show_items(self):
        """
        Show items using rofi and return its reponse code and the parsed item
        :return:
        """
        rofi_input = '\n'.join([mgr.stringify_items()
                                for name, mgr in self.managers.items()])
        exit_code, response = rofi(prompt="Name",
                                   keybindings=self.keybindings,
                                   options=['i', 'no-custom'],
                                   args={'mesg': f"{self._generate_instructions()}"},
                                   stdin=rofi_input)
        # if response and exit_code in self.exit_code_to_output.keys():
        if response:
            result_list = [(mgr, mgr.search(mgr.parser.loads(response)))
                           for name, mgr in self.managers.items()
                           if mgr.parser.str_matches_mapping(response)]
            if len(result_list) != 1:
                raise Exception("The item found in more than one Manager")
            found_items = result_list[0][1]
            mgr = result_list[0][0]
            self._output_switcher(exit_code,
                                  found_items,
                                  mgr)

    def _deduplicate(self, items: [dict], mgr: PasswordManager) -> (int, dict):
        mgr.parser.template_str = mgr.full_template_str
        rofi_input = mgr.stringify_items(items)
        exit_code, response = rofi(prompt="Deduplicate",
                                   keybindings=self.keybindings,
                                   options=['i', 'no-custom'],
                                   args={'mesg': self._generate_instructions()+"\n Entries duplicated!"},
                                   stdin=rofi_input)
        if response:
            item = mgr.search(mgr.parser.loads(response))
            return exit_code, item
        return exit_code, None


class KeyBinding(NamedTuple):
    exit_code: int
    callback: str
    mapping: str = "Return"
