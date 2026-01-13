"""
Shared path definitions for the ElectriAI Research project.

All paths are defined relative to the project root using pathlib,
ensuring portability across Windows, Linux, and macOS.

Usage:
    from src.paths import PROJECT_ROOT, RAW_DIR, PROCESSED_DIR, REFERENCE_DIR, FIGURES_DIR
"""

from pathlib import Path

# Project root is the parent of the 'src' directory (where this file lives)
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Data directories
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
REFERENCE_DIR = DATA_DIR / "reference"

# Figures directory
FIGURES_DIR = PROJECT_ROOT / "figures"

# Notebooks directory (for reference)
NOTEBOOKS_DIR = PROJECT_ROOT / "notebooks"

# Ensure output directories exist
for directory in [RAW_DIR, PROCESSED_DIR, REFERENCE_DIR, FIGURES_DIR]:
    directory.mkdir(parents=True, exist_ok=True)
