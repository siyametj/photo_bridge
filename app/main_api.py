# app/main_api.py

from typing import List
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException, UploadFile, File
from app.storage import save_to_staging, get_staged_files, accept_file, reject_file

app = FastAPI(title="Photo Bridge API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def home():
    return {"message": "Welcome to Photo Bridge API"}

@app.post("/upload")
async def uploads_photo(files: List[UploadFile] = File(...)):
    if not files:
        raise HTTPException(
            status_code=400,
            detail="No file have been selected!"
        )
    saved_names = save_to_staging(files=files)
    return {
        "status": "success",
        "message": f"{len(saved_names)} pictures is staged",
        "files": saved_names,
    }

@app.get("/pending")
def list_pending():
    files = get_staged_files()
    return {
        "count": len(files),
        "pending_files": files,
    }

@app.post("/accept/{filename}")
def accept_photo(filename: str):
    success = accept_file(filename)
    if not success:
        raise HTTPException(
            status_code=404, detail="File not found",
        )
    return {"status": "accepted", "filename": filename}

@app.delete("/reject/{filename}")
def reject_photo(filename: str):
    success = reject_file(filename)
    if not success:
        raise HTTPException(
            status_code=404,
            detail="File not found"
        )
    return {"status": "rejected", "filename": filename}
