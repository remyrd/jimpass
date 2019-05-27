""" Python Bitwarden Rofi """
from pybiro.util import srun
from pybiro.commands import rofi
import click


def get_key() -> str:
    """ Get the key holding the session hash """
    code, stdout = srun("keyctl request user bw_session")
    return stdout if code == 0 else None


def set_key(session_key: str, timeout: int):
    """ Set the key holding the session hash """
    code, key_id = srun("keyctl padd user bw_session @u", stdin=session_key)
    if timeout > 0:
        code, stdout = srun(f"keyctl timeout \"{key_id}\" {timeout}")
    elif timeout == 0:
        code, stdout = srun("keyctl purge user bw_session")


@click.command()
@click.option('-a/-n', '--auto-lock/--no-auto-lock')
@click.option('--lock-timer', type=int, default=0)
def cli(auto_lock, lock_timer):
    """ Unlock the Vault"""
    print(f"{auto_lock} {lock_timer}")
    key = get_key()
    if not key:
        code, passwd = rofi.run(
            dmenu='',
            p='"Master Password"',
            password='',
            lines=0
        )
        code, session_key = srun(f"bw unlock 2> /dev/null "
                                 "| grep 'export' "
                                 "| sed -E 's/.*export BW_SESSION=\"(.*==)\"$/\\1/'",
                                 stdin=passwd)
        set_key(session_key, lock_timer if auto_lock else -1)
