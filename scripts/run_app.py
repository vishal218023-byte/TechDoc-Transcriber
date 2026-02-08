import logging
import os
import sys
from pathlib import Path

import customtkinter as ctk
from tkinter import messagebox

root_dir = Path(__file__).resolve().parent.parent
src_dir = root_dir / "src"
if src_dir.exists():
    sys.path.insert(0, str(src_dir))

from techdoc_transcriber.controller import DocumentController
from techdoc_transcriber.model import DocumentModel
from techdoc_transcriber.view import DocumentView

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

if __name__ == "__main__":
    os.environ["HF_HUB_OFFLINE"] = "1"

    try:
        model = DocumentModel()
        view = DocumentView()
        DocumentController(model=model, view=view)
        view.mainloop()
    except Exception as exc:
        logging.critical("Application crashed during startup: %s", exc)
        fallback = ctk.CTk()
        fallback.withdraw()
        messagebox.showerror("Critical Error", f"Application failed to start:\n{exc}")
        fallback.destroy()
