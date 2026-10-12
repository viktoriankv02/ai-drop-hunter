"""Shared persistent paths for desktop and Linux services."""
import os
from pathlib import Path
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")
DEFAULT_DB = Path(os.environ.get("HUNTER_DB", str(ROOT / "data/workspace.sqlite"))).expanduser()
if not DEFAULT_DB.is_absolute():
    DEFAULT_DB = ROOT / DEFAULT_DB

def mobile_database(database=DEFAULT_DB):
    path = Path(database)
    return path.with_name(path.stem + "-mobile.sqlite")
