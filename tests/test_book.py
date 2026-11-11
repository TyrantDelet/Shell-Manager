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
            len(commands),
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

    
    def test_safety_guardrails_metadata(self):
        rm_cmd = get_command_by_name("rm")
        self.assertIsNotNone(rm_cmd)
        self.assertTrue(rm_cmd.is_destructive)
        self.assertTrue(rm_cmd.requires_confirmation)

        chmod_cmd = get_command_by_name("chmod")
        self.assertIsNotNone(chmod_cmd)
        self.assertTrue(chmod_cmd.requires_sudo)
        self.assertTrue(chmod_cmd.requires_confirmation)

        chown_cmd = get_command_by_name("chown")
        self.assertIsNotNone(chown_cmd)
        self.assertTrue(chown_cmd.requires_sudo)
        self.assertTrue(chown_cmd.requires_confirmation)

        pwd_cmd = get_command_by_name("pwd")
        self.assertIsNotNone(pwd_cmd)
        self.assertFalse(pwd_cmd.requires_confirmation)

        ls_cmd = get_command_by_name("ls")
        self.assertIsNotNone(ls_cmd)
        self.assertFalse(ls_cmd.requires_confirmation)

    def test_lookup_and_search(self):
        self.assertIsNotNone(get_command_by_name("ls"))
        self.assertIsNotNone(get_command_by_name("LS"))
        self.assertIsNone(get_command_by_name("nonexistent_command_xyz"))

        results = search_commands("directory")
        self.assertGreater(len(results), 0)
        found_names = [c.name for c in results]
        self.assertIn("ls", found_names)


if __name__ == "__main__":
    unittest.main()