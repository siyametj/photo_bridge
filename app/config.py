# app/configuration.py

import os
from pathlib import Path

HOME_DIR = Path.home()
DEFAULT_STAGING = HOME_DIR / "Pictures" / ".client_image"
DEFAULT_FINAL = HOME_DIR / "Pictures"

STAGING_DIR = Path(os.getenv("STAGING_DIR", DEFAULT_STAGING))
FINAL_DIR = Path(os.getenv("FINAL_DIR", DEFAULT_FINAL))

STAGING_DIR.mkdir(parents=True, exist_ok=True)
FINAL_DIR.mkdir(parents=True, exist_ok=True)

