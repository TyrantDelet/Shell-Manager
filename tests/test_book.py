import unittest

from app.book import (
    get_all_commands,
    get_command_by_name,
    get_commands_by_category,
    search_commands,
)

from app.models import Category, SafetyLevel

class CommandBookTest(unittest.TestCase):

    def test_book_coverage(self):
        commands = get_all_commands()
        self.assertGreaterEqual(
            len(comamnds),
            20
            f"Expected at least 20 commands, got {len(commands)}",
        )

    def test_all_core_categories_covered(self):
        for category in (
            Category.NAVIGATION,
            Category.FILE_MANIPULATION,
            Category.SYSTEM_LOGS,
        ):
            cmds = get_commands_by_category(category)
            self.assertGreater(
                len(cmds),
                0,
                f"Category {category.name} has no commands cataloged",
            )

    def test_command_fields_validity(self):
        for cmd in get_all_commands():
            with self.subTest(command=cmd.name):
                self.assertTrue(cmd.name, "Command name cannot be empty")
                self.assertIsInstance(cmd.category, Category)
                self.assertIsInstance(cmd.safety_level, SafetyLevel)
                self.assertTrue(cmd.summary, f"{cmd.name} must have a summary")
                self.assertTrue(cmd.description, f"{cmd.name} must have a description")
                self.assertTrue(cmd.syntax, f"{cmd.name} must have a syntax definition")
                self.assertGreater(
                    len(cmd.flags), 0, f"{cmd.name} must have at least one flag defined"
                )
                self.assertGreater(
                    len(cmd.examples),
                    0,
                    f"{cmd.name} must have at least one example defined",
                )

                for flag in cmd.flags:
                    self.assertTrue(flag.flag, f"Flag representation missing in {cmd.name}")
                    self.assertTrue(flag.name, f"Flag name missing in {cmd.name}")
                    self.assertTrue(
                        flag.description, f"Flag description missing in {cmd.name}"
                    )

                for ex in cmd.examples:
                    self.assertTrue(
                        ex.command, f"Example command missing in {cmd.name}"
                    )
                    self.assertTrue(
                        ex.description, f"Example description missing in {cmd.name}"
                    )