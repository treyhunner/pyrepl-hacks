import re
import textwrap
from typing import cast

from ._types import Command, CommandFunction, HistoricalReader
from .command_utils import register_command

# _pyrepl.commands are also included later (see _add_pyrepl_commands)
__all__ = [
    "move_to_indentation",
    "dedent",
    "move_line_down",
    "move_line_up",
    "previous_paragraph",
    "next_paragraph",
]


@register_command  # type: ignore[call-overload]
def move_to_indentation(reader: HistoricalReader) -> None:
    """Move to the start of indentation for the current line."""
    x, y = reader.pos2xy()
    lines = reader.get_unicode().splitlines(keepends=True)
    line = lines[y]
    index = match.end() if (match := re.search(r"^[ \t]+", line)) else 0
    reader.pos = reader.bol() + index


@register_command  # type: ignore[call-overload]
def dedent(reader: HistoricalReader) -> None:
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
        for old, new in zip(original_lines[: y + 1], dedented_lines, strict=False)
    )
    reader.pos -= removed_characters


@register_command  # type: ignore[call-overload]
def move_line_down(reader: HistoricalReader) -> None:
    """Move the current line down."""
    x, y = reader.pos2xy()
    lines = reader.get_unicode().splitlines(keepends=True)

    # Can't move down if we're on the last line
    if y >= len(lines) - 1:
        return

    # Swap current line with next line
    lines[y], lines[y + 1] = lines[y + 1], lines[y]

    if not lines[y].endswith("\n"):
        lines[y] += "\n"

    # Update buffer with swapped lines
    reader.buffer[:] = list("".join(lines))
    reader.last_refresh_cache.invalidated = True
    reader.dirty = True

    # Move cursor to same column in the moved line (one line up)
    reader.pos += len(lines[y])


@register_command  # type: ignore[call-overload]
def move_line_up(reader: HistoricalReader) -> None:
    """Move the current line up."""
    x, y = reader.pos2xy()
    lines = reader.get_unicode().splitlines(keepends=True)

    # Can't move up if we're on the first line
    if y <= 0:
        return

    # Swap current line with previous line
    lines[y - 1], lines[y] = lines[y], lines[y - 1]

    # Update buffer with swapped lines
    reader.buffer[:] = list("".join(lines))
    reader.last_refresh_cache.invalidated = True
    reader.dirty = True

    # Move cursor to same column in the moved line (one line up)
    reader.pos -= len(lines[y])


@register_command  # type: ignore[call-overload]
def previous_paragraph(reader: HistoricalReader) -> None:
    """Move cursor to the blank line before the current paragraph (like Vim { or Emacs M-{)."""
    x, y = reader.pos2xy()
    lines = reader.get_unicode().splitlines(keepends=True)

    # If we're already on the first line, can't go further
    if y == 0:
        reader.pos = 0
        reader.error("start of buffer")
        return

    search_y = y - 1

    # If we're on a blank line, skip backward past consecutive blank lines
    if lines[y].strip() == "":
        while search_y >= 0 and lines[search_y].strip() == "":
            search_y -= 1

    # Skip backward through non-blank lines (current paragraph)
    while search_y >= 0 and lines[search_y].strip() != "":
        search_y -= 1

    # search_y now points to a blank line before current paragraph (or -1)
    # Skip backward to find the FIRST blank line in this sequence
    while search_y > 0 and lines[search_y - 1].strip() == "":
        search_y -= 1

    # Position at the beginning of the first blank line
    if search_y < 0:
        reader.pos = 0
    else:
        reader.pos = sum(len(line) for line in lines[:search_y])


@register_command  # type: ignore[call-overload]
def next_paragraph(reader: HistoricalReader) -> None:
    """Move cursor to the blank line after the current paragraph (like Vim } or Emacs M-})."""
    x, y = reader.pos2xy()
    lines = reader.get_unicode().splitlines(keepends=True)

    # If we're already on the last line, can't go further
    if y >= len(lines) - 1:
        reader.pos = len(reader.buffer)
        reader.error("end of buffer")
        return

    search_y = y + 1

    # If we're on a blank line, skip forward past consecutive blank lines
    if lines[y].strip() == "":
        while search_y < len(lines) and lines[search_y].strip() == "":
            search_y += 1

    # Skip forward through non-blank lines (current paragraph)
    while search_y < len(lines) and lines[search_y].strip() != "":
        search_y += 1

    # search_y now points to the blank line after current paragraph (or past end)
    if search_y >= len(lines):
        reader.pos = len(reader.buffer)
    else:
        # Position at the beginning of this blank line
        reader.pos = sum(len(line) for line in lines[:search_y])


def _add_pyrepl_commands() -> None:
    """Create simple command functions for all _pyrepl commands also."""
    import _pyrepl.commands
    from functools import wraps

    for name, value in vars(_pyrepl.commands).items():
        if (
            isinstance(value, type)
            and issubclass(value, _pyrepl.commands.Command)
            and hasattr(value, "do")
        ):

            def wrapper(command_class: type[Command]) -> CommandFunction:
                @wraps(command_class, assigned=["__name__", "__doc__"], updated=[])
                def command_function(
                    reader: HistoricalReader,
                    event_name: str,
                    event: str,
                ) -> None:
                    command_class(reader, event_name, event).do()

                func = cast(CommandFunction, command_function)
                func.command_class = command_class
                func.name = command_class.__name__
                return func

            globals()[name] = wrapper(value)
            __all__.append(name)


_add_pyrepl_commands()
