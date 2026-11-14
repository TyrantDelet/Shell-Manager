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


THEME_STYLES: Final[dict[str, str]] = {

    # Application header & branding
    "app.title": "bold bright_cyan",
    "app.subtitle": "dim cyan",
    "app.version": "dim green",
    "app.author": "dim italic",
    "app.border": "cyan",

    # Safety levels (text styling)
    "safety.read_only": "bold green",
    "safety.modification": "bold yellow",
    "safety.destructive": "bold red",
    "safety.sudo_required": "bold magenta",

    # Contrasting badge pill styles
    "badge.read_only": "black on green",
    "badge.modification": "black on yellow",
    "badge.destructive": "bold white on red",
    "badge.sudo_required": "bold white on magenta",

    # Categories
    "category.navigation": "bold bright_cyan",
    "category.file_manipulation": "bold bright_blue",
    "category.system_logs": "bold bright_magenta",

    # Command exploded view
    "command.name": "bold bright_white",
    "command.summary": "white",
    "command.description": "bright_white",
    "command.syntax": "bold bright_green",
    "command.syntax_box": "bold green on grey15",
    "command.flag": "bold bright_yellow",
    "command.flag_name": "bold white",
    "command.flag_desc": "white",
    "command.example": "bold bright_cyan",
    "command.example_desc": "dim italic white",
    "command.notes": "italic yellow",

    # Menus and options
    "menu.title": "bold cyan",
    "menu.item": "white",
    "menu.desc": "dim white",
    "menu.index": "bold bright_yellow",
    "menu.key": "bold bright_cyan",
    "menu.selected": "reverse bold",
    "menu.back": "bold yellow",
    "menu.exit": "bold red",
    "menu.search": "bold cyan",
    "menu.footer": "dim",
    "menu.border": "bright_blue",

    # Status & Alerts
    "info": "bright_cyan",
    "success": "bold green",
    "warning": "bold yellow",
    "danger": "bold red",
    "error": "bold bright_red",
    "muted": "dim",
    "highlight": "bold bright_yellow",

    # Prompts & inputs
    "prompt": "bold cyan",
    "prompt.bracket": "dim",
    "prompt.choice": "bold bright_yellow",
    "prompt.default": "dim italic",
    "prompt.danger": "bold red",
    "prompt.confirm": "bold bright_red",

    # Execution preview & output
    "exec.preview": "bold bright_white on grey15",
    "exec.confirm": "bold red",
    "exec.running": "bold yellow",
    "exec.success": "bold green",
    "exec.failed": "bold red",
    "exec.output": "white",

    # Tables & Panels
    "panel.border": "blue",
    "panel.border.safe": "green",
    "panel.border.warning": "yellow",
    "panel.border.danger": "red",
    "panel.border.sudo": "magenta",
    "table.header": "bold cyan",
    "table.border": "dim blue",
}

THEME: Final[Theme] = Theme(THEME_STYLES)