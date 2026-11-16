from __future__ import annotations

from enum import StrEnum
from typing import Final

from rich.console import Console, RenderableType
from rich.markup import escape
from rich.panel import Panel
from rich.table import Table

from app.models import Command, SafetyLevel
from app.ui.theme import (
    BOX_ROUNDED,
    SAFETY_BORDER_STYLES,
    Symbols,
    FormattingHelpers,
    get_console,
)

class ViewAction(StrEnum):
    EXECUTE = "1"
    COPY = "2"
    BACK = "b"
    QUIT = "q"

    @property
    def label(self) -> str:
        return _ACTION_LABELS[self]


_ACTION_LABELS: Final[dict[ViewAction, str]] = {
    ViewAction.EXECUTE: "Execute command",
    ViewAction.COPY: "Copy to clipboard",
    ViewAction.BACK: "Back to list",
    ViewAction.QUIT: "Quit",
}

VIEW_ACTIONS: Final[tuple[tuple[str, str], ...]] = (
    ("1", "Execute command"),
    ("2", "Copy to clipboard"),
    ("b", "Back to list"),
    ("q", "Quit"),
)

def build_header_panel(command: Command) -> Panel:
    border_style = SAFETY_BORDER_STYLES.get(command.safety_level, "panel.border")
    safety_badge = FormattingHelpers.format_safety_badge(command.safety_level, pill=True)
    category_badge = FormattingHelpers.format_category_badge(command.category, include_icon=True)

    header_text = (
        f"[command.name]{command.name}[/command.name]  {safety_badge}  {category_badge}\n\n"
        f"[command.summary]{command.summary}[/command.summary]\n\n"
        f"[dim]Syntax:[/dim] [command.syntax]{escape(command.syntax)}[/command.syntax]"
    )
    if command.default_args:
        header_text += f"  [dim](default: {escape(command.default_args)})[/dim]"

    return Panel(
        header_text,
        title=f"[bold]Command: {command.name}[/bold]",
        title_align="left",
        border_style=border_style,
        box=BOX_ROUNDED,
    )

def build_safety_banner(command: Command) -> Panel | None:
    if command.is_destructive:
        warning_msg = (
            f"[bold red]{Symbols.WARNING} DESTRUCTIVE OPERATION GUARDRAIL[/bold red]\n"
            f"[red]This command permanently deletes files or directories without an undo option.\n"
            f"Execution will strictly require explicit [bold][y/N][/bold] confirmation.[/red]"
        )
        return Panel(
            warning_msg,
            border_style="red",
            box=BOX_ROUNDED,
            title="[bold red]Safety Alert[/bold red]",
            title_align="left",
        )
    if command.requires_sudo:
        sudo_msg = (
            f"[bold magenta]{Symbols.SUDO} ELEVATED / PRIVILEGED OPERATION[/bold magenta]\n"
            f"[magenta]This command alters system configurations or services and requires sudo privileges.\n"
            f"Execution will require administrator access and explicit [bold][y/N][/bold] confirmation.[/magenta]"
        )
        return Panel(
            sudo_msg,
            border_style="magenta",
            box=BOX_ROUNDED,
            title="[bold magenta]Privilege Notice[/bold magenta]",
            title_align="left",
        )
    return None

def build_description_panel(command: Command) -> Panel:
    content = f"[command.description]{command.description}[/command.description]"
    if command.notes:
        content += (
            f"\n\n[bold yellow]{Symbols.INFO} Important Notes:[/bold yellow]\n"
            f"[command.notes]{command.notes}[/command.notes]"
        )

    return Panel(
        content,
        title="[bold cyan]Explanation & Context[/bold cyan]",
        title_align="left",
        border_style="blue",
        box=BOX_ROUNDED,
    )

def build_flags_table(command: Command) -> Table:
    table = Table(
        title="Common Flags & Options",
        box=BOX_ROUNDED,
        border_style="table.border",
        header_style="table.header",
        title_justify="left",
        expand=True,
    )
    table.add_column("Flag", style="command.flag", no_wrap=True)
    table.add_column("Meaning / Name", style="command.flag_name", no_wrap=True)
    table.add_column("Description", style="command.flag_desc")
    table.add_column("Example", style="command.example", no_wrap=True)

    if not command.flags:
        table.add_row("-", "No specific flags", "This command does not define special flags.", "-")
    else:
        for f in command.flags:
            example = f.example if f.example else f"{command.name} {f.flag}"
            table.add_row(f.flag, f.name, f.description, example)

    return table

