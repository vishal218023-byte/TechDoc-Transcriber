import unittest
from datetime import datetime
from techdoc_transcriber.rag_formatter import build_rag_document


class TestRagFormatter(unittest.TestCase):
    def test_metadata_header_includes_source_and_timestamp(self):
        timestamp = datetime(2024, 1, 1, 12, 0)
        result = build_rag_document("# Title\nDetail line", "doc.pdf", generated_at=timestamp)
        self.assertTrue(result.startswith("---\nsource: doc.pdf"))
        self.assertIn("generated_at: 2024-01-01T12:00:00Z", result)

    def test_sections_follow_heading_order(self):
        markdown = "# Alpha\nFirst line\n## Beta\nSecond section"
        result = build_rag_document(markdown, "sample.pdf")
        alpha_index = result.index("## Alpha")
        beta_index = result.index("### Beta")
        self.assertLess(alpha_index, beta_index)

    def test_empty_content_yields_overview_section(self):
        result = build_rag_document("", "ghost.pdf")
        self.assertIn("## Overview", result)
        self.assertIn("No extracted content", result)
