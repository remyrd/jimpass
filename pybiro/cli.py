""" Python Bitwarden Rofi """
import yaml
import click
from pybiro.controller import Controller
from pybiro.managers.bitwarden import Bitwarden
from pybiro.managers.lastpass import Lastpass
from pybiro.util import get_config
from pybiro.config import DEFAULTS

MANAGERS = {
    'bitwarden': Bitwarden,
    'lastpass': Lastpass
}


def populate_option(param_, config_key: str, config):
    """
    Priority order:
    1. user input directly from CLI
    2. configuration file
    3. DEFAULTS fallback
    :param param_:
    :param config_key:
    :param config:
    :return:
    """
    if param_:
        config[config_key] = param_
    elif config_key not in config:
        config[config_key] = DEFAULTS[config_key]


@click.command()
@click.option('-c', '--config', type=click.File('r'),
              help='Path to the config file. Defaults to $HOME/.pybiro.yaml or $XDG_CONFIG_HOME/pybiro/config.yaml')
@click.option('--auto-lock', 'lock', flag_value="lock",
              help='Incompatible with --no-auto-lock')
@click.option('--no-auto-lock', 'lock', flag_value="nolock",
              help='Incompatible with --auto-lock')
@click.option('--lock-timer', type=click.IntRange(min=0),
              help='Lock the database after RANGE seconds, ignored if --no-auto-lock')
@click.option('--clipboard-timeout', type=click.IntRange(min=0),
              help='RANGE seconds before clearing up the clipboard after copying')
@click.option('--copy-command', type=click.Choice(['xclip', 'xset', 'wayland']),
              help='Utility to use when copying')
@click.option('--danger-mode', is_flag=True, default=False,
              help='Automatically press Return after auto-type')
def cli(config, lock, lock_timer, clipboard_timeout, copy_command, danger_mode):
    """
    CLI Entrypoint
    """
    if not config:
        config = get_config()
    else:
        config = yaml.load(config)
    # auto-lock
    if lock:
        if lock == "lock":
            config['auto_lock'] = True
        else:
            config['auto_lock'] = False
    elif 'auto_lock' not in config:
        config['auto_lock'] = DEFAULTS['auto_lock']
    # lock-timer
    if config['auto_lock']:
        if lock_timer:
            config['lock_timer'] = lock_timer
        elif 'lock_timer' not in config:
            config['lock_timer'] = DEFAULTS['lock_timer']
    # clipboard
    populate_option(clipboard_timeout, 'clipboard_timeout', config)
    # copy-command
    populate_option(copy_command, 'copy_command', config)
    # danger-mode
    populate_option(danger_mode, 'danger_mode', config)
    # Run
    print(config)
    Controller(config, MANAGERS).show_items()
