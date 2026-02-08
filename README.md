# TechDoc Transcriber

TechDoc Transcriber is an offline-first GUI tool that converts PDF documents into Markdown using the Docling library. Designed for secure BEL workflows, it bundles a CustomTkinter interface with Docling artifact management so translators can process files without a network connection once the models are downloaded.

## Getting Started

1. **Prepare the virtual environment**:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\activate  # Windows
   pip install -r config/requirements.txt
   ```
2. **Download the Docling artifacts** (required whenever the environment is bootstrapped):
   ```powershell
   python scripts/download_artifacts.py
   ```
   This populates `models/docling_artifacts`, which `DocumentModel` requires in offline mode.
3. **Run the application**:
   ```powershell
   start_app.bat
   ```
   The shortcut activates `.venv` (if present), installs dependencies, downloads artifacts, and launches `scripts/run_app.py`. The GUI exposes an **Enable RAG export** switch (above the status label) so you can decide whether each saved Markdown also creates a `_rag.md` companion.
4. **Run tests**:
   ```powershell
   python -m unittest discover
   ```
   The tests mock Docling internally but still require the package installed via `config/requirements.txt` so the imports resolve.

## Code Overview

- `src/techdoc_transcriber/`
  - `model.py`: Offline `DocumentModel` enforcing `HF_HUB_OFFLINE=1`, validating `models/docling_artifacts`, constructing `PdfPipelineOptions`, and exporting Docling-produced Markdown.
  - `view.py`: CustomTkinter `DocumentView` that lays out the window (title, status badge, Markdown textbox, developer footer) and exposes helpers for status updates and error dialogs.
  - `controller.py`: `DocumentController` wires the Select button, runs conversions on a worker thread, updates the view, and saves the Markdown through a dialog; when the toggle is on, it also builds a RAG-optimized file next to the same user-selected location.
  - `rag_formatter.py`: Builds a metadata-rich, sectioned Markdown string (with extracted facts and optional keywords) optimized for RAG/LLM ingestion.
- `scripts/run_app.py`: Entry point that injects `src/` into `sys.path`, configures logging, and instantiates the MVC components inside CustomTkinter while fallbacks to a hidden root for critical errors.
- `scripts/download_artifacts.py`: Downloads Docling models into `models/docling_artifacts` prior to conversion.
- `tests/`: Unit tests covering the offline model, GUI view, RAG formatter, and controller interactions (Docling/UI dependencies are mocked).

## Notes

- `.agent/rules/` contains `docling-offline.md`, `gui-threading.md`, and `python-standards.md`; consult those before changing Docling initialization or threading logic.
- Logs are written to `app.log` when diagnosing startup or conversion issues.
- `start_app.bat` is the recommended launcher because it orchestrates `.venv`, dependency installation, artifact download, and `scripts/run_app.py` execution in one command.
- After every save (when the toggle is on), a RAG-ready Markdown file named `<filename>_rag.md` appears in the same folder; consume that companion file in your RAG/LLM pipelines.
