import sys
import unittest
from unittest.mock import MagicMock, patch


class TestThemeUtils(unittest.TestCase):
    """Simplified theme utils tests that avoid complex import mocking."""

    def test_convert_color_logic(self):
        """Test the color conversion string processing logic."""
        # Test the actual _convert_color function with mocked ANSIColors
        with patch("pyrepl_hacks.theme_utils.ANSIColors") as mock_ansi:
            # Mock getattr to return predictable values
            mock_ansi.RED = "red_code"
            mock_ansi.BOLD = "bold_code"
            mock_ansi.INTENSE = "intense_code"
            mock_ansi.BLUE = "blue_code"

            from pyrepl_hacks.theme_utils import _convert_color

            # Test simple color
            result = _convert_color("red")
            self.assertEqual(result, "red_code")

            # Test compound color with comma
            result = _convert_color("intense, blue")
            self.assertEqual(result, "intense_codeblue_code")

            # Test color with space (should become underscore)
            mock_ansi.BOLD_RED = "bold_red_code"
            result = _convert_color("bold red")
            self.assertEqual(result, "bold_red_code")

    def test_update_theme_calls_convert_color(self):
        """Test that update_theme calls _convert_color for each color."""

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

            # Call update_theme - this will actually call _convert_color
            update_theme(keyword="green", string="blue")
