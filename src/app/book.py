from __future__ import annotations

from collections.abc import Iterable
from types import MappingProxyType
from typing import Final

from app.commands.file_manipulation import (
    FILE_MANIPULATION_COMMANDS,
)
from app.commands.navigation import NAVIGATION_COMMANDS
from app.commands.system_logs import SYSTEM_LOGS_COMMANDS 
from app.models import Category, Command

ALL_COMMANDS: Final[tuple[Command, ...]] = (
    NAVIGATION_COMMANDS + FILE_MANIPULATION_COMMANDS + SYSTEM_LOGS_COMMANDS
)

class CommandBook():

    def __init__(self, commands: Iterable[Command] = ALL_COMMANDS) -> None:
        self._commands: tuple[Command, ...] = tuple(commands)
        names = [c.name.lower() for c in self._commands]
        if len(names) != len(set(names)):
            raise ValueError("Duplicate command names detected in catalog")

        self._by_name: MappingProxyType[str, Command] = MappingProxyType(
            {c.name.lower(): c for c in self._commands}
        )
        self._by_category: MappingProxyType[Category, tuple[Command, ...]] = (
            MappingProxyType(
                {
                    category: tuple(
                        c for c in self._commands if c.category == category
                    )
                    for category in Category
                }
            )
        )
