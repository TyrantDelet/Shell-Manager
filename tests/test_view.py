from __future__ import annotations

import io
import unittest

from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from app.book import get_command_by_name
from app.models import Category, Command, SafetyLevel
from app.ui.theme import THEME
from app.ui.view import (
    ViewAction,
    build_description_panel,
    build_examples_table,
    build_exploded_view,
    build_flags_table,
    build_header_panel,
    build_safety_banner,
    format_action_bar,
    parse_view_action,
    render_clipboard_box,
    render_command_preview,
    render_exploded_view,
)


