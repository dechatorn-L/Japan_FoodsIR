"""
Cookpad URL Crawler (Legacy Entrypoint)
Delegates to src.crawler.url_scraper
"""

import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent.parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from src.crawler.url_scraper import scrape_recipe_urls

if __name__ == '__main__':
    scrape_recipe_urls()
