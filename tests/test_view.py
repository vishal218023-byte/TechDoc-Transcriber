import unittest
import customtkinter as ctk

from techdoc_transcriber.view import DocumentView


class TestDocumentView(unittest.TestCase):
    """Basic sanity checks for the GUI layout."""

    def setUp(self):
        self.view = DocumentView()
        self.view.withdraw()

    def tearDown(self):
        self.view.destroy()

    def test_developer_info_label_exists(self):
        self.assertTrue(hasattr(self.view, "developer_info_label"))
        self.assertIsInstance(self.view.developer_info_label, ctk.CTkLabel)
        self.assertIn("Vishal Raj V", self.view.developer_info_label.cget("text"))
