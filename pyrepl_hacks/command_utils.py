from _pyrepl.commands import Command
from _pyrepl.simple_interact import _get_reader
from collections.abc import Callable

__all__ = ["register_command"]


def under_to_kebab(name):
    """Convert under_score_case to kebab-case."""
    return name.replace("_", "-")


def register_command(command_name: str = None, /, *, with_event: bool = False):
    def decorator(command_function: Callable):
        name = command_name or under_to_kebab(command_function.__name__)

        def do(self):
            if with_event:
                return command_function(self.reader, self.event_name, self.event)
            else:
                return command_function(self.reader)

        command_class = type(
            name,
            (Command,),
            {"do": do},
        )
        reader = _get_reader()
        reader.commands[name] = command_class
        command_function.command_class = command_class
        command_function.name = name
        return command_function

    if isinstance(command_name, Callable):
        command_function = command_name
        command_name = None
        return decorator(command_function)
    else:
        return decorator
