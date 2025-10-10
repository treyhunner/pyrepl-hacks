"""Core utilities for registering and managing REPL commands.

This module provides the infrastructure for creating and registering custom
REPL commands. Commands are functions that can be bound to key combinations
and executed in response to user input.
"""

from __future__ import annotations

from _pyrepl.simple_interact import _get_reader
from typing import cast, overload

from ._types import (
    Command,
    CommandFunction,
    CommandHandler,
    CommandName,
    CommandRegistrar,
)

__all__ = ["register_command"]


def under_to_kebab(name: str) -> CommandName:
    """Convert under_score_case to kebab-case."""
    return name.replace("_", "-")


@overload
def register_command(
    command_name: CommandHandler,
    /,
    *,
    with_event: bool = False,
) -> CommandFunction: ...


@overload
def register_command(
    command_name: CommandName | None = None,
    /,
    *,
    with_event: bool = False,
) -> CommandRegistrar: ...


def register_command(
    command_name: CommandName | CommandHandler | None = None,
    /,
    *,
    with_event: bool = False,
) -> CommandFunction | CommandRegistrar:
    """Register a function as a REPL command.

    This decorator transforms a regular function into a REPL command that can be
    bound to key combinations. The command name is derived from the function name
    by converting underscores to hyphens (e.g., "my_command" -> "my-command").

    Usage patterns:

    1. Direct decoration (auto-generated name):
        # Creates command "my-function"
        @register_command
        def my_function(reader):
            reader.insert("Hello!")

    2. Registering a command with a custom name:
        # Creates command "custom-name"
        @register_command("custom-name")
        def my_function(reader):
            reader.insert("Hello!")

    3. Registering a command with event parameters:
        @register_command(with_event=True)
        def event_handler(reader, event_name, event):
            reader.insert(f"Event: {event_name}")

    Args:
        command_name: Name for the command, or the function to register.
                      If None, uses the function name converted to kebab-case.
        with_event: Whether the command function expects (reader, event_name, event)
                    instead of just (reader). Defaults to False.

    Returns:
        Either a CommandFunction (when used directly) or a CommandRegistrar
        decorator function (when used with parameters).
    """

    def decorator(function: CommandHandler) -> CommandFunction:
        # Extract the actual name if command_name is a function
        if callable(command_name):
            name = under_to_kebab(command_name.__name__)
        else:
            name = command_name or under_to_kebab(function.__name__)

        def do(self: Command) -> None:
            if with_event:
                return function(self.reader, self.event_name, self.event)
            else:
                return function(self.reader)

        command_class = type(
            name,
            (Command,),
            {"do": do},
        )
        reader = _get_reader()
        reader.commands[name] = command_class

        command_function = cast(CommandFunction, function)
        command_function.command_class = command_class
        command_function.name = name
        return command_function

    if callable(command_name):
        # Direct decoration: @register_command
        return decorator(command_name)
    else:
        # Parameterized decoration: @register_command("name")
        return decorator
