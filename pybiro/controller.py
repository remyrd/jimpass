from pybiro.util import rofi
from pybiro.managers.base import PasswordManager


class Controller(object):
    def __init__(self, config: dict, managers: dict):
        self.managers: [PasswordManager] = managers
        self.config = config
        self.context = 'base'
        self.exit_code_to_output = {
            0: 'copy_pass',
            1: 'type_all',
            2: 'type_user',
            3: 'type_pass'
        }
        for name in self.managers.keys():
            self.managers[name](self.config[name])

    def _output_switcher(self, method_name: str, item_list: [dict], mgr: PasswordManager):
        method = getattr(self, method_name, lambda: 'Method does not exist!')
        return method(item_list, mgr)

    def _type_all(self, item_list, mgr):
        pass

    def _type_user(self, item_list, mgr):
        pass

    def _type_pass(self, item_list, mgr):
        pass

    def copy_pass(self, item_list, mgr):
        pass

    def _generate_instructions(self):
        pass

    def show_items(self) -> (int, [dict]):
        """
        Show items using rofi and return its reponse code and the parsed item
        :return:
        """
        rofi_input = '\n'.join([mgr.stringify_items()
                                for mgr in self.managers])
        exit_code, response = rofi(prompt="Name",
                                       keybindings=self.config["keybindings"],
                                       options=['i', 'no-custom'],
                                       args={'mesg': self.config["message"]},
                                       stdin=rofi_input)
        if response:
            owning_mgr = [(mgr.name, mgr.search(mgr.parser.loads(response)))
                          for mgr in self.managers
                          if mgr.parser.str_matches_mapping(response)]
            if len(owning_mgr) != 1:
                raise Exception("The item matches more than one Password Manager")
            owning_mgr = owning_mgr[0]
            found_items = owning_mgr[1]
            mgr_name = owning_mgr[0]
            self._output_switcher(self.exit_code_to_output[exit_code],
                                  found_items,
                                  mgr_name)
            return exit_code, found_items
        return exit_code, response

    def handle_response(self, response_code: int, response: [dict]):
        pass
