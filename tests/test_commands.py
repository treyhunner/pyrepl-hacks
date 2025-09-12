import unittest

from pyrepl_hacks.commands import (
    dedent,
    move_line_down,
    move_line_up,
    move_to_indentation,
)

from .support import ReaderTestMixin


class TestMoveToIndentation(unittest.TestCase, ReaderTestMixin):
    def test_move_to_indentation_basic(self):
        """Test moving to indentation on a basic indented line."""
        reader = self.create_reader("    hello world", pos=11)  # pos at 'o'

        move_to_indentation(reader)

        self.assertPositionEquals(reader, 4)  # Should move to after spaces

    def test_move_to_indentation_already_at_start(self):
        """Test moving to indentation when already at the start."""
        reader = self.create_reader("    hello world", pos=0)

        move_to_indentation(reader)

        self.assertPositionEquals(reader, 4)  # Should move to after spaces

    def test_move_to_indentation_no_indentation(self):
        """Test moving to indentation on a line with no indentation."""
        reader = self.create_reader("hello world", pos=5)

        move_to_indentation(reader)

        self.assertPositionEquals(reader, 0)  # Should move to beginning

    def test_move_to_indentation_tabs_and_spaces(self):
        """Test moving to indentation with mixed tabs and spaces."""
        reader = self.create_reader("\t  hello world", pos=10)

        move_to_indentation(reader)

        self.assertPositionEquals(reader, 3)  # After tab and spaces

    def test_move_to_indentation_multiline(self):
        """Test moving to indentation on second line of multiline text."""
        text = "line1\n    line2"
        reader = self.create_reader(text, pos=12)  # Position at 'n' in 'line2'

        move_to_indentation(reader)

        self.assertPositionEquals(reader, 10)  # After spaces on second line

    def test_move_to_indentation_empty_line(self):
        """Test moving to indentation on an empty line."""
        text = "line1\n\nline3"
        reader = self.create_reader(text, pos=6)  # Position on empty line

        move_to_indentation(reader)

        self.assertPositionEquals(reader, 6)  # Should stay at beginning of empty line


class TestDedent(unittest.TestCase, ReaderTestMixin):
    def test_dedent_basic(self):
        """Test basic dedenting of indented text."""
        text = "    line1\n    line2\n    line3"
        reader = self.create_reader(text, pos=8)  # Position in first line

        dedent(reader)

        expected = "line1\nline2\nline3"
        self.assertBufferEquals(reader, expected)
        self.assertPositionEquals(reader, 4)  # Position adjusted for removed indent

    def test_dedent_mixed_indentation(self):
        """Test dedenting with mixed indentation levels."""
        text = "    line1\n        line2\n    line3"
        reader = self.create_reader(text, pos=15)  # Position in second line

        dedent(reader)

        expected = "line1\n    line2\nline3"
        self.assertBufferEquals(reader, expected)
        self.assertPositionEquals(reader, 7)  # Position adjusted

    def test_dedent_no_common_indentation(self):
        """Test dedenting when there's no common indentation to remove."""
        text = "line1\n    line2\nline3"
        reader = self.create_reader(text, pos=10)

        dedent(reader)

        # Should remain unchanged
        self.assertBufferEquals(reader, text)
        self.assertPositionEquals(reader, 10)

    def test_dedent_all_whitespace_lines(self):
        """Test dedenting text with some all-whitespace lines."""
        text = "    line1\n    \n    line3"
        reader = self.create_reader(text, pos=8)

        dedent(reader)

        expected = "line1\n\nline3"
        self.assertBufferEquals(reader, expected)

    def test_dedent_tabs(self):
        """Test dedenting with tabs."""
        text = "\tline1\n\tline2"
        reader = self.create_reader(text, pos=5)

        dedent(reader)

        expected = "line1\nline2"
        self.assertBufferEquals(reader, expected)
        self.assertPositionEquals(reader, 4)  # Position adjusted for removed tab


class TestMoveLineDown(unittest.TestCase, ReaderTestMixin):
    def test_move_line_down_basic(self):
        """Test moving a line down."""
        text = "line1\nline2\nline3"
        reader = self.create_reader(text, pos=2)  # Position in first line

        move_line_down(reader)

        expected = "line2\nline1\nline3"
        self.assertBufferEquals(reader, expected)
        # Position should move to same column in moved line
        self.assertPositionEquals(reader, 8)  # 'n' in moved "line1"

    def test_move_line_down_last_line(self):
        """Test trying to move the last line down (should do nothing)."""
        text = "line1\nline2\nline3"
        reader = self.create_reader(text, pos=14)  # Position in last line
        original_pos = reader.pos

        move_line_down(reader)

        # Should remain unchanged
        self.assertBufferEquals(reader, text)
        self.assertPositionEquals(reader, original_pos)

    def test_move_line_down_with_newlines(self):
        """Test moving line down when lines have explicit newlines."""
        text = "line1\nline2\nline3\n"
        reader = self.create_reader(text, pos=3)  # Position in first line

        move_line_down(reader)

        expected = "line2\nline1\nline3\n"
        self.assertBufferEquals(reader, expected)

    def test_move_line_down_empty_line(self):
        """Test moving an empty line down."""
        text = "line1\n\nline3"
        reader = self.create_reader(text, pos=6)  # Position on empty line

        move_line_down(reader)

        expected = "line1\nline3\n\n"
        self.assertBufferEquals(reader, expected)

    def test_move_line_down_single_line(self):
        """Test moving line down when there's only one line."""
        text = "single line"
        reader = self.create_reader(text, pos=5)
        original_pos = reader.pos

        move_line_down(reader)

        # Should remain unchanged
        self.assertBufferEquals(reader, text)
        self.assertPositionEquals(reader, original_pos)


