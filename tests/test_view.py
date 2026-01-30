import unittest
import customtkinter as ctk
from main import DocumentView

class TestDocumentView(unittest.TestCase):
    """Unit tests for DocumentView following TDD."""

    def setUp(self):
        # We need a root to test CustomTkinter widgets
        # However, initializing CTk might open a window which we should ideally avoid in CI
        # But for simple property checks it might be okay.
        self.view = DocumentView()
        self.view.withdraw() # Hide window during test

    def tearDown(self):
        self.view.destroy()

    def test_developer_info_label_exists(self):
        """Test that the developer info label is present in the view."""
        # This should fail initially as the attribute developer_info_label is not yet defined
        self.assertTrue(hasattr(self.view, "developer_info_label"), "Developer info label is missing")
        self.assertIsInstance(self.view.developer_info_label, ctk.CTkLabel)
        self.assertIn("Vishal Raj V", self.view.developer_info_label.cget("text"))

if __name__ == '__main__':
    unittest.main()
