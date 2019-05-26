""" Python Bitwarden Rofi """
from commands.rofi import run
from os import system as sh
import click


def get_key() -> str:
    """ Get the key holding the session hash """
    return sh("keyctl request user bw_session 2> /dev/null") or None


def set_key(session: str, timeout: int):
    """ Set the key holding the session hash """
    key_id = sh(f"echo \"{session}\" | keyctl padd user bw_session @u")
    if timeout > 0:
        sh(f"keyctl timeout \"{key_id}\" {timeout} 2> /dev/null")
    elif timeout == 0:
        sh("keyctl purge user bw_session &> /dev/null")


@click.command()
def unlock():
    """ Unlock the Vault"""
    timeout = 0
    key = get_key()
    if not key:
        passwd: str = run(
            dmenu='',
            p='"Master Password"',
            password='',
            lines=0
        )
        key = sh(f"echo {passwd} | bw unlock 2> /dev/null "
                 "| grep 'export' "
                 "| sed -E 's/.*export BW_SESSION=\"(.*==)\"$/\\1/'")
    set_key(key, timeout)
