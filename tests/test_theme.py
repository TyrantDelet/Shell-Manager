from __future__ import annotations

import io

from rich.console import Console

from app.models import Category, SafetyLevel
from app.ui.theme import (
    BOX_DEFAULT,
    BOX_ROUNDED,
    CATEGORY_BORDER_STYLES,
    CATEGORY_ICONS,
    CATEGORY_STYLES,
    PRIMARY,
    SAFETY_BADGE_STYLES,
    SAFETY_BADGES,
    SAFETY_BORDER_STYLES,
    SAFETY_ICONS,
    SAFETY_STYLES,
    SUCCESS,
    WARNING,
    FormattingHelpers,
    Symbols,
    THEME,
    THEME_STYLES,
    get_console,
    reset_console,
    set_console,
)

import unittest

class ThemeTest(unittest.TestCase):

    def setUp(self) -> None:
        reset_console()
        self.buffer = io.StringIO()
        self.test_console = Console(file=self.buffer, theme=THEME, no_color=True, width=120)
        self.color_console = Console(file=io.StringIO(), theme=THEME, color_system="truecolor", width=120)


if __name__ == "__main__":
    unittest.main()
