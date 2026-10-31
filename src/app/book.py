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


