""" Util functions """
from subprocess import PIPE, DEVNULL, run, Popen
from os import environ, path, listdir
from pybiro.config import DEFAULTS
import yaml


def read_config_file(file: str) -> dict:
    """
    Complement context with user configuration
    TODO: schema verification
    """
    with open(file, 'r') as f:
        return yaml.load(f)


def get_config() -> dict:
    """
    Provide configuration based on canonical paths or default
    """
    if 'XDG_CONFIG_HOME' in environ:
        xdg_h = environ['XDG_CONFIG_HOME']
        if path.isdir(f"{xdg_h}/pybiro"):
            for f in listdir(f"{xdg_h}/pybiro"):
                if f.startswith("conf") and f.endswith(".yaml" or ".yml"):
                    return read_config_file("/".join([xdg_h, 'pybiro', f]))
    if 'HOME' in environ:
        for f in listdir(f"{environ['HOME']}"):
            if f.startswith(".pybiro") and f.endswith(".yaml" or ".yml"):
                return read_config_file(f"{environ['HOME']}/{f}")
    return DEFAULTS


def srun(input_cmd: str, stdin: str = None, no_output: bool = False) -> (int, str):
    """
    Wrapper for subprocess_run
    """
    if stdin:
        res = Popen(input_cmd, stdout=DEVNULL if no_output else PIPE, stderr=DEVNULL, stdin=PIPE, shell=True)
        output = None if no_output else res.communicate(bytes(stdin, 'utf-8'))[0].decode()
        return res.returncode, output
    else:
        res = run(input_cmd, stdout=DEVNULL if no_output else PIPE, stderr=DEVNULL, encoding="utf-8", shell=True)
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
        cmd += " ".join([f"-kb-custom-{kb.exit_code} {kb.mapping}" for kb in keybindings]) + " "
    if args:
        cmd += " ".join([f"-{key} \"{val}\"" for key, val in args.items()]) + " "
    return srun(cmd, stdin) if stdin else srun(cmd)
