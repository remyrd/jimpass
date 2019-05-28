""" Python Bitwarden Rofi """
from pybiro.key_manager import KeyManager
import click


@click.command()
@click.option('-a/-n', '--auto-lock/--no-auto-lock', default=True)
@click.option('--lock-timer', type=int, default=0)
def cli(auto_lock, lock_timer):
    """ CLI Entrypoint """
    key_mgr = KeyManager(lock_timer, auto_lock)
