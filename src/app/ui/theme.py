from __future__ import annotations

from types import MappingProxyType
from typing import Final, Iterable

from rich.box import DOUBLE, HEAVY, MINIMAL, ROUNDED, SIMPLE, Box
from rich.console import Console
from rich.markup import escape
from rich.theme import Theme

from app.models import Category, SafetyLevel


# Color Pallete and Box Borders 

PRIMARY: Final[str] = "cyan"
PRIMARY_BOLD: Final[str] = "bold cyan"
SECONDARY: Final[str] = "blue"
ACCENT: Final[str] = "magenta"
SUCCESS: Final[str] = "green"
WARNING: Final[str] = "yellow"
DANGER: Final[str] = "red"
ELEVATED: Final[str] = "magenta"
MUTED: Final[str] = "dim"
TEXT: Final[str] = "white"
TEXT_MUTED: Final[str] = "dim white"
HIGHLIGHT: Final[str] = "bright_yellow"

BOX_ROUNDED: Final[Box] = ROUNDED
BOX_HEAVY: Final[Box] = HEAVY
BOX_DOUBLE: Final[Box] = DOUBLE
BOX_MINIMAL: Final[Box] = MINIMAL
BOX_SIMPLE: Final[Box] = SIMPLE
BOX_DEFAULT: Final[Box] = ROUNDED

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

SAFETY_STYLES: Final[MappingProxyType[SafetyLevel, str]] = MappingProxyType(
    {
        SafetyLevel.READ_ONLY: "safety.read_only",
        SafetyLevel.MODIFICATION: "safety.modification",
        SafetyLevel.DESTRUCTIVE: "safety.destructive",
        SafetyLevel.SUDO_REQUIRED: "safety.sudo_required",
    }
)

SAFETY_BADGES: Final[MappingProxyType[SafetyLevel, str]] = MappingProxyType(
    {
        SafetyLevel.READ_ONLY: f"[green]{Symbols.READ_ONLY} READ-ONLY[/green]",
        SafetyLevel.MODIFICATION: f"[yellow]{Symbols.MODIFICATION} MODIFICATION[/yellow]",
        SafetyLevel.DESTRUCTIVE: f"[red]{Symbols.DESTRUCTIVE} DESTRUCTIVE[/red]",
        SafetyLevel.SUDO_REQUIRED: f"[magenta]{Symbols.SUDO} SUDO REQUIRED[/magenta]",
    }
)

SAFETY_BADGE_STYLES: Final[MappingProxyType[SafetyLevel, str]] = MappingProxyType(
    {
        SafetyLevel.READ_ONLY: "badge.read_only",
        SafetyLevel.MODIFICATION: "badge.modification",
        SafetyLevel.DESTRUCTIVE: "badge.destructive",
        SafetyLevel.SUDO_REQUIRED: "badge.sudo_required",
    }
)

SAFETY_ICONS: Final[MappingProxyType[SafetyLevel, str]] = MappingProxyType(
    {
        SafetyLevel.READ_ONLY: Symbols.READ_ONLY,
        SafetyLevel.MODIFICATION: Symbols.MODIFICATION,
        SafetyLevel.DESTRUCTIVE: Symbols.DESTRUCTIVE,
        SafetyLevel.SUDO_REQUIRED: Symbols.SUDO,
    }
)

SAFETY_BORDER_STYLES: Final[MappingProxyType[SafetyLevel, str]] = MappingProxyType(
    {
        SafetyLevel.READ_ONLY: "green",
        SafetyLevel.MODIFICATION: "yellow",
        SafetyLevel.DESTRUCTIVE: "red",
        SafetyLevel.SUDO_REQUIRED: "magenta",
    }
)

CATEGORY_ICONS: Final[MappingProxyType[Category, str]] = MappingProxyType(
    {
        Category.NAVIGATION: Symbols.NAVIGATION,
        Category.FILE_MANIPULATION: Symbols.FILE,
        Category.SYSTEM_LOGS: Symbols.LOGS,
    }
)

CATEGORY_STYLES: Final[MappingProxyType[Category, str]] = MappingProxyType(
    {
        Category.NAVIGATION: "category.navigation",
        Category.FILE_MANIPULATION: "category.file_manipulation",
        Category.SYSTEM_LOGS: "category.system_logs",
    }
)

CATEGORY_BORDER_STYLES: Final[MappingProxyType[Category, str]] = MappingProxyType(
    {
        Category.NAVIGATION: "bright_cyan",
        Category.FILE_MANIPULATION: "bright_yellow",
        Category.SYSTEM_LOGS: "bright_blue",
    }
)

CONSOLE: Console | None = None

def set_console(new_console: Console) -> None:
    global _CONSOLE
    _CONSOLE = new_console


def get_console() -> Console:
    global _CONSOLE
    if _CONSOLE is None:
        _CONSOLE = Console(theme=THEME)
    return _CONSOLE


def reset_console() -> Console:
    global _CONSOLE
    _CONSOLE = Console(theme=THEME)
    return _CONSOLE

