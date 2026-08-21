from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from app.storage import (
    save_to_staging,
    get_staged_files,
    accept_file,
    reject_file
)

app = FastAPI(title="Photo Bridge API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", response_class=HTMLResponse)
def phone_gui():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Photo Bridge - Phone Upload</title>
        <style>
            body {
                font-family: Arial, sans-serif;
                background-color: #121212;
                color: #ffffff;
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                min-height: 100vh;
                margin: 0;
                padding: 20px;
                box-sizing: border-box;
            }
            .card {
                background: #1e1e1e;
                padding: 30px;
                border-radius: 16px;
                box-shadow: 0 4px 20px rgba(0,0,0,0.5);
                text-align: center;
                width: 100%;
                max-width: 400px;
            }
            h2 { color: #ff4b4b; margin-bottom: 8px; }
            p { color: #aaa; font-size: 14px; margin-bottom: 24px; }
            input[type="file"] { display: none; }
            .file-label {
                background-color: #2b2b2b;
                border: 2px dashed #ff4b4b;
                padding: 20px;
                border-radius: 12px;
                display: block;
                cursor: pointer;
                margin-bottom: 20px;
                font-weight: bold;
                color: #ddd;
            }
            .btn {
                background: linear-gradient(135deg, #ff4b4b, #ff2a2a);
                color: white;
                border: none;
                padding: 14px;
                width: 100%;
                border-radius: 10px;
                font-size: 16px;
                font-weight: bold;
                cursor: pointer;
            }
            #status { margin-top: 20px; font-weight: bold; font-size: 15px; }
        </style>
    </head>
    <body>
        <div class="card">
            <h2>📸 Photo Bridge</h2>
            <p>Send photos in one click!</p>

            <form id="uploadForm">
                <label for="photoInput" class="file-label" id="fileLabel">
                    📁 <span>Select photos (Multiple)</span>
                </label>
                <input type="file" id="photoInput" name="files" multiple accept="image/*" onchange="updateLabel()">

                <button type="submit" class="btn">🚀 Upload All Photos</button>
            </form>

            <div id="status"></div>
        </div>

        <script>
            function updateLabel() {
                const input = document.getElementById('photoInput');
                const label = document.getElementById('fileLabel');
                if (input.files.length > 0) {
                    label.innerHTML = `✅ ${input.files.length} files selected!`;
                }
            }

            document.getElementById('uploadForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                const input = document.getElementById('photoInput');
                const status = document.getElementById('status');

                if (input.files.length === 0) {
                    status.style.color = '#ff4b4b';
                    status.innerText = 'Please select photos first!';
                    return;
                }

                const formData = new FormData();
                for (let i = 0; i < input.files.length; i++) {
                    formData.append('files', input.files[i]);
                }

                status.style.color = '#ffbb00';
                status.innerText = 'Uploading... please wait ⏳';

                try {
                    const res = await fetch('/upload', { method: 'POST', body: formData });
                    const data = await res.json();
                    if (res.ok) {
                        status.style.color = '#00ff77';
                        status.innerText = `🎉 ${input.files.length} photos uploaded successfully!`;
                        document.getElementById('uploadForm').reset();
                        document.getElementById('fileLabel').innerHTML = '📁 <span>Send more photos?</span>';
                    } else {
                        status.style.color = '#ff4b4b';
                        status.innerText = 'Upload Failed!';
                    }
                } catch (err) {
                    status.style.color = '#ff4b4b';
                    status.innerText = 'Server Error!';
                }
            });
        </script>
    </body>
    </html>
    """

@app.post("/upload")
async def upload_photos(files: List[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded!")
    saved_names = save_to_staging(files)
    return {"message": f"Successfully uploaded {len(saved_names)} photos!", "filenames": saved_names}

@app.get("/pending-photos")
def list_pending_photos():
    files = get_staged_files()
    return {"pending_count": len(files), "photos": files}

@app.post("/accept/{filename}")
def accept_photo(filename: str):
    success = accept_file(filename)
    if not success:
        raise HTTPException(status_code=404, detail="File not found!")
    return {"status": "Accepted", "filename": filename}

@app.delete("/reject/{filename}")
def reject_photo(filename: str):
    success = reject_file(filename)
    if not success:
        raise HTTPException(status_code=404, detail="File not found!")
    return {"status": "Rejected", "filename": filename}
