# 📸 Photo Bridge

Photo Bridge is a small local photo-staging server built with **FastAPI** and **Streamlit**.

The idea is simple:

> Send photos to the server, keep them in a temporary staging directory, preview them, then either **Accept** them into your main Pictures directory or **Reject** them.

The project uses FastAPI for the backend API and Streamlit for the browser-based interface.

## ✨ Features

- 📤 Upload multiple photos through the API
- 🗂️ Store uploaded files in a temporary staging directory
- 👀 List pending/staged photos
- ✅ Accept a photo and move it to the final Pictures directory
- ❌ Reject a photo and delete it from staging
- 🖼️ Preview staged photos through Streamlit
- 🌐 FastAPI automatic Swagger/OpenAPI documentation
- 🔄 Development server with automatic reload
- ⚙️ Configurable staging and final directories through environment variables

## 🏗️ Project Structure

```text
photo_bridge/
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── main_api.py
│   └── storage.py
│
├── gui/
│   └── streamlit_gui.py
│
├── photo_result/
│   ├── client_device.jpeg
│   └── server.png
│
├── LICENSE
├── README.md
├── requirements.txt
└── run_server.py
```

### `app/config.py`

Controls the staging and final directories.

Default locations:

```text
Staging: ~/Pictures/.client_image
Final:   ~/Pictures
```

They can be overridden with:

```bash
export STAGING_DIR=/path/to/staging
export FINAL_DIR=/path/to/final
```

### `app/main_api.py`

Contains the FastAPI application and the client-facing web interface. The `/` route serves the HTML upload GUI directly from FastAPI.

### `app/storage.py`

Handles saving, listing, accepting, and rejecting staged photos.

### `gui/streamlit_gui.py`

Contains the server-side Streamlit management GUI.

### `run_server.py`

Starts the FastAPI application through Uvicorn.

# 🔌 API Endpoints

### `GET /`

Returns a simple welcome message.

Example response:

```json
{
  "message": "Welcome to Photo Bridge API"
}
```

### `POST /upload`

Uploads one or more files to the staging directory.

The endpoint expects multipart form data using the `files` field.

Example response:

```json
{
  "status": "success",
  "message": "2 pictures is staged",
  "files": [
    "photo1.jpg",
    "photo2.png"
  ]
}
```

### `GET /pending-photos`

Returns the files currently waiting in staging.

Example response:

```json
{
  "count": 2,
  "pending_files": [
    "photo1.jpg",
    "photo2.png"
  ]
}
```

### `POST /accept/{filename}`

Accepts a staged photo and moves it from the staging directory to the final directory.

Example:

```text
POST /accept/photo1.jpg
```

### `DELETE /reject/{filename}`

Rejects a staged photo and removes it from the staging directory.

Example:

```text
DELETE /reject/photo1.jpg
```

## 🖥️ API Documentation

When the server is running, FastAPI provides interactive API documentation at:

```text
http://127.0.0.1:8000/docs
```

The OpenAPI schema is available at:

```text
http://127.0.0.1:8000/openapi.json
```

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/siyametj/photo_bridge.git
cd photo_bridge
```

Create a virtual environment:

```bash
python3 -m venv venv
```

Activate it:

```bash
source venv/bin/activate
```

Install the dependencies:

```bash
pip install -r requirements.txt
```

## ▶️ Running the Backend

Start the Photo Bridge server:

```bash
python3 run_server.py
```

You should see something similar to:

```text
Photo Bridge Server Starting on Port 8000...
Uvicorn running on http://0.0.0.0:8000
```

The API can then be accessed locally at:

```text
http://127.0.0.1:8000
```

## 🎨 Running the Streamlit GUI

Start the Streamlit interface in another terminal:

```bash
streamlit run gui/streamlit_gui.py
```

The GUI communicates with the backend through:

```text
http://127.0.0.1:8000
```

The interface is designed to show staged photos and provide **Accept** and **Reject** actions.

## 🔄 Basic Workflow

```text
Phone / Client
      │
      │ Upload photo
      ▼
 FastAPI Backend
      │
      ▼
 Staging Directory
 ~/Pictures/.client_image
      │
      ├───────────────┐
      │               │
      ▼               ▼
   ACCEPT           REJECT
      │               │
      ▼               ▼
 ~/Pictures       Delete file
```

The staging directory acts as a safety/checkpoint area before a photo becomes part of the final collection.

## 🧪 Development

Run the backend with automatic reload:

```bash
python3 run_server.py
```

The project can also be started directly with Uvicorn:

```bash
uvicorn app.main_api:app --reload
```

## 📦 Main Technologies

- **Python**
- **FastAPI**
- **Uvicorn**
- **Streamlit**
- **Pillow**
- **Requests**
- **python-multipart**

The exact pinned dependency versions are available in `requirements.txt`.

## 🔐 Security Note

This project is currently designed as a local/development photo bridge.

The API enables permissive CORS:

```python
allow_origins=["*"]
```

and the server listens on:

```text
0.0.0.0:8000
```

Before exposing the application to an untrusted network, authentication, authorization, safer CORS configuration, filename validation, and other security controls should be added.

### 📸 Screenshots

The repository contains two example screenshots in `photo_result/`:

```text
photo_result/
├── client_device.jpeg
└── server.png
```

They show the two main sides of Photo Bridge: the client upload page and the server-side photo management GUI.

# 📜 License


This project is licensed under the terms of the [MIT License](LICENSE) - see the [MIT License](LICENSE)  file for details..
