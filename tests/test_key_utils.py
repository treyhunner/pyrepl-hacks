import unittest
from pyrepl_hacks.key_utils import to_keyspec, slugify, SPECIAL_CASES


class TestSlugify(unittest.TestCase):
    def test_simple_keybinding(self):
        """Test slugifying simple keybindings."""
        self.assertEqual(slugify("Ctrl+A"), "_Ctrl_A")
        self.assertEqual(slugify("Alt+M"), "_Alt_M")
        self.assertEqual(slugify("F4"), "_F4")

    def test_complex_keybinding(self):
        """Test slugifying complex keybindings."""
        self.assertEqual(slugify("Ctrl+Alt+A"), "_Ctrl_Alt_A")
        self.assertEqual(slugify("Shift+Tab"), "_Shift_Tab")
        self.assertEqual(slugify("Ctrl+X Ctrl+R"), "_Ctrl_X_Ctrl_R")

    def test_special_characters(self):
        """Test handling of special characters in keybindings."""
        self.assertEqual(slugify("Alt+Up"), "_Alt_Up")
        self.assertEqual(slugify("Page Up"), "_Page_Up")
        self.assertEqual(slugify("Ctrl+/"), "_Ctrl__")

    def test_mixed_case(self):
        """Test that slugify handles mixed case properly."""
        self.assertEqual(slugify("ctrl+a"), "_ctrl_a")
        self.assertEqual(slugify("SHIFT+HOME"), "_SHIFT_HOME")
        self.assertEqual(slugify("Alt+PgDn"), "_Alt_PgDn")


class TestToKeyspec(unittest.TestCase):
    def test_ctrl_combinations(self):
        """Test Ctrl key combinations."""
        self.assertEqual(to_keyspec("Ctrl+A"), r"\C-a")
        self.assertEqual(to_keyspec("Ctrl+X"), r"\C-x")
        self.assertEqual(to_keyspec("ctrl+z"), r"\C-z")

    def test_alt_combinations(self):
        """Test Alt key combinations."""
        self.assertEqual(to_keyspec("Alt+M"), r"\M-m")
        self.assertEqual(to_keyspec("Alt+A"), r"\M-a")
        self.assertEqual(to_keyspec("alt+x"), r"\M-x")

    def test_function_keys(self):
        """Test function keys."""
        self.assertEqual(to_keyspec("F4"), r"\<f4>")
        self.assertEqual(to_keyspec("F10"), r"\<f10>")

    def test_arrow_keys(self):
        """Test arrow keys."""
        self.assertEqual(to_keyspec("Up"), r"\<up>")
        self.assertEqual(to_keyspec("Down"), r"\<down>")
        self.assertEqual(to_keyspec("Left"), r"\<left>")
        self.assertEqual(to_keyspec("Right"), r"\<right>")

    def test_page_keys(self):
        """Test page up/down keys."""
        self.assertEqual(to_keyspec("PgUp"), r"\<page up>")
        self.assertEqual(to_keyspec("PgDn"), r"\<page down>")
        self.assertEqual(to_keyspec("PageUp"), r"\<pageup>")
        self.assertEqual(to_keyspec("PageDown"), r"\<pagedown>")

    def test_special_cases(self):
        """Test special key combinations that have custom escape sequences."""
        # Test all special cases from SPECIAL_CASES
        for key_combo, expected_spec in SPECIAL_CASES.items():
            with self.subTest(key_combo=key_combo):
                self.assertEqual(to_keyspec(key_combo), expected_spec)

    def test_special_case_normalization(self):
        """Test that special cases work with different capitalization."""
        self.assertEqual(to_keyspec("ALT+UP"), r"\e[1;3A")
        self.assertEqual(to_keyspec("Shift+Tab"), r"\e[Z")
        self.assertEqual(to_keyspec("shift+home"), r"\e[1;2H")

    def test_multi_key_sequences(self):
        """Test multi-key sequences like Ctrl+X Ctrl+R."""
        self.assertEqual(to_keyspec("Ctrl+X Ctrl+R"), r"\C-x\C-r")
        self.assertEqual(to_keyspec("Alt+A Alt+B"), r"\M-a\M-b")

    def test_single_characters(self):
        """Test single character keys."""
        self.assertEqual(to_keyspec("a"), "a")
        self.assertEqual(to_keyspec("A"), "a")  # Should be normalized to lowercase
        self.assertEqual(to_keyspec("1"), "1")
        self.assertEqual(to_keyspec("Space"), r"\<space>")

    def test_home_end_keys(self):
        """Test Home and End keys."""
        self.assertEqual(to_keyspec("Home"), r"\<home>")
        self.assertEqual(to_keyspec("End"), r"\<end>")

    def test_insert_delete_keys(self):
        """Test Insert and Delete keys."""
        self.assertEqual(to_keyspec("Insert"), r"\<insert>")
        self.assertEqual(to_keyspec("Delete"), r"\<delete>")

    def test_whitespace_handling(self):
        """Test that whitespace is properly handled."""
        self.assertEqual(to_keyspec("  Ctrl+A  "), r"\C-a")
        self.assertEqual(to_keyspec("Alt+M "), r"\M-m")

    def test_complex_combinations(self):
        """Test complex key combinations."""
        # Test combinations that don't have special cases
        self.assertEqual(to_keyspec("Ctrl+Alt+A"), r"\C-\M-a")
        self.assertEqual(to_keyspec("Ctrl+F1"), r"\C-\<f1>")
