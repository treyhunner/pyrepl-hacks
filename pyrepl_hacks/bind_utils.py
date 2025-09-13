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
    def decorator(command_function: CommandHandler) -> CommandFunction:
        command = register_command(command_function, with_event=with_event)
        _bind_existing_command(keybinding, command.name)
        return command

    return decorator


def _bind_existing_command(keybinding: KeyBinding, command_name: CommandName) -> None:
    keyspec = to_keyspec(keybinding)
    logger.debug("binding: %s for %s", keyspec, command_name)
    reader = _get_reader()
    reader.bind(keyspec, command_name)


def _bind_new_command(
    keybinding: KeyBinding,
    command_name: CommandName,
    command_function: CommandHandler,
) -> CommandFunction:
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
    def command_function(
        reader: HistoricalReader,
        event_name: str = "",
        event: str = "",
    ) -> None:
        reader.insert(text)

    bind(keybinding, slugify(keybinding), command_function)
