""" Util functinos """
from typing import List
import subprocess
import sys


def srun(cmd: List[str]) -> (int, bytes):
    """ Wrapper for subprocess_run """
    if sys.version_info > (3, 6):
        res = subprocess.run(cmd, stdout=subprocess.PIPE)
    else:
        res = subprocess.run(cmd, capture_output=True)
    return res.returncode, res.stdout
