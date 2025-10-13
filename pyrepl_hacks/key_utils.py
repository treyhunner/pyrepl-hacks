"""Utilities for converting and normalizing key bindings."""

from _pyrepl.keymap import _keynames

from ._types import CommandName, KeyBinding, KeySpec

__all__ = ["slugify", "to_keyspec"]

bindings_to_specs = {
    "ctrl": r"\C",
    "alt": r"\M",
    "pgup": r"\<page up>",
    "pgdn": r"\<page down>",
    "pageup": r"\<page up>",
    "pagedown": r"\<page down>",
}
bindings_to_specs |= {name: rf"\<{name}>" for name in _keynames.keys()}


# Cases that can't be handled by \C- or \M- notation
SPECIAL_CASES = {
    "alt+up": r"\e[1;3A",
    "alt+down": r"\e[1;3B",
    "alt+right": r"\e[1;3C",
    "alt+left": r"\e[1;3D",
    "shift+tab": r"\e[Z",
    "shift+up": r"\e[1;2A",
    "shift+down": r"\e[1;2B",
    "shift+right": r"\e[1;2C",
    "shift+left": r"\e[1;2D",
    "shift+home": r"\e[1;2H",
    "shift+end": r"\e[1;2F",
    "shift+pageup": r"\e[5;2~",
    "shift+pagedown": r"\e[6;2~",
    "shift+pgup": r"\e[5;2~",
    "shift+pgdn": r"\e[6;2~",
    "shift+insert": r"\e[2;2~",
    "shift+delete": r"\e[3;2~",
    # Add more as we discover them
}


def slugify(keybinding: KeyBinding) -> CommandName:
    """Create a unique command name slug from a key binding.

    Converts a human-readable key binding into a valid command name by
    replacing non-alphanumeric characters with underscores and adding
    a leading underscore.

    Args:
        keybinding: Human-readable key combination (e.g., "Ctrl+F")

    Returns:
        A command name suitable for registration (e.g., "_Ctrl_F"")
    """
    return "_" + "".join(c if c.isalnum() else "_" for c in keybinding)


def to_keyspec(keybinding: KeyBinding) -> KeySpec:
    r"""Convert human-readable key bindings to _pyrepl key specifications.

    Handles modifier keys (Ctrl, Alt, Shift), function keys, arrow keys,
    and some special key combinations.

    Args:
        keybinding: Human-readable key combination. Examples:
                   - With modifiers: "Ctrl+F", "Alt+Up", "Shift+Tab"
                   - Multi-key sequences: "Ctrl+X Ctrl+R"
                   - Special keys: "F1", "Home", "PageUp"

    Returns:
        REPL key specification string. Examples:
        - "Ctrl+F" -> r"\C-f"
        - "Alt+M" -> r"\M-m"
        - "Shift+Tab" -> r"\e[Z"
        - "F4" -> r"\<f4>"
        - "Ctrl+X Ctrl+R" -> r"\C-x\C-r"
    """
    normalized = keybinding.lower().strip()
    spec = ""
    for section in normalized.split():
        if section in SPECIAL_CASES:
            spec += SPECIAL_CASES[section]
        elif "shift" in section:
            # Shift key is unsupported outside of known special cases
            raise ValueError(f"Key combo {section} not yet supported")
        else:
            try:
                spec += "-".join(
                    [
                        bindings_to_specs[part] if len(part) != 1 else part
                        for part in section.split("+")
                    ],
                )
            except KeyError as error:
                raise ValueError(f"Unknown key: {error}") from None
    return spec
