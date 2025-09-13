from ._types import CommandName, KeyBinding, KeySpec

__all__ = ["slugify", "to_keyspec"]

bindings_to_specs = {
    "ctrl": r"\C",
    "alt": r"\M",
    "pgup": r"\<page up>",
    "pgdn": r"\<page down>",
}


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
    """Create unique slug for keybinding."""
    return "_" + "".join(c if c.isalnum() else "_" for c in keybinding)


def to_keyspec(keybinding: KeyBinding) -> KeySpec:
    r"""Convert human-readable bindings to specs (e.g. Ctrl+A to \C-a)."""
    normalized = keybinding.lower().strip()
    if normalized in SPECIAL_CASES:
        return SPECIAL_CASES[normalized]
    spec = ""
    for section in normalized.split():
        spec += "-".join(
            [
                bindings_to_specs.get(part, rf"\<{part}>") if len(part) != 1 else part
                for part in section.split("+")
            ],
        )
    return spec
