# TechDoc Transcriber

TechDoc Transcriber is a GUI-based tool designed to convert technical documents (specifically PDFs) into Markdown format. It leverages the **Docling** library and is configured to run entirely **offline**, making it suitable for secure environments.

## Features

- **Offline Conversion**: No internet connection required for document processing.
- **Markdown Export**: Converts complex PDFs into clean, structured Markdown.
- **GUI Interface**: Simple and intuitive interface built with CustomTkinter.
- **Secure**: Data stays on your local machine.

## Prerequisites

- Python 3.10+
- [Docling](https://github.com/DS4SD/docling)
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)

## Installation

1. Clone the repository (if applicable) or copy the source files.
2. Create a virtual environment:
   ```bash
   python -m venv .venv
   ```
3. Activate the virtual environment:
   - Windows: `.\.venv\Scripts\activate`
   - Linux/macOS: `source .venv/bin/activate`
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. **Download Models (Internet required for this step only)**:
   Since the application is designed for offline use, you must first download the required AI models to your local machine:
   ```bash
   python download_artifacts.py
   ```
   This will store the models in `./models/docling_artifacts`.

6. **Verify Artifacts**: Ensure the directory `./models/docling_artifacts` is populated before running the main application.

## Usage

Run the application:
```bash
python main.py
```

1. Click **Select Document (PDF)** to choose a file.
2. Wait for the conversion to complete (status will show "Converting...").
3. View the generated Markdown in the text box.
4. Save the Markdown file when prompted.

## Developer Info

Developed By: Vishal Raj V, E218023 - T&PS/SS/NS-1

## License

Internal Use Only - Bharat Electronics Limited (BEL)
