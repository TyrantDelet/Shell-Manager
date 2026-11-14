from __future__ import annotations

import io

from rich.console import Console
from rich.theme import Theme

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

    def test_palette_constants(self) -> None:
        self.assertTrue(PRIMARY)
        self.assertTrue(SUCCESS)
        self.assertTrue(WARNING)

    def test_symbols_completeness(self) -> None:
        for attr in (
            "READ_ONLY",
            "MODIFICATION",
            "DESTRUCTIVE",
            "SUDO",
            "CHECK",
            "CROSS",
            "WARNING",
            "INFO",
            "ARROW_RIGHT",
            "ARROW_LEFT",
            "NAVIGATION",
            "FILE",
            "LOGS",
        ):
            val = getattr(Symbols, attr, None)
            self.assertIsNotNone(val, f"Symbol {attr} is missing")
            self.assertIsInstance(val, str)
            self.assertGreater(len(val), 0)

    def test_theme_styles_renderable(self) -> None:
        self.assertIsInstance(THEME, Theme)
        for style_name in THEME_STYLES:
            with self.subTest(style=style_name):
                try:
                    self.color_console.print(f"[{style_name}]Test Content[/{style_name}]")
                except Exception as exc:
                    self.fail(f"Failed to render theme style {style_name!r}: {exc}")

    def test_safety_mappings_cover_all_levels(self) -> None:
        for level in SafetyLevel:
            with self.subTest(level=level):
                self.assertIn(level, SAFETY_STYLES)
                self.assertIn(level, SAFETY_BADGE_STYLES)
                self.assertIn(level, SAFETY_ICONS)
                self.assertIn(level, SAFETY_BADGES)
                self.assertIn(level, SAFETY_BORDER_STYLES)

                badge_markup = SAFETY_BADGES[level]
                try:
                    self.color_console.print(badge_markup)
                except Exception as exc:
                    self.fail(f"Invalid markup in SAFETY_BADGES for {level}: {exc}")

    def test_category_mappings_cover_all_categories(self) -> None:
        for category in Category:
            with self.subTest(category=category):
                self.assertIn(category, CATEGORY_ICONS)
                self.assertIn(category, CATEGORY_STYLES)
                self.assertIn(category, CATEGORY_BORDER_STYLES)

    def test_format_key_escaping(self) -> None:
        rendered_key = FormattingHelpers.format_key("b", "Back")
        self.buffer.seek(0)
        self.buffer.truncate(0)
        self.test_console.print(rendered_key)
        output = self.buffer.getvalue()
        self.assertIn("[b]", output)
        self.assertIn("Back", output)

    def test_format_safety_badge_modes(self) -> None:
        for level in SafetyLevel:
            with self.subTest(level=level):
                std = FormattingHelpers.format_safety_badge(level, pill=False)
                pill = FormattingHelpers.format_safety_badge(level, pill=True)

                self.buffer.seek(0)
                self.buffer.truncate(0)
                self.test_console.print(std)
                std_out = self.buffer.getvalue()
                self.assertTrue(std_out.strip())

                self.buffer.seek(0)
                self.buffer.truncate(0)
                self.test_console.print(pill)
                pill_out = self.buffer.getvalue()
                self.assertTrue(pill_out.strip())

    def test_format_category_badge(self) -> None:
        for cat in Category:
            badge_with_icon = FormattingHelpers.format_category_badge(cat, include_icon=True)
            badge_no_icon = FormattingHelpers.format_category_badge(cat, include_icon=False)

            self.buffer.seek(0)
            self.buffer.truncate(0)
            self.test_console.print(badge_with_icon)
            self.assertIn(cat.display_name, self.buffer.getvalue())

            self.buffer.seek(0)
            self.buffer.truncate(0)
            self.test_console.print(badge_no_icon)
            self.assertIn(cat.display_name, self.buffer.getvalue())

    def test_format_banners_and_nav_bar(self) -> None:
        warn = FormattingHelpers.format_warning_banner("Test warning")
        danger = FormattingHelpers.format_danger_banner("Test danger")
        sudo = FormattingHelpers.format_sudo_banner("Test sudo")

        for banner in (warn, danger, sudo):
            self.buffer.seek(0)
            self.buffer.truncate(0)
            self.test_console.print(banner)
            self.assertTrue(self.buffer.getvalue().strip())

        nav = FormattingHelpers.format_nav_bar([("b", "Back"), ("q", "Quit"), ("r", "Run")])
        self.buffer.seek(0)
        self.buffer.truncate(0)
        self.test_console.print(nav)
        nav_out = self.buffer.getvalue()
        self.assertIn("[b]", nav_out)
        self.assertIn("[q]", nav_out)
        self.assertIn("[r]", nav_out)

    def test_format_prompt(self) -> None:
        p1 = FormattingHelpers.format_prompt("Enter choice")
        p2 = FormattingHelpers.format_prompt("Enter choice", default="1")
        self.buffer.seek(0)
        self.buffer.truncate(0)
        self.test_console.print(p1)
        self.assertIn("Enter choice", self.buffer.getvalue())

        self.buffer.seek(0)
        self.buffer.truncate(0)
        self.test_console.print(p2)
        self.assertIn("(1)", self.buffer.getvalue())

    def test_console_management(self) -> None:
        c1 = get_console()
        self.assertIsInstance(c1, Console)
        custom_console = Console()
        set_console(custom_console)
        self.assertIs(get_console(), custom_console)
        reset = reset_console()
        self.assertIsNot(reset, custom_console)
        self.assertIs(get_console(), reset)

    def test_box_styles(self) -> None:
        self.assertIsNotNone(BOX_DEFAULT)
        self.assertIsNotNone(BOX_ROUNDED)

if __name__ == "__main__":
    unittest.main()
