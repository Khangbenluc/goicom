import streamlit as st
from gtts import gTTS
import os

st.set_page_config(page_title="Gọi cơm", layout="wide")

st.title("🍱 Ứng dụng gọi cơm")

# --- Cột trái: Gọi khách hàng ---
col1, col2 = st.columns([2, 1])

with col1:
    st.header("📢 Gọi khách")

    # Dropdown số thứ tự và quầy
    so_goi = st.selectbox("Số thứ tự:", list(range(1, 11)))
    quay = st.selectbox("Quầy:", ["Cơm", "Canh", "Nước", "Tráng miệng"])

    if st.button("🔔 Gọi"):
        # Tạo thông báo
        thong_bao = f"Kính mời khách hàng số {so_goi} đến quầy {quay}. Xin cảm ơn!"
        st.success(thong_bao)

        # Hiện số thật to, căn giữa
        st.markdown(
            f"<h1 style='text-align:center; font-size:100px; color:red;'>{so_goi}</h1>",
            unsafe_allow_html=True
        )

        # Phát âm thanh
        tts = gTTS(thong_bao, lang='vi')
        audio_path = "thong_bao.mp3"
        tts.save(audio_path)
        st.audio(audio_path, format="audio/mp3")

# --- Cột phải: Máy tính tiền ---
with col2:
    st.header("💰 Máy tính tiền")

    if "tong_tien" not in st.session_state:
        st.session_state.tong_tien = 0

    # Các nút cộng tiền
    for so_tien in [10000, 20000, 30000, 40000, 50000, 60000]:
        if st.button(f"+ {so_tien:,} đ"):
            st.session_state.tong_tien += so_tien

    # Hiện tổng
    st.markdown("---")
    st.markdown(f"### Tổng tiền: <span style='color:green'>{st.session_state.tong_tien:,} đ</span>", unsafe_allow_html=True)

    if st.button("🧾 Reset"):
        st.session_state.tong_tien = 0
