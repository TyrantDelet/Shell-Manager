from __future__ import annotations

from types import MappingProxyType
from typing import Final, Iterable

from rich.box import DOUBLE, HEAVY, MINIMAL, ROUNDED, SIMPLE, Box
from rich.console import Console
from rich.markup import escape
from rich.theme import Theme

from app.models import Category, SafetyLevel

class Symbols:

    READ_ONLY: Final[str] = "●"
    MODIFICATION: Final[str] = "▲"
    DESTRUCTIVE: Final[str] = "■"
    SUDO: Final[str] = "⚡"

    CHECK: Final[str] = "✔"
    CROSS: Final[str] = "✖"
    WARNING: Final[str] = "⚠"
    INFO: Final[str] = "ℹ"
    QUESTION: Final[str] = "?"

    ARROW_RIGHT: Final[str] = "→"
    ARROW_LEFT: Final[str] = "←"
    BULLET: Final[str] = "•"
    CHEVRON_RIGHT: Final[str] = "›"
    POINTER: Final[str] = "▶"

    NAVIGATION: Final[str] = "🧭"
    FILE: Final[str] = "📁"
    LOGS: Final[str] = "📋"
    TERMINAL: Final[str] = "💻"
    BOOK: Final[str] = "📖"
    SEARCH: Final[str] = "🔍"
    GEAR: Final[str] = "⚙"
    SHIELD: Final[str] = "🛡"