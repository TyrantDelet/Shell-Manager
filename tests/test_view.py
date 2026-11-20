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

class ViewTest(unittest.TestCase):

    def setUp(self) -> None:
        self.buffer = io.StringIO()
        self.console = Console(file=self.buffer, theme=THEME, no_color=True, width=120)

    def test_view_action_enum_and_labels(self) -> None:
        self.assertEqual(ViewAction.EXECUTE.value, "1")
        self.assertEqual(ViewAction.COPY.value, "2")
        self.assertEqual(ViewAction.BACK.value, "b")
        self.assertEqual(ViewAction.QUIT.value, "q")

        for action in ViewAction:
            self.assertTrue(action.label)

    def test_parse_view_action(self) -> None:
        self.assertEqual(parse_view_action("1"), ViewAction.EXECUTE)
        self.assertEqual(parse_view_action("execute"), ViewAction.EXECUTE)
        self.assertEqual(parse_view_action("run"), ViewAction.EXECUTE)
        self.assertEqual(parse_view_action("2"), ViewAction.COPY)
        self.assertEqual(parse_view_action("copy"), ViewAction.COPY)
        self.assertEqual(parse_view_action("b"), ViewAction.BACK)
        self.assertEqual(parse_view_action("back"), ViewAction.BACK)
        self.assertEqual(parse_view_action("q"), ViewAction.QUIT)
        self.assertEqual(parse_view_action("quit"), ViewAction.QUIT)
        self.assertEqual(parse_view_action("  B  "), ViewAction.BACK)
        self.assertEqual(parse_view_action("QUIT"), ViewAction.QUIT)
        self.assertIsNone(parse_view_action("invalid_choice"))
        self.assertIsNone(parse_view_action(""))

    def test_build_header_panel(self) -> None:
        ls_cmd = get_command_by_name("ls")
        self.assertIsNotNone(ls_cmd)
        panel = build_header_panel(ls_cmd)
        self.assertIsInstance(panel, Panel)
        self.console.print(panel)
        output = self.buffer.getvalue()
        self.assertIn("ls", output)
        self.assertIn("Syntax", output)
        self.assertIn("Navigation", output)

    def test_build_safety_banner(self) -> None:
        ls_cmd = get_command_by_name("ls")
        self.assertIsNotNone(ls_cmd)
        self.assertIsNone(build_safety_banner(ls_cmd))
        rm_cmd = get_command_by_name("rm")
        self.assertIsNotNone(rm_cmd)
        rm_banner = build_safety_banner(rm_cmd)
        self.assertIsNotNone(rm_banner)
        self.assertIsInstance(rm_banner, Panel)
        self.buffer.seek(0)
        self.buffer.truncate(0)
        self.console.print(rm_banner)
        rm_output = self.buffer.getvalue()
        self.assertIn("DESTRUCTIVE", rm_output)
        self.assertIn("confirmation", rm_output)
        chown_cmd = get_command_by_name("chown")
        self.assertIsNotNone(chown_cmd)
        chown_banner = build_safety_banner(chown_cmd)
        self.assertIsNotNone(chown_banner)
        self.assertIsInstance(chown_banner, Panel)
        self.buffer.seek(0)
        self.buffer.truncate(0)
        self.console.print(chown_banner)
        chown_output = self.buffer.getvalue()
        self.assertIn("ELEVATED", chown_output)

    def test_build_description_panel(self) -> None:
        ls_cmd = get_command_by_name("ls")
        self.assertIsNotNone(ls_cmd)
        panel = build_description_panel(ls_cmd)
        self.assertIsInstance(panel, Panel)
        self.console.print(panel)
        output = self.buffer.getvalue()
        self.assertIn("Lists files", output)
        self.assertIn("Important Notes", output)

    def test_build_flags_table(self) -> None:
        ls_cmd = get_command_by_name("ls")
        self.assertIsNotNone(ls_cmd)
        table = build_flags_table(ls_cmd)
        self.assertIsInstance(table, Table)
        self.console.print(table)
        output = self.buffer.getvalue()
        self.assertIn("-l", output)
        self.assertIn("-a", output)
        self.assertIn("-h", output)

    def test_build_flags_table_empty(self) -> None:
        bare_cmd = Command(
            name="testcmd",
            category=Category.NAVIGATION,
            safety_level=SafetyLevel.READ_ONLY,
            summary="Test summary",
            description="Test description",
            syntax="testcmd",
            flags=(),
        )
        table = build_flags_table(bare_cmd)
        self.assertIsInstance(table, Table)
        self.console.print(table)
        output = self.buffer.getvalue()
        self.assertIn("No specific flags", output)

    def test_build_examples_table(self) -> None:
        rm_cmd = get_command_by_name("rm")
        self.assertIsNotNone(rm_cmd)
        table = build_examples_table(rm_cmd)
        self.assertIsInstance(table, Table)
        self.console.print(table)
        output = self.buffer.getvalue()
        self.assertIn("rm -i", output)

    def test_format_action_bar(self) -> None:
        bar = format_action_bar()
        self.console.print(bar)
        output = self.buffer.getvalue()
        self.assertIn("[1]", output)
        self.assertIn("[2]", output)
        self.assertIn("[b]", output)
        self.assertIn("[q]", output)

    def test_exploded_view_renderable(self) -> None:
        for cmd_name in ("ls", "rm", "chmod", "journalctl"):
            with self.subTest(command=cmd_name):
                cmd = get_command_by_name(cmd_name)
                self.assertIsNotNone(cmd)
                renderables = build_exploded_view(cmd)
                self.assertGreaterEqual(len(renderables), 4)
                self.buffer.seek(0)
                self.buffer.truncate(0)
                render_exploded_view(cmd, console=self.console)
                output = self.buffer.getvalue()
                self.assertIn(cmd.name, output)
                self.assertIn("[1]", output)

    def test_render_command_preview(self) -> None:
        render_command_preview("rm -rf /tmp/test", SafetyLevel.DESTRUCTIVE, console=self.console)
        output = self.buffer.getvalue()
        self.assertIn("rm -rf /tmp/test", output)
        self.assertIn("DESTRUCTIVE", output)

    def test_render_clipboard_box(self) -> None:
        self.buffer.seek(0)
        self.buffer.truncate(0)
        render_clipboard_box("ls -lah", was_copied=True, console=self.console)
        output_copied = self.buffer.getvalue()
        self.assertIn("ls -lah", output_copied)
        self.assertIn("Copied to System Clipboard", output_copied)
        self.buffer.seek(0)
        self.buffer.truncate(0)
        render_clipboard_box("ls -lah", was_copied=False, console=self.console)
        output_manual = self.buffer.getvalue()
        self.assertIn("ls -lah", output_manual)
        self.assertIn("manually select and copy", output_manual)


if __name__ == "__main__":
    unittest.main()
