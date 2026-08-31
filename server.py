"""
Japanese Foods IR Web Application Launcher
"""

import sys
import argparse
from pathlib import Path

# Ensure src is in python path
SRC_DIR = Path(__file__).resolve().parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from src.web.server import run_server


def main():
    parser = argparse.ArgumentParser(description="Japanese Foods IR Web Application Server")
    parser.add_argument("--port", type=int, default=8000, help="Port to run the HTTP server on (default: 8000)")
    parser.add_argument("--host", type=str, default="0.0.0.0", help="Host address (default: 0.0.0.0)")
    args = parser.parse_args()

    run_server(host=args.host, port=args.port)


if __name__ == '__main__':
    main()
