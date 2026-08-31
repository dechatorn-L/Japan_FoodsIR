"""
Japanese Foods Information Retrieval Engine Entrypoint
Re-exports from src.engine
"""

import sys
from pathlib import Path

# Ensure src is in python path
SRC_DIR = Path(__file__).resolve().parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from src.engine import JapaneseFoodIREngine, get_engine

__all__ = ["JapaneseFoodIREngine", "get_engine"]
