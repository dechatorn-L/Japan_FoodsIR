"""
Food Clustering & PCA Visualization (Legacy Entrypoint)
Delegates to src.modeling.food_clustering
"""

import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent.parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from src.modeling.food_clustering import run_food_clustering

if __name__ == '__main__':
    run_food_clustering()