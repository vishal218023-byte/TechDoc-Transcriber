import os
import unittest
from unittest.mock import MagicMock, patch

from techdoc_transcriber.model import DocumentModel


class TestDocumentModel(unittest.TestCase):
    """Verify offline document conversion plumbing."""

    @patch("techdoc_transcriber.model.Path.exists")
    @patch("techdoc_transcriber.model.DocumentConverter")
    def test_model_initialization_offline(self, mock_converter, mock_exists):
        mock_exists.return_value = True

        model = DocumentModel()

        self.assertEqual(os.environ.get("HF_HUB_OFFLINE"), "1")
        mock_converter.assert_called_once()

    @patch("techdoc_transcriber.model.Path.exists")
    @patch("techdoc_transcriber.model.DocumentConverter")
    def test_model_initialization_fails_if_no_artifacts(self, mock_converter, mock_exists):
        mock_exists.return_value = False

        with self.assertRaises(FileNotFoundError):
            DocumentModel()

        mock_converter.assert_not_called()

    @patch("techdoc_transcriber.model.Path.exists")
    @patch("techdoc_transcriber.model.DocumentConverter")
    def test_conversion_success(self, mock_converter, mock_exists):
        mock_exists.side_effect = [True, True]
        converter_instance = mock_converter.return_value
        mock_result = MagicMock()
        mock_result.document.export_to_markdown.return_value = "# Test Content"
        converter_instance.convert.return_value = mock_result

        model = DocumentModel()
        result = model.convert_to_markdown("test.pdf")

        self.assertEqual(result, "# Test Content")
        converter_instance.convert.assert_called_with("test.pdf")
