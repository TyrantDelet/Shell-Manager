from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class SafetyLevel(StrEnum):

    READ_ONLY = "read_only"
    MODIFICATION = "modification"
    DESTRUCTIVE = "destructive"
    SUDO_REQUIRED = "sudo_required"


    @property
    def label(self) -> str:
        return _SAFETY_LABELS[self]

    @property
    def badge(self) -> str:
        return _SAFETY_BADGES[self]


class Category(StrEnum):

    NAVIGATION = "navigation"
    FILE_MANIPULATION = "file_manipulation"
    SYSTEM_LOGS = "system_logs"

    @property
    def display_name(self) -> str:
        return _CATEGORY_NAMES[self]

    @property
    def description(self) -> str:
        return _CATEGORY_DESCRIPTIONS[self]
 

_SAFETY_LABELS: dict[SafetyLevel, str] = {
    SafetyLevel.READ_ONLY: "Read-Only (Safe)",
    SafetyLevel.MODIFICATION: "Modification (Writes Data)",
    SafetyLevel.DESTRUCTIVE: "Destructive (Data Loss Risk)",
    SafetyLevel.SUDO_REQUIRED: "Elevated / Sudo Required",
}

_SAFETY_BADGES: dict[SafetyLevel, str] = {
    SafetyLevel.READ_ONLY: "[green]● READ-ONLY[/green]",
    SafetyLevel.MODIFICATION: "[yellow]▲ MODIFICATION[/yellow]",
    SafetyLevel.DESTRUCTIVE: "[red]■ DESTRUCTIVE[/red]",
    SafetyLevel.SUDO_REQUIRED: "[magenta]⚡ SUDO REQUIRED[/blue]",
}
 
_CATEGORY_NAMES: dict[Category, str] = {
    Category.NAVIGATION: "Navigation & Directory Browsing",
    Category.FILE_MANIPULATION: "File & Directory Manipulation",
    Category.SYSTEM_LOGS: "System Logs & Process Monitoring",
}
 
_CATEGORY_DESCRIPTIONS: dict[Category, str] = {
    Category.NAVIGATION: (
        "Commands to move around, search, locate files, and inspect current location."
    ),
    Category.FILE_MANIPULATION: (
        "Commands to create, copy, move, view, edit, and delete files or folders."
    ),
    Category.SYSTEM_LOGS: (
        "Commands to view system logs, monitor processes, and check system status."
    ),
}


@dataclass(frozen=True)
class Flag:

    flag: str
    name: str
    description: str
    example: str = ""


@dataclass(frozen=True)
class CommandExample:

    command: str
    description: str


@dataclass
class Command:

    name: str
    category: Category
    safety_level: SafetyLevel
    summary: str
    description: str
    syntax: str
    default_args: str = ""
    flags: tuple[Flag, ...] = ()
    examples: tuple[CommandExample, ...] = ()
    notes: str = ""

    @property
    def is_destructive(self) -> bool:
        return self.safety_level is SafetyLevel.DESTRUCTIVE

    @property
    def requires_sudo(self) -> bool:
        return self.safety_level is SafetyLevel.SUDO_REQUIRED

    @property
    def requires_confirmation(self) -> bool:
        return self.safety_level in (
            SafetyLevel.DESTRUCTIVE,
            SafetyLevel.SUDO_REQUIRED,
        )

