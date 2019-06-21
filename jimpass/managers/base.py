""" Abstract backend """
from abc import ABCMeta, abstractmethod
from deepdiff import DeepDiff
from jimpass.parser import Parser


class PasswordManager(metaclass=ABCMeta):
    """
    Since there is only one backend for now, we will let concrete managers define the flow.
    In the future though, flow should be guided by abstract methods
    """
    def __init__(self, config: dict, name: str):
        """
        :param config:  must include `managers`
        :param name: the password manager's name in the config
        """
        self.config = config
        self.pm_config = config[name]
        self._items = []
        self._parser = None
        self._name = name
        self._full_template_str = "{id}"
        self._current_template_str = None

    @abstractmethod
    def _fetch_all_items(self) -> [dict]:
        pass

    @property
    def name(self):
        return self._name

    @property
    def items(self) -> list:
        return self._items

    @property
    def parser(self) -> Parser:
        return self._parser

    @property
    def full_template_str(self) -> str:
        return self._full_template_str

    @staticmethod
    def _is_sub_dict(d1: dict, d2: dict) -> bool:
        """
        :param d1: contained in d2
        :param d2: contains d1
        :return: if d2 contains all fields in d1
        """
        diff = DeepDiff(d1, d2)
        return 'dictionary_item_added' in diff and len(diff) == 1

    def stringify_items(self, items: [dict] = None) -> str:
        """
        Leverage parser to render each database item according to the configured template
        :return: line-separated items to display
        """
        if not items:
            items = self.items
        return '\n'.join([
            self._parser.dumps(item)
            for item in items])

    def search(self, stub: dict) -> [dict]:
        """
        Fetches an item from the database based on a partial dict
        :param stub: dict with partial information to match with items in the db
        :return: a list of matching database items
        """
        return [item
                for item in self.items
                if self._is_sub_dict(stub, item)]

    def get_totp(self, item) -> str:
        """
        Get the item's TOTP 2FA. Subclass implements if supported.
        Default behaviour is empty string
        """
        return ""

