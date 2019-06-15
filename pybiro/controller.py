from pybiro.managers.base import PasswordManager
from pybiro.util import rofi, srun


class Controller(object):
    def __init__(self, config: dict, managers: dict):
        self.managers = managers
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

        for name in self.managers.keys():
            self.managers[name] = self.managers[name](self.config)

    def _get_keybinding(self, exit_code: int) -> int:
        for k in self.keybindings:
            if k.exit_code == exit_code:
                return self.keybindings.index(k)
        # Default to 0 in case of doubt
        return 0

    def _output_switcher(self, exit_code: int, item_list: [dict], mgr: PasswordManager):
        """
        Choose the method to execute based on its name
        :param exit_code: the exit code returned by rofi
        :param item_list: a list of database items from a single password manager
        :param mgr: the Password Manager
        :return:
        """
        # rofi returns exit codes from 10 - 18 corresponding to kb-custom-1 - kb-custom-9
        if exit_code > 0:
            exit_code -= 9

        kb = self.keybindings[self._get_keybinding(exit_code)]
        callback = getattr(self, f"_{kb.callback}", lambda: 'Method does not exist!')
        return callback(
            self.deduplicate(item_list, mgr)[1] if item_list else None,
            mgr)

    def _type_all(self, item, mgr):
        self._type_user(item, mgr)
        srun("xdotool key Tab")
        self._type_pass(item, mgr)

    @staticmethod
    def _type_user(item, mgr):
        username = mgr.parser.fetch_param_from_dict(item, "username")
        srun(f"xdotool type \"{username}\"")

    @staticmethod
    def _type_pass(item, mgr):
        password = mgr.parser.fetch_param_from_dict(item, "password")
        srun(f"xdotool type \"{password}\"")

    @staticmethod
    def copy_pass(item, mgr):
        pass

    def _generate_instructions(self):
        pass

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
                                   args={'mesg': self.config["message"]},
                                   stdin=rofi_input)
        print(exit_code)
        # if response and exit_code in self.exit_code_to_output.keys():
        if response:
            result_list = [(mgr, mgr.search(mgr.parser.loads(response)))
                           for name, mgr in self.managers.items()
                           if mgr.parser.str_matches_mapping(response)]
            if len(result_list) != 1:
                raise Exception("The item matches more than one Password Manager")
            found_items = result_list[0][1]
            mgr = result_list[0][0]
            self._output_switcher(exit_code,
                                  found_items,
                                  mgr)

    def deduplicate(self, items: [dict], mgr: PasswordManager) -> (int, dict):
        if len(items) == 1:
            return 0, items[0]
        else:
            mgr.parser.template_str = mgr.full_template_str
            rofi_input = mgr.stringify_items(items)
            exit_code, response = rofi(prompt="Deduplicate",
                                       keybindings=self.keybindings,
                                       options=['i', 'no-custom'],
                                       args={'mesg': self.config["message"]},
                                       stdin=rofi_input)
            if response:
                item = mgr.search(mgr.parser.loads(response))
                return exit_code, item
        return exit_code, None


class KeyBinding(object):
    """
    Simple struct to represent a keybinding
    """
    def __init__(self, exit_code: int, callback: str, mapping: str = 'return'):
        self._exit_code = exit_code
        self._mapping = mapping
        self._callback = callback

    @property
    def exit_code(self) -> int:
        return self._exit_code

    @exit_code.setter
    def exit_code(self, exit_code: int):
        self._exit_code = exit_code

    @property
    def mapping(self) -> str:
        return self._mapping

    @mapping.setter
    def mapping(self, mapping: str):
        self._mapping = mapping

    @property
    def callback(self):
        return self._callback

    @callback.setter
    def callback(self, callback: str):
        self._callback = callback


