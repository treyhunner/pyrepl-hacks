"""Hacky extensions and helper functions for the new Python REPL.

This package provides utilities to enhance the Python REPL experience by adding:
- Custom key bindings for common operations
- Command registration system for creating new REPL commands
- Utility functions for key mapping and theme customization
- Pre-built commands for text manipulation and navigation

Main functions:
    bind: Bind keys to commands or create command decorators
    bind_to_insert: Bind keys to insert specific text
    register_command: Register new commands for the REPL
    update_theme: Customize REPL syntax highlighting colors
"""

from . import commands
from .bind_utils import bind, bind_to_insert
from .command_utils import register_command
from .theme_utils import update_theme

__all__ = ["commands", "bind", "bind_to_insert", "register_command", "update_theme"]
