"""Utilities for binding keys to commands in the REPL.

Provides functions for creating key bindings that trigger commands in
the Python REPL, including registering new commands, binding to
existing commands, and creating decorator-based bindings.
"""

from __future__ import annotations

import logging
from _pyrepl.simple_interact import _get_reader

from ._types import (
    CommandDecorator,
    CommandFunction,
    CommandHandler,
    CommandName,
    HistoricalReader,
    KeyBinding,
)
from .command_utils import register_command
from .key_utils import slugify, to_keyspec

__all__ = ["bind", "bind_to_insert"]


logger = logging.getLogger(__name__)


def _bind_decorator(
    keybinding: KeyBinding,
    with_event: bool,
) -> CommandDecorator:
    """Create a decorator that binds the decorated function to a key.

    Args:
        keybinding: Human-readable key combination (e.g., "Ctrl+A")
        with_event: Whether the command function expects event parameters

    Returns:
        A decorator function that registers and binds command functions
    """

    def decorator(command_function: CommandHandler) -> CommandFunction:
        command = register_command(command_function, with_event=with_event)
        _bind_existing_command(keybinding, command.name)
        return command

    return decorator


def _bind_existing_command(keybinding: KeyBinding, command_name: CommandName) -> None:
    """Bind a key combination to an existing command by name.

    Args:
        keybinding: Human-readable key combination (e.g., "Ctrl+A")
        command_name: Name of existing command to bind to
    """
    keyspec = to_keyspec(keybinding)
    logger.debug("binding: %s for %s", keyspec, command_name)
    reader = _get_reader()
    reader.bind(keyspec, command_name)


def _bind_new_command(
    keybinding: KeyBinding,
    command_name: CommandName,
    command_function: CommandHandler,
) -> CommandFunction:
    """Register a new command and bind it to a key combination.

    Args:
        keybinding: Human-readable key combination (e.g., "Ctrl+A")
        command_name: Name to register the command under
        command_function: Function to execute when key is pressed

    Returns:
        The registered command function with added metadata
    """
    command = register_command(command_name)(command_function)
    _bind_existing_command(keybinding, command_name)
    return command


def bind(
    keybinding: KeyBinding,
    command_name: CommandName | None = None,
    command_function: CommandHandler | None = None,
    *,
    with_event: bool = False,
) -> CommandDecorator | None:
    """Bind a key combination to a command or create a command decorator.

    This function has multiple usage patterns:

    1. Bind to existing command:
        bind("Ctrl+A", "beginning-of-line")

    2. Register and bind new command:
        import sys
        bind("F4", "my-command", lambda reader: reader.insert("F4 pressed"))

    3. Use as decorator:
        @bind("F4")
        def my_command(reader):
            reader.insert("F4 pressed")

    4. Use as decorator with custom name:
        @bind("F4", "my-command")
        def f4_pressed_command(reader):
            reader.insert("F4 pressed")

    Args:
        keybinding: Human-readable key combination (e.g., "Ctrl+A", "Alt+Up")
        command_name: Name of existing command or name for new command
        command_function: Function to execute when key is pressed
        with_event: set to True if function expects (reader, event_name, event)
                    instead of just (reader). Only used with decorator pattern.

    Returns:
        None when binding to existing commands or registering new ones.
        CommandDecorator when used as a decorator (no arguments besides keybinding).
    """
    if command_function is not None:
        assert command_name is not None
        _bind_new_command(keybinding, command_name, command_function)
        return None
    elif command_name is not None:
        _bind_existing_command(keybinding, command_name)
        return None
    else:
        return _bind_decorator(keybinding, with_event)


def bind_to_insert(keybinding: KeyBinding, text: str) -> None:
    """Bind a key combination to insert specific text at the cursor.

    This is a convenience function for creating simple text insertion bindings.
    The command name is automatically generated from the key binding.

    Args:
        keybinding: Human-readable key combination (e.g., "Ctrl+P")
        text: Text to insert when the key is pressed
    """

    def command_function(
        reader: HistoricalReader,
        event_name: str = "",
        event: str = "",
    ) -> None:
        reader.insert(text)

    bind(keybinding, slugify(keybinding), command_function)