def build_examples_table(command: Command) -> Table:
    table = Table(
        title="Common Command Examples",
        box=BOX_ROUNDED,
        border_style="table.border",
        header_style="table.header",
        title_justify="left",
        expand=True,
    )
    table.add_column("#", style="dim", width=4, justify="right")
    table.add_column("Command", style="command.example", no_wrap=True)
    table.add_column("What it does", style="command.example_desc")

    if not command.examples:
        table.add_row("1", command.name, command.summary)
    else:
        for idx, ex in enumerate(command.examples, start=1):
            table.add_row(str(idx), ex.command, ex.description)

    return table


def format_action_bar() -> str:
    return FormattingHelpers.format_nav_bar(VIEW_ACTIONS)


def build_exploded_view(command: Command) -> list[RenderableType]:
    renderables: list[RenderableType] = []

    renderables.append(build_header_panel(command))

    safety_banner = build_safety_banner(command)
    if safety_banner is not None:
        renderables.append(safety_banner)

    renderables.append(build_description_panel(command))

    renderables.append(build_flags_table(command))

    renderables.append(build_examples_table(command))

    return renderables

def render_exploded_view(command: Command, console: Console | None = None) -> None:
    c = console or get_console()
    c.print()
    for renderable in build_exploded_view(command):
        c.print(renderable)
    c.print()
    c.print(format_action_bar())
    c.print()

def render_command_preview(
    command_str: str,
    safety_level: SafetyLevel,
    console: Console | None = None,
) -> None:
    c = console or get_console()
    border_style = SAFETY_BORDER_STYLES.get(safety_level, "cyan")
    badge = FormattingHelpers.format_safety_badge(safety_level, pill=True)

    content = (
        f"[dim]Prepared Command:[/dim]\n\n"
        f"  [exec.preview] {escape(command_str)} [/exec.preview]\n\n"
        f"Safety Classification: {badge}"
    )

    if safety_level in (SafetyLevel.DESTRUCTIVE, SafetyLevel.SUDO_REQUIRED):
        content += (
            f"\n\n[bold red]{Symbols.WARNING} Explicit confirmation required before running.[/bold red]"
        )

    c.print(
        Panel(
            content,
            title="[bold]Execution Preview[/bold]",
            title_align="left",
            border_style=border_style,
            box=BOX_ROUNDED,
        )
    )

def render_clipboard_box(
    command_str: str,
    was_copied: bool = False,
    console: Console | None = None,
) -> None:
    c = console or get_console()
    if was_copied:
        title = f"[bold green]{Symbols.CHECK} Copied to System Clipboard![/bold green]"
        status_msg = (
            "[green]The command has been copied to your clipboard. "
            "You can paste it into any terminal.[/green]"
        )
    else:
        title = f"[bold cyan]{Symbols.TERMINAL} Copy Command[/bold cyan]"
        status_msg = (
            "[dim]No native clipboard utility detected (xclip/wl-copy).[/dim]\n"
            "[white]You can manually select and copy the command below:[/white]"
        )

    content = f"{status_msg}\n\n  [exec.preview] {escape(command_str)} [/exec.preview]"

    c.print(
        Panel(
            content,
            title=title,
            title_align="left",
            border_style="green" if was_copied else "cyan",
            box=BOX_ROUNDED,
        )
    )

def parse_view_action(raw_input: str) -> ViewAction | None:
    cleaned = raw_input.strip().lower()
    mapping: dict[str, ViewAction] = {
        "1": ViewAction.EXECUTE,
        "execute": ViewAction.EXECUTE,
        "run": ViewAction.EXECUTE,
        "e": ViewAction.EXECUTE,
        "2": ViewAction.COPY,
        "copy": ViewAction.COPY,
        "c": ViewAction.COPY,
        "b": ViewAction.BACK,
        "back": ViewAction.BACK,
        "q": ViewAction.QUIT,
        "quit": ViewAction.QUIT,
        "exit": ViewAction.QUIT,
    }
    return mapping.get(cleaned)

def prompt_view_action(console: Console | None = None) -> ViewAction:
    c = console or get_console()
    while True:
        try:
            choice = c.input(FormattingHelpers.format_prompt("Choose an action [1, 2, b, q]", default="1"))
            action = parse_view_action(choice if choice.strip() else "1")
            if action is not None:
                return action
            c.print("[warning]Invalid option. Please enter 1, 2, 'b' (back), or 'q' (quit).[/warning]")
        except (KeyboardInterrupt, EOFError):
            c.print("\n[dim]Returning to previous menu...[/dim]")
            return ViewAction.BACK