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

    def get_all(self) -> tuple[Command, ...]:
        return self._commands

    def get_by_name(self, name: str) -> Command | None:
        return self._by_name.get(name.strip().lower())

    def get_by_category(self, category: Category) -> tuple[Command, ...]:
        return self._by_category.get(category, ())

    def search(self, query: str) -> tuple[Command, ...]:
        q = query.strip().lower()
        if not q:
            return self._commands
        return tuple(
            cmd
            for cmd in self._commands
            if q in cmd.name.lower()
            or q in cmd.summary.lower()
            or q in cmd.description.lower()
        )

    def __iter__(self):
        return iter(self._commands)

    def __len__(self) -> int:
        return len(self._commands)

    def __contains__(self, name: str) -> bool:
        return name.strip().lower() in self._by_name