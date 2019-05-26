""" Python Bitwarden Rofi """
from pybiro.commands.rofi import run
from os import system as sh
from typing import List
import pybiro.util
import subprocess
import sys
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
@click.option('-a/-n', '--auto-lock/--no-auto-lock')
@click.option('--lock-timer', type=int)
def cli(auto_lock, lock_timer):
    """ Unlock the Vault"""
    print(f"{auto_lock} {lock_timer}")
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
