"""
Text Preprocessing & NLP Cleaning (Legacy Entrypoint)
Delegates to src.preprocessing.text_cleaner
"""

import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent.parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from src.preprocessing.text_cleaner import clean_recipe_dataset

if __name__ == '__main__':
    clean_recipe_dataset()