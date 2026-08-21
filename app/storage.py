# app/storage.py

import shutil
from typing import List
from fastapi import UploadFile
from app.config import STAGING_DIR, FINAL_DIR

def save_to_staging(files: List[UploadFile]) -> List[str]:
    saved_files = []
    for file in files:
        file_path = STAGING_DIR / file.filename

        with open(file=file_path, mode="wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        saved_files.append(file.filename)
    return saved_files

def get_staged_files() -> List[str]:
    return [f.name for f in STAGING_DIR.iterdir() if f.is_file()]

def accept_file(file_name: str) -> bool:
    source = STAGING_DIR / file_name
    destination = FINAL_DIR / file_name

    if source.exists():
        shutil.move(str(source), str(destination))
        return True
    return False

def reject_file(file_name: str) -> bool:
    file_path = STAGING_DIR / file_name
    if file_path.exists():
        file_path.unlink()
        return True
    return False
