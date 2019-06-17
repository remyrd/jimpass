This project was **heavily** inspired by and builds on top of the ideas in [bitwarden-rofi](https://github.com/mattydebie/bitwarden-rofi). Be sure to check it out!

# Jimpass (alpha) - The unified password management interface

```c
  jimpass() {
    system("/usr/bin/sendmail","jim@business.company", "Jim, get the password typed by 3PM", attachment=logins)
  }
```

---
- [Jimpass (alpha) - The unified password management interface](#jimpass---the-unified-password-management-interface)
  * [Supported Managers](#supported-managers)
  * [Roadmap](#roadmap)
  * [Dependencies](#dependencies)
  * [Installation](#installation)
  * [Usage](#usage)
  * [Configuration](#configuration)
  * [License](#license)

---

Autotype, copy, and ~~manage~~(soon) your credentials from multiple providers through a single [launcher](https://github.com/davatorium/rofi).

---

There is no doubt password managers make security online better and easier, yet their use involves a lot of moving, searching and clicking. This is tedious at best, and depending on the context, they'll require additional software just to do some good old copy/pasting. In my experience it's really hard to convince someone to switch from their universal 8 year old muscle-memory-typed password, over to installing 2 apps and a browser extension which require a different search and click choreography to get similar results.

The people behind [bitwarden-rofi](https://github.com/mattydebie/bitwarden-rofi) nailed it by bridging this UX gap for [*Bitwarden*](https://bitwarden.com/) users. But, what if I don't use Bitwarden, or even worse, what if I need to use **multiple** managers? That's where Jim comes into play.

## Supported Managers
- [Bitwarden](https://bitwarden.com/)
- [LastPass](https://www.lastpass.com/)

## Roadmap

- [x] **Customizable keybindings** --- For actions such as `copy_username`, `type_password`, etc
- [x] **Templated item display** --- Choose how *Rofi* displays items. Eg `"Bitwarden: {name} {username}"`
- [ ] **Context based management** --- Manage your managers from rofi itself
- [ ] **Encrypted in-memory storage** -- Duh...


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

For now, you'll have to install locally using pip or setup.py

```bash
git clone https://github.com/remyrd/jimpass
cd jimpass
pip install .
# or
python setup.py install
```

## Usage
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

## License

Released under the GNU General Public License, version 3. See `LICENSE` file.
