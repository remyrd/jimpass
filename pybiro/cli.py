""" Python Bitwarden Rofi """
from pybiro.managers.bitwarden import Bitwarden
from pybiro.util import get_config
import click

managers = {
    'bitwarden': Bitwarden
}


@click.command()
@click.option('-a/-n', '--auto-lock/--no-auto-lock', default=True)
@click.option('--lock-timer', type=int, default=0)
@click.option('-c', '--config-file', type=str)
def cli(auto_lock, lock_timer, config_file):
    """
    CLI Entrypoint
    """
    config = get_config(config_file)
    config.update(locals())
    for name in managers.keys():
        managers[name](config)
