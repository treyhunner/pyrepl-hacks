# pyrepl-hacks 🙀

Hacky extensions and helper functions for the new Python REPL.

```python
import pyrepl_hacks as repl

repl.bind("Alt+M", "move-to-indentation")   # Move to first non-space in current line
repl.bind("Shift+Tab", "dedent")            # Dedent the whole input
repl.bind("Alt+Down", "move-line-down")     # Swap current line with next in block
repl.bind("Alt+Up", "move-line-up")         # Swap current line with previous in block
repl.bind("Shift+Home", "home")             # Move to first character in the input
repl.bind("Shift+End", "end")               # Move to last character in the input

# Make Ctrl+N insert a specific list of numbers
repl.bind_to_insert("Ctrl+N", "[2, 1, 3, 4, 7, 11, 18, 29]")


@repl.bind(r"Ctrl+X Ctrl+R", with_event=True)
def subprocess_run(reader, event_name, event):
    """Ctrl+X followed by Ctrl+R will insert a subprocess.run command."""
    reader.insert("import subprocess\n")
    code = 'subprocess.run("", shell=True)'
    reader.insert(code)
    for _ in range(len(code) - code.index('""') - 1):
        repl.commands.left(reader, event_name, event)
```


## ⚠️ WARNING: here be dragons 🐉

This library relies on Python implementation details which may change in future Python versions.

This library uses the `_pyrepl` module (and optionally `_colorize`).
As the `_` prefix implies, these modules are not designed for public use.

That means that when you upgrade to a newer Python (for example Python 3.15) this code may break.
For that reason, the Python versions this package claims to work with are pinned to only known-to-be-working Python versions.


## Installing 💾

To install globally:

```console
pip install pyrepl-hacks
```

Then you can use it in [your `PYTHONSTARTUP` file][PYTHONSTARTUP]:

```python
def _main():
    try:
        import pyrepl_hacks as repl
    except ImportError:
        pass  # We must be on Python 3.12 or earlier
    else:
        repl.bind("Alt+M", "move-to-indentation")
        repl.bind("Shift+Tab", "dedent")
        repl.bind("Alt+Down", "move-line-down")
        repl.bind("Alt+Up", "move-line-up")
        repl.bind("Shift+Home", "home")
        repl.bind("Shift+End", "end")

        repl.bind_to_insert("Ctrl+N", "[2, 1, 3, 4, 7, 11, 18, 29]")

_main()
del _main  # Don't pollute the global namespace in our REPL
```

Note that this will only modify the REPL in environments where `pyrepl-hacks` is installed.
So if you want it everywhere, you would need to install `pyrepl-hacks` system-wide *and* in every virtual environment.

If you just want to play with this tool, try this:

```console
uvx --with pyrepl-hacks python
```


## Command Registering and Key Binding ⌨️

This library includes features for easily registering and binding new REPL commands.

### Binding to existing commands

You can bind a key to an existing command:

```python
import pyrepl_hacks as repl

repl.bind("Shift+Home", "home")
```

### Inserting text with a binding

You can use the `bind_to_insert` helper to bind a key to insert specific text:

```python
import pyrepl_hacks as repl

repl.bind_to_insert("Ctrl+P", "Python?!")
```

### Registering new commands

Need something fancy that doesn't exist yet?

You can register a new command:

```python
import pyrepl_hacks as repl

@repl.register_command
def exit(reader):
    """Exits Python immediately."""
    import sys
    sys.exit(0)
```

The `register_command` decorator will turn the `under_score` separated name into a `kebab-case` name by default.

The `register_command` can optionally accept a command name and, if the command needs access to the event name and event object, a `with_event=True` argument can be provided:

```python
import pyrepl_hacks as repl

@repl.register_command("delete-line", with_event=True)
def delete_whole_line(reader, event_name, event):
    """Move to beginning of line and delete all text."""
    reader.pos = reader.bol()
    repl.commands.kill_line(reader, event_name, event)
```

After commands have been registered, they can be used with the `bind` function to bind them to specific keys:

```python
import pyrepl_hacks as repl

repl.bind("F4", "exit")
repl.bind("Ctrl+X Ctrl+D", "delete-line")
```

### Binding keys while registering

