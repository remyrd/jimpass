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
        return str(sub)

    def dumps(self, item_dict: dict) -> str:

        flat_mapping = dict(
            [(k, self.fetch_param_from_dict(item_dict, k)) for k, v in self.mapping.items()])
        return self.template_str.format(**flat_mapping)

    def _mapping_string_to_dict(self, dict_mapping: list, value: str, sub: dict) -> dict:
        """
        DF recursive update a dictionnary at the specified position
        :param dict_mapping: dot-separated mapping where to write the value
        :param value: value to write
        :param sub: sub-tree of the dictionnary specified by `dict_mapping
        :return:
        """
        if len(dict_mapping) > 1:
            if dict_mapping[0] not in sub:
                sub[dict_mapping[0]] = {}
            sub[dict_mapping[0]] = self._mapping_string_to_dict(dict_mapping[1:], value, sub[dict_mapping[0]])
        else:
            sub[dict_mapping[0]] = value
        return sub

    def loads(self, item_str: str) -> dict:
        params = parse(self.template_str, item_str).named
        for key in params.keys():
            if key not in self.mapping:
                raise Exception("Unkown variable in template string")
        res = {}
        for param_name in params.keys():
            self._mapping_string_to_dict(self.mapping[param_name].split('.'), params[param_name], res)
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

