"""
VSM Interactive Search CLI (Legacy Entrypoint)
Delegates to src.modeling.vsm_cli
"""

import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parent.parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from src.modeling.vsm_cli import run_vsm_cli

if __name__ == '__main__':
    run_vsm_cli()