The `bind` function can also be used as a decorator to register a command and bind it to a specific key combination at the same time:

```python
import pyrepl_hacks as repl

@repl.bind("F4")
def exit(reader):
    """Exits Python immediately."""
    import sys
    sys.exit(0)
```

Since there's not much point in making a new command *without* binding it, you'll usually want to use `bind` instead of `register_command`.

Just like `register_command`, `bind` decorator can also accept a `with_event=True` argument to pass the event name and event object into the command function.


## Available Commands 📑

Here are some of the interesting commands provided by Python (in `_pyrepl.commands`):

- `clear-screen`: Clear screen (`Ctrl+L`)
- `accept`: Run current code block (`Alt+Enter`)
- `beginning-of-line`: Move cursor to the first character of the current line (`Ctrl+A` or `Home`)
- `end-of-line`: Move cursor to the last character of the current line (`Ctrl+E` or `End`)
- `home`: Move cursor the first character in the code block
- `end`: Move cursor the last character in the code block
- `kill-line`: Delete to end of line (`Ctrl+K`)
- `unix-line-discard`: Delete to beginning of line (`Ctrl+U`)
- `backward-word`: Move cursor back one word (`Ctrl+Left`)
- `forward-word`: Move cursor forward one word (`Ctrl+Right`)
- `backward-kill-word`:  Delete to beginning of word (`Alt+Backspace`)
- `kill-word`:  Delete to end of word (`Alt+D`)

[See here for which keyboard shortcuts these are bound to by default](https://www.pythonmorsels.com/repl-features/#keyboard-shortcuts).

This `pyrepl-hacks` project provides some additional commands as well:

- `move-to-indentation`: Move to first non-space in current line
- `dedent`: Dedent the whole code block
- `move-line-down`: Swap current line with next one in the block
- `move-line-up`: Swap current line with previous one in the block

These 4 additional commands have no key bindings by default.

I recommend binding these commands as well as the `home` and `end` commands (provided by `_pyrepl.commands`) which are also unbound by default:

```python
repl.bind("Alt+M", "move-to-indentation")   # Move to first non-space in current line
repl.bind("Shift+Tab", "dedent")            # Dedent the whole input
repl.bind("Alt+Down", "move-line-down")     # Swap current line with next in block
repl.bind("Alt+Up", "move-line-up")         # Swap current line with previous in block
repl.bind("Shift+Home", "home")             # Move to first character in the input
repl.bind("Shift+End", "end")               # Move to last character in the input
```

Note that these custom REPL commands and all existing commands provided by `_pyrepl.commands` include wrapper functions in the `commands` submodule.
These functions are named the same as their command name, except `-` must be replaced by `_`:

```python
from pyrepl_hacks.commands import move_to_indentation, clear_screen
```


## Customizing Your Syntax Theme 🎨

Python 3.14 includes syntax highlighting in the REPL.

You can use the `update_theme` command from pyrepl-hacks to customize the colors your REPL uses:

```python
try:
    import pyrepl_hacks as repl

    repl.update_theme(
        keyword="green",
        builtin="blue",
        comment="intense blue",
        string="cyan",
        number="cyan",
        definition="blue",
        soft_keyword="bold green",
        op="intense green",
        reset="reset, intense green",
    )
except ImportError:
    pass  # We're on Python 3.13 or below
```

These are the supported colors:

- `black`
- `blue`
- `cyan`
- `green`
- `grey`
- `magenta`
- `red`
- `white`
- `yellow`

Each supports the modifiers `bold`, `intense`, `background` and `intense background`.

Also the "color" of `reset` will reset all modifiers.


## The Future is Obsolescence? 🦤

This project came out of the things I learned while [hacking on my own REPL shortcuts](https://treyhunner.com/2024/10/adding-keyboard-shortcuts-to-the-python-repl/) and [customizing my REPL's syntax highlighting](https://treyhunner.com/2025/09/customizing-your-python-repl-color-scheme/).

My hope is that this package will be obsolete one day.

I hope that Python will eventually include an official interface for creating new REPL commands and binding keys to commands.

I also hope that some (or all?) of the 4 new commands this module includes will eventually be included with Python by default.


[PYTHONSTARTUP]: https://nedbatchelder.com/blog/201001/running_code_at_python_startup.html
