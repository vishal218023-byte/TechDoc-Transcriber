import os
import logging
from typing import Optional
from pathlib import Path
from docling.document_converter import DocumentConverter, PdfFormatOption
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.datamodel.base_models import InputFormat

# Setup logging according to standards
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class DocumentModel:
    """Handles the document conversion logic using Docling in offline mode.
    
    Attributes:
        artifacts_path (str): Path to the local Docling artifacts.
        converter (DocumentConverter): The Docling document converter instance.
    """

    def __init__(self, artifacts_path: str = "./models/docling_artifacts"):
        """Initializes the DocumentModel with offline configuration.
        
        Args:
            artifacts_path (str): Path to the local Docling artifacts.
            
        Raises:
            FileNotFoundError: If the artifacts_path does not exist.
        """
        self.artifacts_path = artifacts_path
        
        # Rule: Set HF_HUB_OFFLINE = 1
        os.environ["HF_HUB_OFFLINE"] = "1"
        
        # Rule: Verify artifacts_path exists
        if not os.path.exists(self.artifacts_path):
            error_msg = f"Docling artifacts directory not found: {self.artifacts_path}"
            logging.error(error_msg)
            raise FileNotFoundError(error_msg)
            
        try:
            # Rule: Configure PdfPipelineOptions with artifacts_path
            pipeline_options = PdfPipelineOptions(artifacts_path=Path(self.artifacts_path))
            format_options = {
                InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
            }
            self.converter = DocumentConverter(format_options=format_options)
            logging.info("DocumentConverter initialized successfully in offline mode.")
        except Exception as e:
            logging.error(f"Failed to initialize DocumentConverter: {e}")
            raise

    def convert_to_markdown(self, file_path: str) -> str:
        """Converts a document to Markdown.
        
        Args:
            file_path (str): path to the document file.
            
        Returns:
            str: The exported markdown content.
            
        Raises:
            FileNotFoundError: If the input file does not exist.
            Exception: If any error occurs during conversion.
        """
        if not os.path.exists(file_path):
            error_msg = f"Input file not found: {file_path}"
            logging.error(error_msg)
            raise FileNotFoundError(error_msg)
            
        try:
            logging.info(f"Starting conversion for: {file_path}")
            result = self.converter.convert(file_path)
            md_content = result.document.export_to_markdown()
            logging.info(f"Conversion successful for: {file_path}")
            return md_content
        except Exception as e:
            logging.error(f"Error during conversion of {file_path}: {e}")
            raise

import customtkinter as ctk
from tkinter import filedialog, messagebox
import threading

class DocumentView(ctk.CTk):
    """The GUI View for TechDoc Transcriber using CustomTkinter."""

    def __init__(self):
        super().__init__()
        self.title("TechDoc Transcriber - BEL")
        self.geometry("600x400")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=0) # Developer info row

        self.label = ctk.CTkLabel(self, text="Convert Documents to Markdown (Offline)", font=("Arial", 20, "bold"))
        self.label.grid(row=0, column=0, padx=20, pady=20)

        self.select_button = ctk.CTkButton(self, text="Select Document (PDF)", command=None) # Set by Controller
        self.select_button.grid(row=1, column=0, padx=20, pady=10)

        self.status_label = ctk.CTkLabel(self, text="Ready", text_color="gray")
        self.status_label.grid(row=2, column=0, padx=20, pady=5)

        self.textbox = ctk.CTkTextbox(self)
        self.textbox.grid(row=3, column=0, padx=20, pady=(10, 5), sticky="nsew")

        self.developer_info_label = ctk.CTkLabel(
            self, 
            text="Developed By: Vishal Raj V, E218023 - T&PS/SS/NS-1", 
            font=("Arial", 10), 
            text_color="gray"
        )
        self.developer_info_label.grid(row=4, column=0, padx=20, pady=(0, 10), sticky="e")

    def show_error(self, message: str):
        """Shows an error message box."""
        messagebox.showerror("Error", message)

    def update_status(self, text: str, color: str = "gray"):
        """Updates the status label."""
        self.status_label.configure(text=text, text_color=color)

    def set_markdown_content(self, content: str):
        """Displays the converted markdown content."""
        self.textbox.delete("1.0", "end")
        self.textbox.insert("1.0", content)


class DocumentController:
    """The Controller that bridges Model and View."""

    def __init__(self, model: DocumentModel, view: DocumentView):
        self.model = model
        self.view = view
        self.view.select_button.configure(command=self.handle_select_file)

    def handle_select_file(self):
        """Handles the file selection and starts conversion in a background thread."""
        file_path = filedialog.askopenfilename(
            filetypes=[("PDF files", "*.pdf"), ("All files", "*.*")]
        )
        if not file_path:
            return

        self.view.update_status("Converting...", "yellow")
        self.view.select_button.configure(state="disabled")
        
        # Start conversion in worker thread
        thread = threading.Thread(target=self.run_conversion, args=(file_path,), daemon=True)
        thread.start()

    def run_conversion(self, file_path: str):
        """Runs the conversion in a background thread and updates the UI safely."""
        try:
            markdown_content = self.model.convert_to_markdown(file_path)
            # Safe UI update
            self.view.after(0, lambda: self.on_conversion_success(markdown_content))
        except Exception as e:
            self.view.after(0, lambda: self.on_conversion_error(str(e)))

    def on_conversion_success(self, content: str):
        """Success callback on the main thread."""
        self.view.set_markdown_content(content)
        self.view.update_status("Success", "green")
        self.view.select_button.configure(state="normal")
        # Automatically offer to save
        self.save_markdown(content)

    def on_conversion_error(self, error_msg: str):
        """Error callback on the main thread."""
        self.view.update_status("Error", "red")
        self.view.select_button.configure(state="normal")
        self.view.show_error(f"Conversion failed:\n{error_msg}")

    def save_markdown(self, content: str):
        """Offers to save the markdown content."""
        save_path = filedialog.asksaveasfilename(
            defaultextension=".md",
            filetypes=[("Markdown files", "*.md")]
        )
        if save_path:
            try:
                with open(save_path, "w", encoding="utf-8") as f:
                    f.write(content)
                messagebox.showinfo("Saved", f"File saved to {save_path}")
            except Exception as e:
                self.view.show_error(f"Save failed: {e}")


if __name__ == "__main__":
    # Ensure offline mode environment variable is set as early as possible
    os.environ["HF_HUB_OFFLINE"] = "1"
    
    try:
        app_model = DocumentModel()
        app_view = DocumentView()
        app_controller = DocumentController(app_model, app_view)
        app_view.mainloop()
    except Exception as e:
        # High level catch for initialization errors
        logging.critical(f"Application crashed during startup: {e}")
        # Need a separate root if view wasn't created
        root = ctk.CTk()
        root.withdraw()
        messagebox.showerror("Critical Error", f"Application failed to start:\n{e}")
        root.destroy()
