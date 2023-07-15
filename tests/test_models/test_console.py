import unittest
from unittest.mock import patch
from io import StringIO
import console
import os


class TestConsole(unittest.TestCase):

    def setUp(self):
        self.console = console.HBNBCommand()
        self.file_path = "file.json"

    def tearDown(self):
        try:
            os.remove(self.file_path)
        except FileNotFoundError:
            pass

    def test_create(self):
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create State")
            state_id = f.getvalue().strip()
            self.assertTrue(len(state_id) > 0)

    def test_show(self):
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create State")
            state_id = f.getvalue().strip()

            self.console.onecmd(f"show State {state_id}")
            self.assertEqual(f.getvalue().strip(), f"[State] ({state_id}) {{}}")

    def test_destroy(self):
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create State")
            state_id = f.getvalue().strip()

            self.console.onecmd(f"destroy State {state_id}")
            self.assertEqual(f.getvalue().strip(), "")

    def test_update(self):
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create State")
            state_id = f.getvalue().strip()

            self.console.onecmd(f"update State {state_id} name 'California'")
            self.assertEqual(f.getvalue().strip(), "")

            self.console.onecmd(f"show State {state_id}")
            self.assertEqual(f.getvalue().strip(), f"[State] ({state_id}) {{'name': 'California'}}")

    def test_all(self):
        with patch('sys.stdout', new=StringIO()) as f:
            self.console.onecmd("create State")
            state_id = f.getvalue().strip()

            self.console.onecmd("create City")
            city_id = f.getvalue().strip()

            self.console.onecmd("all")
            expected_output = f"[State] ({state_id}) {{'id': '{state_id}'}}\n"
            expected_output += f"[City] ({city_id}) {{'id': '{city_id}'}}"
            self.assertEqual(f.getvalue().strip(), expected_output)

    def test_quit(self):
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertTrue(self.console.onecmd("quit"))
            self.assertEqual(f.getvalue().strip(), "")

    def test_EOF(self):
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertTrue(self.console.onecmd("EOF"))
            self.assertEqual(f.getvalue().strip(), "")

    def test_emptyline(self):
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(self.console.onecmd(""))
            self.assertEqual(f.getvalue().strip(), "")

    def test_help(self):
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(self.console.onecmd("help"))
            self.assertTrue(len(f.getvalue().strip()) > 0)

    def test_unknown_command(self):
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertFalse(self.console.onecmd("unknown_command"))
            self.assertEqual(f.getvalue().strip(), "*** Unknown syntax: unknown_command")

    def test_console_with_file_storage(self):
        with patch('sys.stdout', new=StringIO()) as f:
            self.assertTrue(self.console.onecmd("create State"))
            self.assertTrue(os.path.exists(self.file_path))


if __name__ == "__main__":
    unittest.main()