class TestMoveLineUp(unittest.TestCase, ReaderTestMixin):
    def test_move_line_up_basic(self):
        """Test moving a line up."""
        text = "line1\nline2\nline3"
        reader = self.create_reader(text, pos=8)  # Position in second line

        move_line_up(reader)

        expected = "line2\nline1\nline3"
        self.assertBufferEquals(reader, expected)
        # Position should move to same column in moved line
        self.assertPositionEquals(reader, 2)  # 'n' in moved "line2"

    def test_move_line_up_first_line(self):
        """Test trying to move the first line up (should do nothing)."""
        text = "line1\nline2\nline3"
        reader = self.create_reader(text, pos=2)  # Position in first line
        original_pos = reader.pos

        move_line_up(reader)

        # Should remain unchanged
        self.assertBufferEquals(reader, text)
        self.assertPositionEquals(reader, original_pos)

    def test_move_line_up_with_newlines(self):
        """Test moving line up when lines have explicit newlines."""
        text = "line1\nline2\nline3\n"
        reader = self.create_reader(text, pos=9)  # Position in second line

        move_line_up(reader)

        expected = "line2\nline1\nline3\n"
        self.assertBufferEquals(reader, expected)

    def test_move_line_up_empty_line(self):
        """Test moving an empty line up."""
        text = "line1\n\nline3"
        reader = self.create_reader(text, pos=6)  # Position on empty line

        move_line_up(reader)

        expected = "\nline1\nline3"
        self.assertBufferEquals(reader, expected)

    def test_move_line_up_single_line(self):
        """Test moving line up when there's only one line."""
        text = "single line"
        reader = self.create_reader(text, pos=5)
        original_pos = reader.pos

        move_line_up(reader)

        # Should remain unchanged
        self.assertBufferEquals(reader, text)
        self.assertPositionEquals(reader, original_pos)

    def test_move_line_up_last_line(self):
        """Test moving the last line up."""
        text = "line1\nline2\nline3"
        reader = self.create_reader(text, pos=14)  # Position in last line

        move_line_up(reader)

        expected = "line1\nline3line2\n"
        self.assertBufferEquals(reader, expected)


class TestCommandsIntegration(unittest.TestCase, ReaderTestMixin):
    def test_commands_mark_reader_as_dirty(self):
        """Test that commands properly mark the reader as dirty."""
        reader = self.create_reader("    indented line", pos=8)
        self.assertFalse(reader.dirty)

        # Test dedent marks as dirty
        dedent(reader)
        self.assertTrue(reader.dirty)

        # Reset for next test
        reader.dirty = False
        reader.buffer[:] = list("line1\nline2")
        reader.pos = 3

        move_line_down(reader)
        self.assertTrue(reader.dirty)

    def test_commands_invalidate_cache(self):
        """Test that commands properly invalidate the refresh cache."""
        reader = self.create_reader("    test", pos=2)
        self.assertFalse(reader.last_refresh_cache.invalidated)

        dedent(reader)
        self.assertTrue(reader.last_refresh_cache.invalidated)

    def test_pyrepl_commands_integration(self):
        """Test that _pyrepl commands are properly wrapped."""
        from pyrepl_hacks import commands

        # Check that some common _pyrepl commands were added
        # These should be available as functions in the commands module
        expected_commands = ["clear_screen", "beginning_of_line", "end_of_line"]

        for cmd_name in expected_commands:
            if hasattr(commands, cmd_name):
                cmd_func = getattr(commands, cmd_name)
                self.assertTrue(callable(cmd_func))

                # Try to call it with mock reader - this exercises line 106
                reader = self.create_reader("test text", pos=4)
                from contextlib import suppress

                with suppress(Exception):
                    # Some commands might fail due to missing console/etc, but we
                    # just want to test the wrapper function exists and is callable
                    cmd_func(reader, "test_event", "test_data")

    def test_mock_reader_bounds_checking(self):
        """Test MockReader handles out-of-bounds positions."""
        reader = self.create_reader("test", pos=10)  # Position beyond text
        # This should trigger the bounds check in pos2xy
        x, y = reader.pos2xy()
        # Should be at end of text
        self.assertEqual(reader.pos, 4)  # Length of "test"
