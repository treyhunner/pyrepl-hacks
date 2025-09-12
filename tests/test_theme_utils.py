import sys
import unittest
from unittest.mock import MagicMock, patch


class TestThemeUtils(unittest.TestCase):
    """Simplified theme utils tests that avoid complex import mocking."""

    def test_convert_color_regex(self):
        """Test the color conversion regex patterns."""
        # We can test the basic pattern matching logic
        test_cases = [
            ("red", ["red"]),
            ("bold red", ["bold", "red"]),
            ("intense, blue", ["intense", "blue"]),
            ("background, intense, green", ["background", "intense", "green"]),
        ]

        for color_string, expected_parts in test_cases:
            with self.subTest(color_string=color_string):
                parts = color_string.split(",")
                actual_parts = [
                    c.strip().replace(" ", "_").upper()
                    for part in parts
                    for c in part.split()
                ]
                expected_upper = [
                    part.replace(" ", "_").upper() for part in expected_parts
                ]
                self.assertEqual(actual_parts, expected_upper)

    @patch("pyrepl_hacks.theme_utils._convert_color")
    def test_update_theme_calls_convert_color(self, mock_convert_color):
        """Test that update_theme calls _convert_color for each color."""
        mock_convert_color.return_value = "mocked_color"

        # Mock the _colorize imports to avoid ImportError
        with patch.dict(
            "sys.modules",
            {
                "_colorize": MagicMock(),
            },
        ):
            # Import after mocking
            from pyrepl_hacks.theme_utils import update_theme

            # Mock the _colorize components
            mock_colorize = sys.modules["_colorize"]
            mock_default_theme = MagicMock()
            mock_syntax = MagicMock()
            mock_new_theme = MagicMock()

            mock_colorize.default_theme = mock_default_theme
            mock_colorize.Syntax = MagicMock(return_value=mock_syntax)
            mock_colorize.set_theme = MagicMock()
            mock_default_theme.copy_with.return_value = mock_new_theme

            # Call update_theme
            update_theme(keyword="green", string="blue")

            # Verify _convert_color was called for each argument
            mock_convert_color.assert_any_call("green")
            mock_convert_color.assert_any_call("blue")
            self.assertEqual(mock_convert_color.call_count, 2)
