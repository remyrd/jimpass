This project was **heavily** inspired by and builds on top of the ideas in [bitwarden-rofi](https://github.com/mattydebie/bitwarden-rofi). Be sure to check it out!

# Jimpass (alpha) - The unified password management interface

[![Build Status](https://travis-ci.com/remyrd/jimpass.svg?branch=master)](https://travis-ci.com/remyrd/jimpass) [![PyPI version](https://badge.fury.io/py/Jimpass.svg)](https://badge.fury.io/py/Jimpass)

[Jimsort](https://cmpwn.com/@sir/102220283470088263), but for passwords.

---
- [Jimpass (alpha) - The unified password management interface](#jimpass---the-unified-password-management-interface)
  * [Features](#features)
  * [Supported Managers](#supported-managers)
  * [Dependencies](#dependencies)
  * [Installation](#installation)
  * [Usage](#usage)
  * [Configuration](#configuration)
  * [Roadmap](#roadmap)
  * [Extending](#extending)
  * [License](#license)

---

A backend-agnostic credential launcher/manager. Powered by [Rofi](https://github.com/davatorium/rofi).

---

There is no doubt password managers make security online better and easier, yet their use involves a lot of moving, searching and clicking. This is tedious at best, and depending on the context, they'll require additional software just to do some good old copy/pasting. In my experience it's really hard to convince someone to switch from their universal 8 year old muscle-memory-typed password, over to installing 2 apps and a browser extension which require a different search and click choreography to get similar results.

The people behind [bitwarden-rofi](https://github.com/mattydebie/bitwarden-rofi) nailed it by bridging this UX gap for [*Bitwarden*](https://bitwarden.com/) users. But, what if I don't use Bitwarden, or even worse, what if I need to use **multiple** managers? That's where Jim comes into play.

## Features

- __Auto-type__: For those too busy to paste the selected password, fill-in username/passwords automatically. 

  :warning: Introducing __Danger mode__: end by typing in `<Return>` automatically :warning:

- __TOTP support__: Copy the TOTP of the selected entry to your clipboard
- __Sync__: Force the local databases to sync up with the remote backend
- __Custom keybindings__: Define your own keybindings for different actions supported at runtime
- __Custom item display__: Choose how and what is displayed in Rofi for each password manager using `{}`. Eg. `"Work(lastpass): {name} -- {username} ({email})"`
- __Lock timeout(bitwarden only)__: Set a timer before having to re-enter your Master Password. Can be disabled.
- __Clipboard timeout__: Set a timeout after which the keyboard is cleared

## Supported Managers

- [Bitwarden](https://bitwarden.com/)
- [LastPass](https://www.lastpass.com/)

The architecture allows anyone to extend Jim to use their password manager, provided there's a CLI for it.
See the [currently implemented ones](jimpass/managers)

## Dependencies

- [python3.6+](https://www.python.org/)
- [rofi](https://github.com/davatorium/rofi)
- [xdotool](https://www.semicomplete.com/projects/xdotool/)
- `xclip` / `wl-copy` / `xsel`

Jim communicates with each password manager through specific CLIs.
Only install and configure those you use.
- [Bitwarden](https://github.com/bitwarden/cli)
- [LastPass](https://github.com/lastpass/lastpass-cli)


## Installation

Using pip:

```bash
pip install Jimpass
```

Locally:

```bash
git clone https://github.com/remyrd/jimpass
cd jimpass
pip install .
# or
python setup.py install
```

## Usage

In order to use Jimpass efficiently, bind the `jp` or `jimpass` command to a key combination of your choice.
The command comes with these options, which will override their counterpart in the [configuration](#configuration)

```
Usage: <jp|jimpass> [OPTIONS]

  CLI Entrypoint

Options:
  -c, --config FILENAME           Path to the config file. Defaults to
                                  $HOME/.jimpass.yaml or
                                  $XDG_CONFIG_HOME/jimpass/config.yaml
  --auto-lock                     Incompatible with --no-auto-lock
  --no-auto-lock                  Incompatible with --auto-lock
  --lock-timer INTEGER RANGE      Lock the database after RANGE seconds,
                                  ignored if --no-auto-lock
  --clipboard-timeout INTEGER RANGE
                                  RANGE seconds before clearing up the
                                  clipboard after copying
  --copy-command [xclip|xset|wayland]
                                  Utility to use when copying
  --danger-mode                   Automatically press Return after auto-type
  --help                          Show this message and exit.

```


## Configuration

Jimpass requires at least a minimal configuration. This is due to the fact it wishes to load only the backend modules it needs.
Configuration files can be specified through the CLI, or by placing them under `$HOME/.jimpass.yaml` or `$XDG_CONFIG_HOME/jimpass/config.yaml`

### Minimal for Bitwarden users

```yaml
managers:
  - bitwarden
bitwarden:
  template_str: 'bw: {name}: user {username}'
```

### Minimal for Lastpass users

```yaml
managers:
  - lastpass
lastpass:
  username: 'example@mail.box'
  template_str: 'lp: {name}: {username} at {url}'
```

### Complete with defaults

```yaml
managers: # REQUIRED. List all password managers to be loaded
  - bitwarden
  - lastpass
auto_lock: True
lock_timer: 500 # Ignored if auto_lock: False
clipboard_timeout: 5
copy_command: xclip # Command to use when copying [xclip|xsel|wayland]
danger_mode: False # After auto-typing a password, immediately presses Return
keybindings:
  # pressing Return copies the password under the selected entry.
  type_all: 'alt+1'
  type_user: 'alt+2'
  type_pass: 'alt+3'
  copy_totp: 'alt+t'
  sync: 'alt+r'
bitwarden:
  template_str: 'bw: {name}: user {username}'
  # available templated params include:
  # - id
  # - name
  # - username
lastpass:
  username: 'example@mail.box'
  template_str: 'lp: {name}: {username} at {url}'
  # available templated params include:
  # - id
  # - fullname
  # - name
  # - username
  # - url
  # - group
  # - note
  # - last_modified
  # - last_touch
```

## Roadmap

- [x] **Customizable keybindings** --- For actions such as `copy_username`, `type_password`, etc
- [x] **Templated item display** --- Choose how *Rofi* displays items. Eg `"Bitwarden: {name} {username}"`
- [x] **Better testing and CI**
- [ ] **Context based management** --- Manage more credential aspects.
- [ ] **Encrypted in-memory storage** -- Will allow to add other features such as caching of frequently and last used for even faster launches.


## Extending

Instructions on how to integrate your own password manager coming soon... 
In the meantime you can get inspired by the [current implementations](jimpass/managers)

## License

Released under the GNU General Public License, version 3. See `LICENSE` file.
