""" Util functions """
from subprocess import PIPE, DEVNULL, run, Popen
from os import environ, path
from pybiro.config import defaults
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
