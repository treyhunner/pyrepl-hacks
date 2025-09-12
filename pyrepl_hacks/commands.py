import re
import textwrap

from .command_utils import register_command


# _pyrepl.commands are also included later (see _add_pyrepl_commands)
__all__ = ["move_to_indentation", "dedent", "move_line_down", "move_line_up"]


@register_command
def move_to_indentation(reader):
    """Move to the start of indentation for the current line."""
    x, y = reader.pos2xy()
    lines = reader.get_unicode().splitlines(keepends=True)
    line = lines[y]
    if match := re.search(r"^\s+", line):
        index = match.end()
    else:
        index = 0
    reader.pos = reader.bol() + index


@register_command
def dedent(reader):
    """Dedent the current code block."""
    x, y = reader.pos2xy()
    original_text = reader.get_unicode()
    dedented_text = textwrap.dedent(original_text)

    # Dedent buffer and invalidate cache
    reader.buffer[:] = list(dedented_text)
    reader.last_refresh_cache.invalidated = True
    reader.dirty = True

    # Reposition cursor correctly
    original_lines = original_text.splitlines()
    dedented_lines = dedented_text.splitlines()
    removed_characters = sum(
        len(old) - len(new)
        for old, new in zip(original_lines[:y+1], dedented_lines)
    )
    reader.pos -= removed_characters


@register_command
def move_line_down(reader):
    """Move the current line down."""
    x, y = reader.pos2xy()
    lines = reader.get_unicode().splitlines(keepends=True)

    # Can't move down if we're on the last line
    if y >= len(lines) - 1:
        return

    # Swap current line with next line
    lines[y], lines[y+1] = lines[y+1], lines[y]

    if not lines[y].endswith("\n"):
        lines[y] += "\n"

    # Update buffer with swapped lines
    reader.buffer[:] = list("".join(lines))
    reader.last_refresh_cache.invalidated = True
    reader.dirty = True

    # Move cursor to same column in the moved line (one line up)
    reader.pos += len(lines[y])


@register_command
def move_line_up(reader):
    """Move the current line up."""
    x, y = reader.pos2xy()
    lines = reader.get_unicode().splitlines(keepends=True)

    # Can't move up if we're on the first line
    if y <= 0:
        return

    # Swap current line with previous line
    lines[y-1], lines[y] = lines[y], lines[y-1]

    # Update buffer with swapped lines
    reader.buffer[:] = list("".join(lines))
    reader.last_refresh_cache.invalidated = True
    reader.dirty = True

    # Move cursor to same column in the moved line (one line up)
    reader.pos -= len(lines[y])


def _add_pyrepl_commands():
    """Create simple command functions for all _pyrepl commands also."""
    import _pyrepl.commands
    from functools import wraps
    for name, value in vars(_pyrepl.commands).items():
        if (
                isinstance(value, type)
                and issubclass(value, _pyrepl.commands.Command)
                and hasattr(value, "do")
        ):
            def wrapper(command_class):
                @wraps(value, assigned=["__name__", "__doc__"], updated=[])
                def command_function(reader, event_name, event):
                    return command_class(reader, event_name, event).do()
                return command_function
            globals()[name] = wrapper(value)
            __all__.append(name)


_add_pyrepl_commands()
