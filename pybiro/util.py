""" Util functions """
from subprocess import PIPE, DEVNULL, run, Popen
from os import environ, path
from pybiro.config import defaults
from parse import parse
import yaml


def read_config_file(file: str) -> dict:
    """
    Complement context with user configuration
    TODO: schema verification
    """
    with open(file, 'r') as f:
        return yaml.parse(f)


def get_config(config_path: str = None) -> dict:
    """
    Provide configuration based on canonical paths or default
    """
    if not config_path:
        if 'XDG_CONFIG_HOME' in environ:
            if path.isdir(f"{environ['XDG_CONFIG_HOME']}/pybiro"):
                config_path = f"{environ['XDG_CONFIG_HOME']}/pybiro/config"
        if 'HOME' in environ and not config_path:
            if path.isfile(f"{environ['HOME']}/.pybiro"):
                config_path = f"{environ['HOME']}/.pybiro"
    return read_config_file(config_path) if config_path else defaults


def srun(input_cmd: str, stdin: str = None) -> (int, str):
    """
    Wrapper for subprocess_run
    """
    if stdin:
        res = Popen(input_cmd, stdout=PIPE, stderr=DEVNULL, stdin=PIPE, shell=True)
        output = res.communicate(bytes(stdin, 'utf-8'))[0].decode()
        return res.returncode, output
    else:
        res = run(input_cmd, stdout=PIPE, stderr=DEVNULL, encoding="utf-8", shell=True)
        return res.returncode, res.stdout


def rofi(mode: str = "dmenu", prompt: str = None, options: list = None,
         keybindings: list = None, args: dict = None, stdin: str = None) -> (int, str):
    """
    Run Rofi
    """
    cmd = "rofi "
    if mode:
        cmd += f"-{mode} "
    if prompt:
        cmd += f"-p \"{prompt}\" "
    if options:
        cmd += " ".join([f"-{opt}" for opt in options]) + " "
    if keybindings:
        cmd += " ".join([f"-kb-custom-{keybindings.index(kb)+1} {kb}" for kb in keybindings]) + " "
    if args:
        cmd += " ".join([f"-{key} {val}" for key, val in args.items()]) + " "
    return srun(cmd, stdin) if stdin else srun(cmd)


class Parser(object):
    """
    Converts items in the database (dict) from/to the user's template string
    """
    def __init__(self, template_str: str, mapping: dict):
        """
        :param template_str: retrieved from configuration
        eg. "account <b>{name}</b> with user {username}"
        :param mapping: maps parameters in template_str to an field in the database item
        eg. {'name': 'name', 'username': 'login.username'}
        """
        self.template_str = template_str
        self.mapping = mapping

    def _fetch_param_from_dict(self, item: dict, param_name: str) -> str:
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
            [(k, self._fetch_param_from_dict(item_dict, k)) for k, v in self.mapping.items()])
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

