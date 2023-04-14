import unittest

from recursive_gpt.commands import execute_command


class TestExecuteCommand(unittest.TestCase):
    def test_do_nothing(self):
        result = execute_command("do_nothing", {})
        self.assertEqual(result, "No action performed.")

    def test_unknown_command(self):
        result = execute_command("unknown_command", {})
        self.assertEqual(result, "Unknown command 'unknown_command'. Please refer to the 'COMMANDS' list for available commands and only respond in the specified JSON format.")

if __name__ == "__main__":
    unittest.main()