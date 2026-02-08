import logging
import threading
from datetime import datetime
from pathlib import Path
from tkinter import filedialog, messagebox
from typing import TYPE_CHECKING

from techdoc_transcriber.rag_formatter import build_rag_document

if TYPE_CHECKING:
    from techdoc_transcriber.model import DocumentModel
    from techdoc_transcriber.view import DocumentView

if TYPE_CHECKING:
    from techdoc_transcriber.model import DocumentModel

logger = logging.getLogger(__name__)


class DocumentController:
    """Controller orchestrating the model and view interactions."""

    def __init__(self, model: "DocumentModel", view: "DocumentView"):
        self.model = model
        self.view = view
        self.view.select_button.configure(command=self.handle_select_file)

    def handle_select_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if not file_path:
            return

        self.view.update_status("Converting...", "yellow")
        self.view.select_button.configure(state="disabled")

        thread = threading.Thread(
            target=self.run_conversion,
            args=(file_path,),
            daemon=True,
        )
        thread.start()

    def run_conversion(self, file_path: str):
        try:
            markdown_content = self.model.convert_to_markdown(file_path)
            self.view.after(0, lambda: self.on_conversion_success(markdown_content))
        except Exception as exc:
            self.view.after(0, lambda: self.on_conversion_error(str(exc)))

    def on_conversion_success(self, content: str):
        self.view.set_markdown_content(content)
        self.view.update_status("Success", "green")
        self.view.select_button.configure(state="normal")
        # Automatically offer to save the primary Markdown
        self.save_markdown(content)

    def on_conversion_error(self, error_msg: str):
        self.view.update_status("Error", "red")
        self.view.select_button.configure(state="normal")
        self.view.show_error(f"Conversion failed:\n{error_msg}")

    def save_markdown(self, content: str):
        save_path = filedialog.asksaveasfilename(
            defaultextension=".md",
            filetypes=[("Markdown files", "*.md")],
        )
        if not save_path:
            return

        try:
            with open(save_path, "w", encoding="utf-8") as out_file:
                out_file.write(content)
            messagebox.showinfo("Saved", f"File saved to {save_path}")
            if self.view.is_rag_enabled():
                self.save_rag_markdown(content, save_path)
        except Exception as exc:
            self.view.show_error(f"Save failed: {exc}")

    def save_rag_markdown(self, content: str, save_path: str):
        """Auto-export a RAG-friendly Markdown file beside the saved Markdown."""
        target = Path(save_path)
        output_path = target.with_name(f"{target.stem}_rag.md")

        try:
            rag_document = build_rag_document(
                text=content,
                source_name=target.name,
                generated_at=datetime.utcnow(),
            )
            output_path.write_text(rag_document, encoding="utf-8")
            messagebox.showinfo(
                "RAG Exported", f"RAG-ready Markdown saved to {output_path}"
            )
        except Exception as exc:
            logger.error("Failed to emit RAG document for %s: %s", save_path, exc)
            self.view.show_error(f"RAG export failed:\n{exc}")
