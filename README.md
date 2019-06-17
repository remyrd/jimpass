This project was **heavily** inspired by and builds on top of the ideas in [bitwarden-rofi](https://github.com/mattydebie/bitwarden-rofi). Be sure to check it out!

# Jimpass - The unified password management interface

```c
  jimpass() {
    system("/usr/bin/sendmail","jim@business.company", "Jim, get the password by 3PM", attachments=export.csv)
  }
```

Autotype, copy, and ~~manage~~(soon) your credentials from multiple providers through a single [launcher](https://github.com/davatorium/rofi).


There is no doubt password managers make security online better and easier, yet their use involves a lot of moving, searching and clicking. This is tedious at best, and depending on the context, they'll require additional software just to do some good old copy/pasting. In my experience it's really hard to convince someone to switch from their universal 8 year old muscle-memory-typed password, over to installing 2 apps and a browser extension which require a different search and click choreography to get similar results.

The people behind [bitwarden-rofi](https://github.com/mattydebie/bitwarden-rofi) nailed it by bridging this UX gap for [*Bitwarden*](https://bitwarden.com/) users. But, what if I don't use Bitwarden, or even worse, what if I need to use **multiple** managers? That's where Jim comes into play.

### Supported Managers
- [Bitwarden](https://bitwarden.com/)
- [LastPass](https://www.lastpass.com/)

### Roadmap:

- [x] **Customizable keybindings** --- For actions such as `copy_username`, `type_password`, etc
- [x] **Templated item display** --- Choose how *Rofi* displays items. Eg `"Bitwarden: {name} {username}"`
- [ ] **Context based management** --- Manage your managers from rofi itself
- [ ] **Encrypted in-memory storage** -- Duh...


### Dependencies

- [rofi](https://github.com/davatorium/rofi)
- [xdotool](https://www.semicomplete.com/projects/xdotool/)
- `xclip` / `wl-copy` / `xsel`

Jim communicates with each password manager through specific CLIs.
Only install and configure those you use.
- [Bitwarden](https://github.com/bitwarden/cli)
- [LastPass](https://github.com/lastpass/lastpass-cli)

### Usage:
```

```

### Configuration
