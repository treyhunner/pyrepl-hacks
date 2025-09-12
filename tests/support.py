"""Test utilities for pyrepl-hacks tests."""

from unittest.mock import MagicMock


class MockReader:
    """Mock reader that simulates the _pyrepl reader interface."""

    def __init__(self, initial_text="", pos=None):
        self.buffer = list(initial_text)
        self.pos = len(initial_text) if pos is None else pos
        self.dirty = False

        # Mock the refresh cache
        self.last_refresh_cache = MagicMock()
        self.last_refresh_cache.invalidated = False

        # Store original state for assertions
        self._initial_text = initial_text

    def get_unicode(self):
        """Get the current buffer content as a string."""
        return "".join(self.buffer)

    def pos2xy(self):
        """Convert position to (x, y) coordinates."""
        text = self.get_unicode()
        if self.pos > len(text):
            self.pos = len(text)

        text_to_pos = text[: self.pos]
        lines = text_to_pos.split("\n")

        y = len(lines) - 1
        x = len(lines[y])

        return (x, y)

    def bol(self):
        """Find beginning of current line position."""
        text = self.get_unicode()[: self.pos]
        last_newline = text.rfind("\n")
        return last_newline + 1


def assert_buffer_equals(test_case, reader, expected_text):
    """Assert that the reader's buffer contains the expected text."""
    actual = reader.get_unicode()
    test_case.assertEqual(
        actual,
        expected_text,
        f"Expected buffer: {expected_text!r}, got: {actual!r}",
    )


def assert_position_equals(test_case, reader, expected_pos):
    """Assert that the reader's position is as expected."""
    test_case.assertEqual(
        reader.pos,
        expected_pos,
        f"Expected position: {expected_pos}, got: {reader.pos}",
    )


class ReaderTestMixin:
    """Mixin class providing common reader test utilities."""

    def create_reader(self, text="", pos=None):
        """Create a MockReader for testing."""
        return MockReader(text, pos)

    def assertBufferEquals(self, reader, expected_text):
        """Assert that the reader's buffer contains the expected text."""
        assert_buffer_equals(self, reader, expected_text)

    def assertPositionEquals(self, reader, expected_pos):
        """Assert that the reader's position is as expected."""
        assert_position_equals(self, reader, expected_pos)
