import logging
from _pyrepl.simple_interact import _get_reader
from collections.abc import Callable

from .command_utils import register_command
from .key_utils import slugify, to_keyspec

__all__ = ["bind", "bind_to_insert"]


logger = logging.getLogger(__name__)


def _bind_decorator(keybinding: str, with_event: bool):
    def decorator(command_function: Callable):
        command = register_command(command_function, with_event=with_event)
        return _bind_existing_command(keybinding, command.name)

    return decorator


def _bind_existing_command(keybinding: str, command_name: str = None):
    keyspec = to_keyspec(keybinding)
    logger.debug("binding: %s for %s", keyspec, command_name)
    reader = _get_reader()
    reader.bind(keyspec, command_name)


def _bind_new_command(
    keybinding: str,
    command_name: str = None,
    command_function: Callable = None,
):
    command = register_command(command_name)(command_function)
    _bind_existing_command(keybinding, command_name)
    return command


def bind(
    keybinding: str,
    command_name: str = None,
    command_function: Callable = None,
    *,
    with_event=False,
):
    if command_function is not None:
        return _bind_new_command(keybinding, command_name, command_function)
    elif command_name is not None:
        return _bind_existing_command(keybinding, command_name)
    else:
        return _bind_decorator(keybinding, with_event)


def bind_to_insert(keybinding: str, text: str):
    def command_function(reader):
        reader.insert(text)

    bind(keybinding, slugify(keybinding), command_function)
