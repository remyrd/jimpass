from jimpass.util import srun
from jimpass.managers.base import PasswordManager
from jimpass.parser import Parser

parser_mapping = {
    'id': 'id',
    'name': 'name',
    'fullname': 'fullname',
    'username': 'username',
    'password': 'password',
    'last_modified': 'last_modified_gmt',
    'last_touch': 'last_touch',
    'group': 'group',
    'url': 'url',
    'note': 'note'
}


class Lastpass(PasswordManager):
    def __init__(self, config: dict):
        PasswordManager.__init__(self, config, 'lastpass')
        self._parser = Parser(self.pm_config['template_str'], parser_mapping)
        self._do_log_in()
        self._items = self.fetch_all_items()
        self._full_template_str = "{name} ({fullname}): {username}, {url}, {group}, ({id})"

    def _do_log_in(self):
        exit_code, _ = srun("lpass status -q", no_output=True)
        if exit_code == 1:
            srun(f"lpass login --trust {self.pm_config['username']}")
        elif exit_code == 0:
            return
        else:
            raise Exception("Couldn't use LastPass, verify it's installed")

    def fetch_all_items(self) -> [dict]:
        """
        Lastpass supports exporting items into CSV
        :return: flat list of items converted into dict
        """
        exit_code, items_csv = srun("lpass export --fields=id,name,fullname,username,"
                                    "password,last_modified_gmt,last_touch,group,url,note")
        if exit_code != 0:
            raise Exception("Something went wrong retrieving Lastpass items")
        keys = items_csv.split('\n')[0]
        lines = items_csv.split('\n')[1:]
        items = [
            {k: v for k, v in zip(keys.split(','), line.split(','))}
            for line in lines
        ]
        return items

