# AGENTS.md - System Instructions

## Project Identity
**Name:** TechDoc Transcriber  
**Lead Architect:** Vishal Raj V, E218023
**Designation of Architect:** Senior Engineer (BEL)

## Project Context
A professional document-to-markdown converter for BEL engineering teams.
**Stack:** Python 3.12+, CustomTkinter, Docling.

## Essential Mandates
- **Offline First:** Under no circumstances should the agent attempt to connect to external APIs (Hugging Face, etc.). Use local artifacts only.
- **Architecture:** Use a strict Class-Based MVC (Model-View-Controller) pattern.
- **Environment:** Run within the project's virtual environment. 

## Key Commands
- Download models: `python download_artifacts.py`
- Run App: `python main.py`

## File Structure
- `models/`: Contains downloaded artifacts.
- `main.py`: Main application file.
- `download_artifacts.py`: Script to download artifacts.