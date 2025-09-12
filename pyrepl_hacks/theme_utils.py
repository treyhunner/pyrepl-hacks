def _convert_color(color):
    """Convert strings like 'reset, intense blue' into valid color."""
    subcolors = color.split(",")
    return "".join(
        getattr(ANSIColors, c.strip().replace(" ", "_").upper())
        for c in subcolors
    )


def update_theme(**kwargs):
    from _colorize import set_theme, default_theme, Syntax, ANSIColors
    items = {
        name: _convert_color(color)
        for name, color in kwargs.items()
    }
    new_theme = default_theme.copy_with(syntax=Syntax(**items))
    set_theme(new_theme)
