# run_server.py

import uvicorn

if __name__ == "__main__":
    print("Photo Bridge Server Starting on Port 8000...")
    uvicorn.run("app.main_api:app", host="0.0.0.0", port=8000, reload=True)

