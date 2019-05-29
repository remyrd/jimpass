"""Test functions in util.py"""
from pybiro.util import get_file_config, srun
from os import environ, path
import yaml


def test_get_file_config():
    config = {
        'foo': 'bar'
    }
    config_path: str = ""
    if 'XDG_CONFIG_HOME' in environ:
        if path.isdir(f"{environ['XDG_CONFIG_HOME']}/pybiro"):
            config_path = f"{environ['XDG_CONFIG_HOME']}/pybiro/config"
    elif 'HOME' in environ:
        config_path = f"{environ['HOME']}/.pybiro"
    assert(len(config_path) > 0)
    with open(config_path, 'w') as new_config_f:
        yaml.dump(config, new_config_f)
    # TODO
    result = get_file_config(config_path)
    deletion_return_code = srun(f"rm {config_path}")[0]
    assert(deletion_return_code == 0)
