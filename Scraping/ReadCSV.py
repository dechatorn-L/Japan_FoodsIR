"""
Cookpad Recipe Details Scraper (Legacy Entrypoint)
Delegates to src.crawler.recipe_scraper
"""

import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent.parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from src.crawler.recipe_scraper import scrape_recipe_details

if __name__ == '__main__':
    scrape_recipe_details()