import tempfile
from pathlib import Path
from unittest import TestCase
from unittest.mock import MagicMock, patch

from techdoc_transcriber.controller import DocumentController


class DummyView:
    def __init__(self, rag_enabled=True):
        self.select_button = MagicMock()
        self._rag_enabled = rag_enabled
        self._last_error = None

    def is_rag_enabled(self):
        return self._rag_enabled

    def show_error(self, message: str):
        self._last_error = message


class TestDocumentController(TestCase):
    def setUp(self):
        self.model = MagicMock()
        self.view = DummyView(rag_enabled=True)
        self.controller = DocumentController(model=self.model, view=self.view)

    @patch("tkinter.messagebox.showinfo")
    @patch("techdoc_transcriber.controller.filedialog.asksaveasfilename")
    @patch("techdoc_transcriber.controller.build_rag_document")
    def test_save_markdown_also_writes_rag(self, mock_build, mock_dialog, mock_showinfo):
        mock_build.return_value = "rag content"
        with tempfile.TemporaryDirectory() as tmp_dir:
            save_path = Path(tmp_dir) / "document.md"
            mock_dialog.return_value = str(save_path)

            self.controller.save_markdown("converted content")

            self.assertTrue(save_path.exists())
            self.assertEqual(save_path.read_text(encoding="utf-8"), "converted content")

            rag_path = save_path.with_name(f"{save_path.stem}_rag.md")
            self.assertTrue(rag_path.exists())
            self.assertEqual(rag_path.read_text(encoding="utf-8"), "rag content")

        mock_build.assert_called_once()

    @patch("tkinter.messagebox.showinfo")
    @patch("techdoc_transcriber.controller.filedialog.asksaveasfilename")
    @patch("techdoc_transcriber.controller.build_rag_document")
    def test_save_markdown_skips_rag_when_disabled(
        self, mock_build, mock_dialog, mock_showinfo
    ):
        self.view._rag_enabled = False
        with tempfile.TemporaryDirectory() as tmp_dir:
            save_path = Path(tmp_dir) / "doc.md"
            mock_dialog.return_value = str(save_path)

            self.controller.save_markdown("content")

            self.assertTrue(save_path.exists())
            self.assertFalse(save_path.with_name(f"{save_path.stem}_rag.md").exists())

        mock_build.assert_not_called()
