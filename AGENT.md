# TechDoc Transcriber Agent Notes

## Command quick reference
- `start_app.bat`: sets up `.venv`, installs `config/requirements.txt`, downloads the Docling artifacts, and launches `scripts/run_app.py` in a single command (Windows entry point).
- `python scripts/download_artifacts.py`: refreshes `models/docling_artifacts` if you already have an activated environment.
- `pip install -r config/requirements.txt` (after activating `.venv`): installs `docling`/`customtkinter` for development and tests.
- `python -m unittest discover`: run the regression suite (model/view + new RAG formatter/controller tests).
- `python -m unittest tests.test_rag_formatter.TestRagFormatter`: ensure the RAG formatter emits metadata and preserves heading order.
- `python -m unittest tests.test_controller`: confirm the controller saves the `_rag.md` companion next to the user-chosen Markdown output (toggle-aware).

## Architecture snapshot
- `src/techdoc_transcriber/model.py`: Offline `DocumentModel` that enforces `HF_HUB_OFFLINE=1`, validates `models/docling_artifacts`, builds `PdfPipelineOptions`, and exports Docling-generated Markdown.
- `src/techdoc_transcriber/view.py`: CustomTkinter `DocumentView` that lays out the GUI (title, status label, Markdown textbox, developer credit) and exposes helpers for status updates and errors.
- `src/techdoc_transcriber/controller.py`: `DocumentController` wires the Select button, runs conversions on a worker thread, updates the view, and saves the Markdown via the user’s save dialog; when the **Enable RAG export** toggle is active, it also writes the `_rag.md` companion beside the saved file.
- `src/techdoc_transcriber/rag_formatter.py`: Builds a metadata-rich, sectioned Markdown string optimized for RAG/LLM ingestion, surfacing extracted facts and respecting optional keywords.
- `scripts/run_app.py`: Entry script that injects `src/` into `sys.path`, configures logging, and creates the MVC trio inside CustomTkinter while preserving a fallback hidden root for startup errors.
- `scripts/download_artifacts.py`: Downloads Docling models into `models/docling_artifacts` prior to any conversion.
- `tests/`: Unit tests for the offline model, GUI view, RAG formatter, and controller interactions (Docling/UI dependencies mocked).

## Notes for future agents
- The application is strictly offline-first; make sure `models/docling_artifacts` exists and `HF_HUB_OFFLINE` stays set. Do not download models at runtime without explicit instruction.
- When the GUI toggle is on, a RAG-ready Markdown file named `<filename>_rag.md` is saved alongside the same folder where users save their Markdown; pass that companion to downstream RAG/LLM systems.
- The `.agent/rules/` folder still holds `docling-offline.md`, `gui-threading.md`, and `python-standards.md`; consult them before adjusting Docling initialization or threading logic.
- Check `app.log` when debugging startup or conversion issues.
