"""Shell Manager - An interactive Linux terminal assistant for beginners."""

__version__ = "1.0.0"
__author__ = "Tyrant_Delet"

from app.commands import (
    get_all_commands,
    get_command_by_name,
    get_commands_by_category,
    search_commands,
)

from app.config import CONFIG, AppConfig
from app.models import Category, Command, CommandExample, Flag, SafetyLevel

__all__ = [
    "AppConfig",
    "CONFIG",
    "Category",
    "Command",
    "CommandExample",
    "Flag",
    "SafetyLevel",
    "__version__",
    "get_all_commands",
    "get_command_by_name",
    "get_commands_by_category",
    "search_commands",
]
