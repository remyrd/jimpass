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

    def _output_switcher(self, method_name: str, item_list: [dict], mgr_name: PasswordManager):
        method = getattr(self, method_name, lambda: 'Method does not exist!')
        return method(item_list, mgr_name)

    def _type_all(self, item_list, mgr_name):
        pass

    def _type_user(self, item_list, mgr_name):
        pass

    def _type_pass(self, item_list, mgr_name):
        pass

    def copy_pass(self, item_list, mgr_name):
        pass

    def _generate_instructions(self):
        pass

    def show_items(self, item_template: str = None):
        """
        Show items using rofi and return its reponse code and the parsed item
        :return:
        """
        rofi_input = '\n'.join([mgr.stringify_items(item_template)
                                for mgr in self.managers])
        exit_code, response = rofi(prompt="Name",
                                   keybindings=self.config["keybindings"],
                                   options=['i', 'no-custom'],
                                   args={'mesg': self.config["message"]},
                                   stdin=rofi_input)
        if response:
            owning_mgr = [(mgr.name, mgr.search(mgr.parser.loads(response, item_template)))
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

    def deduplicate(self, items: [dict], mgr_name: str) -> (int, dict):
        mgr: PasswordManager = self.managers[mgr_name]
        rofi_input = '\n'.join(mgr.stringify_items(mgr.full_template_str))
        exit_code, response = rofi(prompt="Deduplicate",
                                   keybindings=self.config["keybindings"],
                                   options=['i', 'no-custom'],
                                   args={'mesg': self.config["message"]},
                                   stdin=rofi_input)
        if response:
            item = mgr.search(mgr.parser.loads(response, mgr.full_template_str))
            return exit_code, item
        return exit_code, None
