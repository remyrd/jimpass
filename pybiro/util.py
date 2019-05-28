""" Util functinos """
from subprocess import PIPE, DEVNULL, run, Popen


def srun(cmd: str, stdin: str = None) -> (int, bytes):
    """ Wrapper for subprocess_run """
    if stdin:
        res = Popen(cmd, stdout=PIPE, stderr=DEVNULL, stdin=PIPE, shell=True)
        output = res.communicate(bytes(stdin, 'utf-8'))[0].decode()
        return res.returncode, output
    else:
        res = run(cmd, stdout=PIPE, stderr=DEVNULL, encoding="utf-8", shell=True)
        return res.returncode, res.stdout
