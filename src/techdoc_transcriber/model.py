import os
import logging
from pathlib import Path
from typing import Union

from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions

logger = logging.getLogger(__name__)


class DocumentModel:
    """Handles conversion of PDF documents to Markdown using Docling."""

    def __init__(self, artifacts_path: Union[str, Path] = "./models/docling_artifacts"):
        self.artifacts_path = Path(artifacts_path)
        os.environ["HF_HUB_OFFLINE"] = "1"

        if not self.artifacts_path.exists():
            message = f"Docling artifacts directory not found: {self.artifacts_path}"
            logger.error(message)
            raise FileNotFoundError(message)

        pipeline_options = PdfPipelineOptions(artifacts_path=self.artifacts_path)
        format_options = {
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
        }

        try:
            self.converter = DocumentConverter(format_options=format_options)
            logger.info("Initialized DocumentConverter in offline mode.")
        except Exception as exc:
            logger.error(f"Failed to initialize DocumentConverter: {exc}")
            raise

    def convert_to_markdown(self, file_path: Union[str, Path]) -> str:
        file_path = Path(file_path)
        if not file_path.exists():
            message = f"Input file not found: {file_path}"
            logger.error(message)
            raise FileNotFoundError(message)

        logger.info("Starting document conversion: %s", file_path)
        result = self.converter.convert(str(file_path))
        markdown = result.document.export_to_markdown()
        logger.info("Conversion succeeded for %s", file_path)
        return markdown
