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
