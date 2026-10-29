"""Shell Manager - An interactive Linux terminal assistant for beginners."""

__version__ = "1.0.0"
__author__ = "Tyrant_Delet"

from shell_manager.config import CONFIG, AppConfig
from shell_manager.models import Category, Command, CommandExample, Flag, SafetyLevel

__all__ = [
    "AppConfig",
    "CONFIG",
    "Category",
    "Command",
    "CommandExample",
    "Flag",
    "SafetyLevel",
    "__version__",
]
