import streamlit as st
from gtts import gTTS
from pathlib import Path
import tempfile
import os

st.set_page_config(page_title="Gọi cơm", layout="wide")
st.title("🍱 Ứng dụng gọi cơm")

# --- File chuông có sẵn ---
TING_PATH = Path("ting.mp3")
if not TING_PATH.exists():
    st.error("⚠️ Không tìm thấy file ting.mp3 trong thư mục! Hãy thêm file này vào cùng với goi_com.py.")
    st.stop()

# --- Session state ---
if "tong_tien" not in st.session_state:
    st.session_state.tong_tien = 0
if "so_hien" not in st.session_state:
    st.session_state.so_hien = None
if "thong_bao" not in st.session_state:
    st.session_state.thong_bao = ""
if "ting_bytes" not in st.session_state:
    st.session_state.ting_bytes = TING_PATH.read_bytes()
if "tts_bytes" not in st.session_state:
    st.session_state.tts_bytes = None

# --- Layout chia đôi ---
col1, col2 = st.columns([2, 1])

# =============================
# CỘT TRÁI: GỌI KHÁCH
# =============================
with col1:
    st.header("📢 Gọi khách")

    so_goi = st.selectbox("Số thứ tự:", list(range(1, 7)), index=0)
    quay = st.selectbox("Quầy:", ["Cơm", "Canh", "Nước và tráng miệng", "Lễ tân"], index=0)

    if st.button("🔔 Gọi"):
        thong_bao = f"Kính mời khách hàng số {so_goi} đến quầy {quay} để nhận món. Xin cảm ơn!"
        st.session_state.thong_bao = thong_bao
        st.session_state.so_hien = so_goi

        # Tạo file TTS tạm thời
        with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
            gTTS(thong_bao, lang="vi").save(tmp.name)
            st.session_state.tts_bytes = Path(tmp.name).read_bytes()
        os.remove(tmp.name)

        st.success(f"Đã tạo lời mời cho khách hàng số {so_goi} đến quầy {quay}")

    # Hiển thị số to
    if st.session_state.so_hien:
        st.markdown(
            f"<div style='text-align:center; margin-top:20px;'>"
            f"<span style='font-size:150px; color:red; font-weight:bold;'>{st.session_state.so_hien}</span>"
            f"</div>",
            unsafe_allow_html=True
        )

    # Hiển thị trình phát âm thanh (nếu đã tạo)
    if st.session_state.tts_bytes:
        st.markdown("#### 🔊 Chuông báo:")
        st.audio(st.session_state.ting_bytes, format="audio/mp3")

        st.markdown("#### 🗣️ Lời mời khách hàng:")
        st.audio(st.session_state.tts_bytes, format="audio/mp3")

# =============================
# CỘT PHẢI: MÁY TÍNH TIỀN
# =============================
with col2:
    st.header("💰 Máy tính tiền")

    col_btns = st.columns(3)
    for i, so_tien in enumerate([10000, 20000, 30000, 40000, 50000):
        if col_btns[i % 3].button(f"+{so_tien//1} vnđ", key=f"t{so_tien}"):
            st.session_state.tong_tien += so_tien

    st.markdown("---")
    st.markdown(
        f"<h4 style='text-align:center;'>Tổng tiền:</h4>"
        f"<h2 style='text-align:center; color:green;'>{st.session_state.tong_tien:,} đ</h2>",
        unsafe_allow_html=True
    )

    if st.button("🧾 Reset tổng"):
        st.session_state.tong_tien = 0
        st.success("Đã reset tổng tiền.")

# =============================
# Ghi chú cuối trang
# =============================
st.markdown("---")
st.caption("© 2025 - Ứng dụng Gọi Cơm | Dùng file ting.mp3 trong cùng thư mục.")
