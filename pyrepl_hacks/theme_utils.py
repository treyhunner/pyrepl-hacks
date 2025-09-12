from _colorize import ANSIColors


def _convert_color(color):
    """Convert strings like 'reset, intense blue' into valid color."""
    subcolors = color.split(",")
    return "".join(
        getattr(ANSIColors, c.strip().replace(" ", "_").upper()) for c in subcolors
    )


def update_theme(**kwargs):
    from _colorize import Syntax, default_theme, set_theme

    items = {name: _convert_color(color) for name, color in kwargs.items()}
    new_theme = default_theme.copy_with(syntax=Syntax(**items))
    set_theme(new_theme)
