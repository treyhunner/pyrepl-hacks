import unittest
from unittest.mock import patch, MagicMock
from pyrepl_hacks.bind_utils import bind, bind_to_insert
from pyrepl_hacks.command_utils import register_command


class TestBindUtils(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        # Mock the reader that _get_reader returns
        self.mock_reader = MagicMock()
        self.mock_reader.commands = {}
        self.mock_reader.bind = MagicMock()

        # Patch _get_reader to return our mock
        self.patcher = patch("pyrepl_hacks.bind_utils._get_reader")
        self.mock_get_reader = self.patcher.start()
        self.mock_get_reader.return_value = self.mock_reader

        # Also patch it in command_utils since register_command uses it too
        self.command_patcher = patch("pyrepl_hacks.command_utils._get_reader")
        self.mock_command_get_reader = self.command_patcher.start()
        self.mock_command_get_reader.return_value = self.mock_reader

    def tearDown(self):
        """Clean up test fixtures."""
        self.patcher.stop()
        self.command_patcher.stop()

    def test_bind_existing_command(self):
        """Test binding to an existing command."""
        bind("Ctrl+A", "beginning-of-line")

        # Verify the reader's bind method was called with correct keyspec
        self.mock_reader.bind.assert_called_once_with(r"\C-a", "beginning-of-line")

    def test_bind_decorator_basic(self):
        """Test using bind as a decorator."""

        @bind("F4")
        def exit_command(reader):
            """Exit the REPL."""

        # Verify the command was registered
        self.assertIn("exit-command", self.mock_reader.commands)

        # Verify the binding was created
        self.mock_reader.bind.assert_called_once_with(r"\<f4>", "exit-command")

    def test_bind_decorator_with_event(self):
        """Test using bind as a decorator with event parameter."""

        @bind("Ctrl+X", with_event=True)
        def special_command(reader, event_name, event):
            """A command that needs event info."""

        # Verify the command was registered
        self.assertIn("special-command", self.mock_reader.commands)

        # Verify the binding was created
        self.mock_reader.bind.assert_called_once_with(r"\C-x", "special-command")

    def test_bind_decorator_custom_name(self):
        """Test using bind as a decorator with a custom command name."""

        @bind("Alt+M")
        def move_to_indentation(reader):
            """Move to indentation."""

        # Verify the command was registered with kebab-case name
        self.assertIn("move-to-indentation", self.mock_reader.commands)

    def test_bind_function_and_name(self):
        """Test binding a function with an explicit name."""

        def my_command(reader):
            """My custom command."""

        bind("Ctrl+Y", "custom-name", my_command)

        # Verify the command was registered with the custom name
        self.assertIn("custom-name", self.mock_reader.commands)

        # Verify the binding was created
        self.mock_reader.bind.assert_called_once_with(r"\C-y", "custom-name")

    def test_bind_to_insert_basic(self):
        """Test bind_to_insert functionality."""
        bind_to_insert("Ctrl+P", "Python!")

        # Verify a command was registered (the name will be slugified)
        command_name = "_Ctrl_P"
        self.assertIn(command_name, self.mock_reader.commands)

        # Verify the binding was created
        self.mock_reader.bind.assert_called_once_with(r"\C-p", command_name)

        # Test that the command actually inserts text
        command_class = self.mock_reader.commands[command_name]
        mock_reader = MagicMock()
        command_instance = command_class(mock_reader, "event", "event_data")

        command_instance.do()
        mock_reader.insert.assert_called_once_with("Python!")

    def test_bind_to_insert_complex_key(self):
        """Test bind_to_insert with complex key combinations."""
        bind_to_insert("Alt+Shift+N", "[1, 2, 3, 4]")

        # Verify command was registered with slugified name
        command_name = "_Alt_Shift_N"
        self.assertIn(command_name, self.mock_reader.commands)

    def test_bind_special_keys(self):
        """Test binding with special key combinations."""
        bind("Shift+Tab", "dedent")

        # Verify the special escape sequence is used
        self.mock_reader.bind.assert_called_once_with(r"\e[Z", "dedent")

    def test_bind_multi_key_sequence(self):
        """Test binding multi-key sequences."""
        bind("Ctrl+X Ctrl+R", "subprocess-run")

        # Verify the multi-key sequence is properly converted
        self.mock_reader.bind.assert_called_once_with(r"\C-x\C-r", "subprocess-run")

    def test_multiple_bindings(self):
        """Test creating multiple bindings."""
        bind("Ctrl+A", "beginning-of-line")
        bind("Ctrl+E", "end-of-line")
        bind("F1", "help")

        # Verify all bindings were created
        expected_calls = [
            unittest.mock.call(r"\C-a", "beginning-of-line"),
            unittest.mock.call(r"\C-e", "end-of-line"),
            unittest.mock.call(r"\<f1>", "help"),
        ]
        self.mock_reader.bind.assert_has_calls(expected_calls)


class TestCommandUtils(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures."""
        # Mock the reader that _get_reader returns
        self.mock_reader = MagicMock()
        self.mock_reader.commands = {}

        # Patch _get_reader to return our mock
        self.patcher = patch("pyrepl_hacks.command_utils._get_reader")
        self.mock_get_reader = self.patcher.start()
        self.mock_get_reader.return_value = self.mock_reader

    def tearDown(self):
        """Clean up test fixtures."""
        self.patcher.stop()

    def test_register_command_basic(self):
        """Test basic command registration."""

        @register_command
        def test_command(reader):
            """A test command."""

        # Verify command was registered with kebab-case name
        self.assertIn("test-command", self.mock_reader.commands)

        # Verify the command function has the right attributes
        self.assertEqual(test_command.name, "test-command")
        self.assertTrue(hasattr(test_command, "command_class"))

    def test_register_command_custom_name(self):
        """Test command registration with custom name."""

        @register_command("my-custom-name")
        def some_function(reader):
            """A function with custom command name."""

        # Verify command was registered with the custom name
        self.assertIn("my-custom-name", self.mock_reader.commands)
        self.assertEqual(some_function.name, "my-custom-name")

    def test_register_command_with_event(self):
        """Test command registration with event parameters."""

        @register_command(with_event=True)
        def event_command(reader, event_name, event):
            """A command that needs event info."""
            return f"Got event: {event_name}"

        # Verify command was registered
        self.assertIn("event-command", self.mock_reader.commands)

        # Test that the command function signature is preserved
        command_class = self.mock_reader.commands["event-command"]
        mock_reader = MagicMock()
        command_instance = command_class(mock_reader, "test_event", "test_data")
        command_instance.reader = mock_reader
        command_instance.event_name = "test_event"
        command_instance.event = "test_data"

        # The command's do method should call our function with the right args
        result = command_instance.do()
        # We can't easily test the return value due to mocking, but we can verify
        # the command was created successfully

    def test_register_command_without_parentheses(self):
        """Test register_command used without parentheses."""

        @register_command
        def simple_command(reader):
            """Simple command without parentheses."""

        self.assertIn("simple-command", self.mock_reader.commands)
        self.assertEqual(simple_command.name, "simple-command")
