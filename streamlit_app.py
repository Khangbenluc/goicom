import streamlit as st
from gtts import gTTS
import os

st.set_page_config(page_title="Gọi cơm", layout="wide")

st.title("🍱 Ứng dụng gọi cơm")

# --- Khởi tạo session state ---
if "tong_tien" not in st.session_state:
    st.session_state.tong_tien = 0
if "phat_am_thanh" not in st.session_state:
    st.session_state.phat_am_thanh = False

# --- Layout chia 2 cột ---
col1, col2 = st.columns([2, 1])

# ----------------------------- #
#          CỘT 1: GỌI CƠM
# ----------------------------- #
with col1:
    st.header("📢 Gọi khách")

    so_goi = st.selectbox("Số thứ tự:", list(range(1, 11)), key="so_goi")
    quay = st.selectbox("Quầy:", ["Cơm", "Canh", "Nước", "Tráng miệng"], key="quay")

    if st.button("🔔 Gọi"):
        thong_bao = f"Kính mời khách hàng số {so_goi} đến quầy {quay}. Xin cảm ơn!"
        st.session_state.phat_am_thanh = True
        st.session_state.thong_bao = thong_bao
        st.session_state.so_hien = so_goi
        st.success(thong_bao)

    # Hiện số đang gọi thật to
    if "so_hien" in st.session_state:
        st.markdown(
            f"<h1 style='text-align:center; font-size:100px; color:red;'>{st.session_state.so_hien}</h1>",
            unsafe_allow_html=True
        )

    # Phát âm thanh (chỉ khi nhấn nút Gọi)
    if st.session_state.phat_am_thanh:
        tts = gTTS(st.session_state.thong_bao, lang='vi')
        tts.save("thong_bao.mp3")
        st.audio("thong_bao.mp3", format="audio/mp3")
        st.session_state.phat_am_thanh = False

# ----------------------------- #
#        CỘT 2: MÁY TÍNH TIỀN
# ----------------------------- #
with col2:
    st.header("💰 Máy tính tiền")

    # Các nút cộng tiền (gọn hơn, nhanh hơn)
    btns = [10000, 20000, 30000, 40000, 50000, 60000]
    col_btns = st.columns(3)
    for i, so_tien in enumerate(btns):
        if col_btns[i % 3].button(f"+{so_tien//1000}K", key=f"t{so_tien}"):
            st.session_state.tong_tien += so_tien

    # Hiển thị tổng
    st.markdown("---")
    st.markdown(
        f"<h3 style='text-align:center;'>Tổng tiền:</h3>"
        f"<h2 style='text-align:center; color:green;'>{st.session_state.tong_tien:,} đ</h2>",
        unsafe_allow_html=True
    )

    # Nút reset
    if st.button("🧾 Reset tổng"):
        st.session_state.tong_tien = 0
