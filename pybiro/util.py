""" Util functions """
from subprocess import PIPE, DEVNULL, run, Popen
import yaml

def get_file_config(file: str) -> dict:
    """ Complement context with user configuration """
    with open(file, 'r') as f:
        return yaml.parse(f)

def srun(input_cmd: str, stdin: str = None) -> (int, str):
    """ Wrapper for subprocess_run """
    if stdin:
        res = Popen(input_cmd, stdout=PIPE, stderr=DEVNULL, stdin=PIPE, shell=True)
        output = res.communicate(bytes(stdin, 'utf-8'))[0].decode()
        return res.returncode, output
    else:
        res = run(input_cmd, stdout=PIPE, stderr=DEVNULL, encoding="utf-8", shell=True)
        return res.returncode, res.stdout
