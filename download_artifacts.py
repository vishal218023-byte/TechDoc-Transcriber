import os
from pathlib import Path
from docling.utils.model_downloader import download_models

# Use pathlib.Path for compatibility with Docling's internal logic
ARTIFACT_DIR = Path(os.getcwd()) / "models" / "docling_artifacts"

if __name__ == "__main__":
    print(f"Downloading models to: {ARTIFACT_DIR.absolute()}...")
    
    # Ensure the parent directory exists manually just in case
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    
    # Pass the Path object, not a string
    download_models(output_dir=ARTIFACT_DIR)
    
    print("\nDone! All models are stored locally for offline BEL use.")