from parse import parse


class Parser(object):
    """
    Converts items in a password manager's database from/to the user's template string
    based on a model
    """
    def __init__(self, template_str: str, mapping: dict):
        """
        :param template_str: retrieved from configuration
        eg. "account <b>{name}</b> with user {username}"
        :param mapping: maps parameters in template_str to an field in the database item
        eg. {'name': 'name', 'username': 'login.username'}
        """
        self._template_str = template_str
        self.mapping = mapping

    @property
    def template_str(self) -> str:
        return self._template_str

    @template_str.setter
    def template_str(self, template_str):
        self._template_str = template_str

    def fetch_param_from_dict(self, item: dict, param_name: str) -> str:
        if param_name not in self.mapping.keys():
            raise Exception("Requested parameter is not mapped to a field in item dictionary"
                            f"Available mappings are:\n {','.join(self.mapping.keys())}")
        param_path = self.mapping[param_name].split('.')
        sub = item
        for p in param_path:
            if p not in sub:
                return "?"
            sub = sub[p]
        return str(sub) if sub else "?"

    def dumps(self, item: dict) -> str:
        return self.template_str.format(**item)

    def flat_map_item(self, original_item: dict) -> dict:
        """
        Make a flat map out of an item
        :param original_item: fetched from the database
        :return: its flat map according to `login_parser_mapping`
        """
        new_item = {}
        for k in self.mapping.keys():
            new_item[k] = self.fetch_param_from_dict(original_item, k)
        return new_item

    def loads(self, item_str: str) -> dict:
        params = parse(self.template_str, item_str).named
        for key in params.keys():
            if key not in self.mapping:
                raise Exception("Unkown variable in template string")
        res = {}
        for param_name, val in params.items():
            if val not in '?':
                res[param_name] = val
        return res

    def str_matches_mapping(self, item_str: str) -> bool:
        """
        Checks if string matches the password manager's template str
        :param item_str:
        :return:
        """
        parse_result = parse(self.template_str, item_str)
        if not parse_result:
            return False
        params = parse_result.named
        for key in params.keys():
            if key not in self.mapping:
                return False
        return True

