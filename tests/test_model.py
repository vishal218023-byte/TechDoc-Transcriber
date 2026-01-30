import unittest
from unittest.mock import MagicMock, patch
import os
from main import DocumentModel

class TestDocumentModel(unittest.TestCase):
    """Unit tests for DocumentModel following TDD and Python standards."""

    def setUp(self):
        self.artifacts_path = "./models/docling_artifacts"
        # Ensure we don't actually try to touch the real disk if possible, 
        # or at least handle existence checks.
        
    @patch('main.os.path.exists')
    @patch('main.DocumentConverter')
    def test_model_initialization_offline(self, mock_converter, mock_exists):
        """Test that DocumentModel initializes correctly with offline settings."""
        mock_exists.return_value = True
        
        model = DocumentModel(artifacts_path=self.artifacts_path)
        
        # Verify HF_HUB_OFFLINE is set in the model's initialization or entry point
        self.assertEqual(os.environ.get("HF_HUB_OFFLINE"), "1")
        mock_converter.assert_called_once()
        
    @patch('main.os.path.exists')
    @patch('main.DocumentConverter')
    def test_model_initialization_fails_if_no_artifacts(self, mock_converter, mock_exists):
        """Test that Model raises an error if artifacts are missing."""
        mock_exists.return_value = False
        
        with self.assertRaises(FileNotFoundError):
            DocumentModel(artifacts_path=self.artifacts_path)

    @patch('main.os.path.exists')
    @patch('main.DocumentConverter')
    def test_conversion_success(self, mock_converter, mock_exists):
        """Test successful conversion logic."""
        mock_exists.return_value = True
        mock_instance = mock_converter.return_value
        mock_result = MagicMock()
        mock_result.document.export_to_markdown.return_value = "# Test Content"
        mock_instance.convert.return_value = mock_result
        
        model = DocumentModel(artifacts_path=self.artifacts_path)
        result = model.convert_to_markdown("test.pdf")
        
        self.assertEqual(result, "# Test Content")
        mock_instance.convert.assert_called_with("test.pdf")

if __name__ == '__main__':
    unittest.main()
