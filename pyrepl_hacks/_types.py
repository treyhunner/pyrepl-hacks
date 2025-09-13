"""Type definitions for pyrepl_hacks."""

from __future__ import annotations

from _pyrepl.commands import Command
from _pyrepl.historical_reader import HistoricalReader
from collections.abc import Callable
from typing import Protocol

# Type aliases for different string meanings
type KeySpec = str  # like r"\C-c" (readline-style key specification)
type KeyBinding = str  # like "Ctrl+C" (human-readable key description)
type ColorName = str  # like "blue" (color name)
type AnsiEscape = str  # like "\x1b[34m" (ANSI escape sequence)
type CommandName = str  # like "interrupt" (command identifier)

# Common callable patterns
type CommandDecorator = Callable[
    [CommandHandler],
    CommandFunction,
]  # Decorator that transforms handlers to functions
type CommandRegistrar = Callable[
    [CommandHandler],
    CommandFunction,
]  # Command registration callable

__all__ = [
    "Command",
    "CommandHandler",
    "CommandFunction",
    "CommandDecorator",
    "CommandRegistrar",
    "HistoricalReader",
    "KeySpec",
    "KeyBinding",
    "ColorName",
    "AnsiEscape",
    "CommandName",
]


class CommandHandler(Protocol):
    """A function that can be used as a command handler.

    This protocol represents functions that:
    1. Take a HistoricalReader as the first argument
    2. Have a __name__ attribute (since they're functions)
    3. Can accept either (reader) or (reader, event_name, event) signatures
    """

    __name__: str

    def __call__(
        self,
        reader: HistoricalReader,
        event_name: str = ...,
        event: str = ...,
    ) -> None: ...


class CommandFunction(Protocol):
    """A function that has been registered as a command."""

    command_class: type[Command]
    name: str

    def __call__(self, reader: HistoricalReader) -> None: ...
