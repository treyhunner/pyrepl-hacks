"""Utilities to modify _pyrepl syntax highlighting themes."""

from _colorize import ANSIColors


def _convert_color(color: str) -> str:
    """Convert color specification strings into ANSI color codes.

    Args:
        color: Color specification like 'red', 'intense blue', 'reset, bold'

    Returns:
        Combined ANSI color escape sequence

    Examples:
        >>> _convert_color('red')
        '\\x1b[31m'
        >>> _convert_color('intense blue')
        '\\x1b[94m'
        >>> _convert_color('red, bold')
        '\\x1b[31m\\x1b[1m'
    """
    subcolors = color.split(",")
    return "".join(
        getattr(ANSIColors, c.strip().replace(" ", "_").upper()) for c in subcolors
    )


def update_theme(**kwargs: str) -> None:
    """Update the Python REPL syntax highlighting theme.

    Available token types include:
        - prompt: REPL prompt
        - keyword: Python keywords (def, if, for, etc.)
        - keyword_constant: keyword constant (None, True, False)
        - builtin: Built-in functions
        - comment: Comments
        - string: String literals
        - number: Numeric literals
        - op: Operators (+, -, etc.)
        - definition: Name of function or class as it's defined
        - soft_keyword: Python keywords (match, case, type)
        - reset: The default style

    Color specifications can be:
        - Basic colors: 'black', 'blue', cyan', 'green', 'grey', 'magenta', 'red', 'white', 'yellow'
        - Bold colors: 'bold black', 'bold blue', 'bold cyan', etc.
        - Intense colors: 'intense black', 'intense blue', etc.
        - Background colors: 'background black', 'background blue', etc.
        - Intense background colors: 'intense background black', 'intense background blue', etc.
        - Combinations: 'background black, bold magenta'
        - Reset: 'reset' to clear formatting

    Args:
        **kwargs: Token type names mapped to color specifications

    Examples:
        >>> update_theme(string='red', number='blue')
    """
    from _colorize import Syntax, default_theme, set_theme

    items = {name: _convert_color(color) for name, color in kwargs.items()}
    new_theme = default_theme.copy_with(syntax=Syntax(**items))
    set_theme(new_theme)
