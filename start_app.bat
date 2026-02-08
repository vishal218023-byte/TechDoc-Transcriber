@echo off
setlocal enabledelayedexpansion

if not exist "config\requirements.txt" (
    echo ERROR: Missing config\requirements.txt; please ensure dependencies are listed there.
    exit /b 1
)

if not exist ".venv\Scripts\activate" (
    echo Creating virtual environment...
    python -m venv .venv || (
        echo ERROR: Failed to create virtual environment.
        exit /b 1
    )
)

call ".venv\Scripts\activate"

echo Installing dependencies from config\requirements.txt...
pip install -r config\requirements.txt || (
    echo ERROR: Could not install dependencies.
    exit /b 1
)

if not exist "scripts\download_artifacts.py" (
    echo ERROR: scripts\download_artifacts.py is missing.
    exit /b 1
)

if not exist "models\docling_artifacts" (
    echo Docling artifacts not found; downloading now...
    python scripts/download_artifacts.py || (
        echo ERROR: Artifact download failed.
        exit /b 1
    )
) else (
    echo Docling artifacts already present; skipping download.
)

if not exist "scripts\run_app.py" (
    echo ERROR: scripts\run_app.py is missing.
    exit /b 1
)

echo Starting TechDoc Transcriber...
python scripts/run_app.py %*
