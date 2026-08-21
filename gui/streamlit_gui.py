# gui/streamlit_gui.py

import streamlit as st
import requests
from PIL import Image
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parent.parent))
from app.config import STAGING_DIR

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Photo Bridge Staging", page_icon="📸", layout="wide")

st.title("Photo Bridge")
st.write("Send any photo from phone and save your server")

col_top1, col_top2 = st.columns([3, 1])

with col_top2:
    if st.button("Refresh Staging", use_container_width=True):
        st.rerun()

try:
    response = requests.get(f"{API_URL}/pending-photos")
    if response.status_code == 200:
        data = response.json()
        pending_photos = data.get("photos", [])
    else:
        pending_photos = []
        st.error("API Error: Data not found in backend")
except Exception as e:
    st.error(f"Server is offline! Please run `python run_server.py`({e})")
    pending_photos = []

st.subheader(f"Pending Photos in Staging: {len(pending_photos)}")

if pending_photos:
    if st.button("Accept ALL Photos", type="primary"):
        success_count = 0
        for photo in pending_photos:
            res = requests.post(f"{API_URL}/accept/{photo}")
            if res.status_code == 200:
                success_count += 1
        st.success(f"{success_count} photo move success in ~/Pictures")
        st.rerun()

    st.markdown("---")

    cols = st.columns(3)
    for idx, photo_name in enumerate(pending_photos):
        col = cols[idx % 3]
        file_path = STAGING_DIR / photo_name

        with col:
            st.write(f"**{photo_name}**")

            if file_path.exists():
                try:
                    img = Image.open(file_path)
                    st.image(img, use_container_width=True)
                except Exception:
                    st.warning("Preview unavailable!")

            btn_col1, btn_col2 = st.columns(2)
            with btn_col1:
                if st.button(f"Accept", key=f"acc_{photo_name}"):
                    res = requests.post(f"{API_URL}/accept/{photo_name}")
                    if res.status_code == 200:
                        st.success(f"Accepted!")
                        st.rerun()

            with btn_col2:
                if st.button(f"Reject", key=f"rej_{photo_name}"):
                    res = requests.delete(f"{API_URL}/reject/{photo_name}")
                    if res.status_code == 200:
                        st.info(f"Deleted!")
                        st.rerun()
else:
    st.info("There are no pending photot")
