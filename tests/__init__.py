import sys
from pathlib import Path

root = Path(__file__).resolve().parent
src = root.parent / "src"
sys.path.insert(0, str(src))