console: Console = get_console()


class FormattingHelpers():
        
    def format_key(key: str, label: str = "") -> str:
        escaped_bracketed = escape(f"[{key}]")
        styled_key = f"[menu.key]{escaped_bracketed}[/menu.key]"
        if label:
            return f"{styled_key} {label}"
        return styled_key


    def format_safety_badge(safety_level: SafetyLevel, pill: bool = False) -> str:
        icon = SAFETY_ICONS.get(safety_level, Symbols.INFO)
        label = safety_level.name.replace("_", " ").upper()

        if pill:
            style = SAFETY_BADGE_STYLES.get(safety_level, "bold white on blue")
            return f"[{style}] {icon} {label} [/{style}]"

        style = SAFETY_STYLES.get(safety_level, "white")
        return f"[{style}]{icon} {label}[/{style}]"


    def format_category_badge(category: Category, include_icon: bool = True) -> str:
        icon = CATEGORY_ICONS.get(category, "")
        style = CATEGORY_STYLES.get(category, "white")
        display_name = category.display_name
        if include_icon and icon:
            return f"[{style}]{icon} {display_name}[/{style}]"
        return f"[{style}]{display_name}[/{style}]"


    def format_warning_banner(message: str) -> str:
        return f"[warning]{Symbols.WARNING} {message}[/warning]"


    def format_danger_banner(message: str) -> str:
        return f"[danger]{Symbols.DESTRUCTIVE} {message}[/danger]"


    def format_sudo_banner(message: str) -> str:
        return f"[safety.sudo_required]{Symbols.SUDO} {message}[/safety.sudo_required]"


    def format_nav_bar(actions: Iterable[tuple[str, str]], separator: str = "  [dim]|[/dim]  ") -> str:
        rendered_actions = [FormattingHelpers.format_key(key, label) for key, label in actions]
        return separator.join(rendered_actions)


    def format_prompt(message: str = "Select an option", default: str = "") -> str:
        if default:
            return f"[prompt]{message}[/prompt] [prompt.bracket]([prompt.default]{default}[/prompt.default]):[/prompt.bracket] "
        return f"[prompt]{message}:[/prompt] "


if __name__ == "__main__":
    from rich.panel import Panel
    from rich.table import Table

    demo_console = get_console()

    demo_console.print()
    demo_console.print(
        Panel(
            "[app.title]Shell Manager[/app.title] - [app.subtitle]Interactive Linux Terminal Guide[/app.subtitle]\n"
            "[app.version]v1.0.0[/app.version] [app.author](by Tyrant_Delet)[/app.author]",
            border_style="app.border",
            box=BOX_ROUNDED,
            title="[bold cyan]Theme Preview[/bold cyan]",
        )
    )

    badge_table = Table(
        title="Visual Safety Badges (Implementation Plan Compliance)",
        box=BOX_ROUNDED,
        border_style="panel.border",
        header_style="table.header",
    )
    badge_table.add_column("Safety Level", style="bold white")
    badge_table.add_column("Standard Badge")
    badge_table.add_column("Pill Badge")
    badge_table.add_column("Behavior & Guardrails", style="dim")

    descriptions = {
        SafetyLevel.READ_ONLY: "Safe to run without system risk",
        SafetyLevel.MODIFICATION: "Alters user files",
        SafetyLevel.DESTRUCTIVE: "Can delete data - requires explicit [y/N] confirmation",
        SafetyLevel.SUDO_REQUIRED: "Elevated / Sudo required - requires explicit [y/N] confirmation",
    }

    for level in SafetyLevel:
        badge_table.add_row(
            level.name,
            FormattingHelpers.format_safety_badge(level, pill=False),
            FormattingHelpers.format_safety_badge(level, pill=True),
            descriptions.get(level, ""),
        )
    demo_console.print(badge_table)

    cat_table = Table(
        title="Core Categories",
        box=BOX_ROUNDED,
        border_style="panel.border",
        header_style="table.header",
    )
    cat_table.add_column("Category", style="bold white")
    cat_table.add_column("Badge")
    cat_table.add_column("Description", style="dim")

    for cat in Category:
        cat_table.add_row(
            cat.name,
            FormattingHelpers.format_category_badge(cat),
            cat.description,
        )
    demo_console.print(cat_table)

    demo_console.print("\n[bold]Status & Alert Banners:[/bold]")
    demo_console.print(FormattingHelpers.format_warning_banner("Modification warning: alters files."))
    demo_console.print(FormattingHelpers.format_danger_banner("Destructive action: permanent data loss risk."))
    demo_console.print(FormattingHelpers.format_sudo_banner("Privileged operation: requires elevated sudo credentials."))

    demo_console.print("\n[bold]Navigation Bar & Prompts:[/bold]")
    demo_console.print(
        FormattingHelpers.format_nav_bar([("1..5", "Select"), ("s", "Search"), ("b", "Back"), ("q", "Quit")])
    )
    demo_console.print(FormattingHelpers.format_prompt("Select an option", default="1"))
    demo_console.print()

    