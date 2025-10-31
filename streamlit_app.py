import streamlit as st
from gtts import gTTS
from pathlib import Path
import base64
import tempfile
import os

st.set_page_config(page_title="Gọi cơm", layout="wide")
st.title("🍱 Ứng dụng gọi cơm")

# --- File chuông có sẵn ---
TING_PATH = Path("ting.mp3")

if not TING_PATH.exists():
    st.error("⚠️ Không tìm thấy file ting.mp3 trong thư mục! Hãy thêm file này vào cùng với goi_com.py.")
    st.stop()

# --- Khởi tạo session state ---
if "tong_tien" not in st.session_state:
    st.session_state.tong_tien = 0
if "so_hien" not in st.session_state:
    st.session_state.so_hien = None
if "thong_bao" not in st.session_state:
    st.session_state.thong_bao = ""
if "phat_am_thanh" not in st.session_state:
    st.session_state.phat_am_thanh = False

# --- Layout chia đôi ---
col1, col2 = st.columns([2, 1])

# =============================
# CỘT TRÁI: GỌI KHÁCH
# =============================
with col1:
    st.header("📢 Gọi khách")

    so_goi = st.selectbox("Số thứ tự:", list(range(1, 11)), index=0)
    quay = st.selectbox("Quầy:", ["Cơm", "Canh", "Nước", "Tráng miệng"], index=0)

    if st.button("🔔 Gọi"):
        thong_bao = f"Kính mời khách hàng số {so_goi} đến quầy {quay}. Xin cảm ơn!"
        st.session_state.thong_bao = thong_bao
        st.session_state.so_hien = so_goi
        st.session_state.phat_am_thanh = True
        st.success(f"Đang gọi khách hàng số {so_goi} đến quầy {quay}...")

    # Hiển thị số to
    if st.session_state.so_hien:
        st.markdown(
            f"<div style='text-align:center; margin-top:20px;'>"
            f"<span style='font-size:120px; color:red; font-weight:bold;'>{st.session_state.so_hien}</span>"
            f"</div>",
            unsafe_allow_html=True
        )

# =============================
# CỘT PHẢI: MÁY TÍNH TIỀN
# =============================
with col2:
    st.header("💰 Máy tính tiền")

    col_btns = st.columns(3)
    for i, so_tien in enumerate([10000, 20000, 30000, 40000, 50000, 60000]):
        if col_btns[i % 3].button(f"+{so_tien//1000}K", key=f"t{so_tien}"):
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
# PHÁT ÂM THANH (ting -> TTS)
# =============================
def file_to_b64(file_path: Path):
    """Chuyển file mp3 thành data URI base64 để nhúng HTML"""
    data = file_path.read_bytes()
    b64 = base64.b64encode(data).decode()
    return f"data:audio/mp3;base64,{b64}"

def tts_to_b64(text: str):
    """Tạo file tạm từ gTTS, trả về base64 data URI"""
    with tempfile.NamedTemporaryFile(suffix=".mp3", delete=False) as tmp:
        temp_path = tmp.name
    try:
        gTTS(text, lang="vi").save(temp_path)
        b64 = base64.b64encode(Path(temp_path).read_bytes()).decode()
        return f"data:audio/mp3;base64,{b64}"
    finally:
        os.remove(temp_path)

if st.session_state.phat_am_thanh:
    ting_uri = file_to_b64(TING_PATH)
    tts_uri = tts_to_b64(st.session_state.thong_bao)

    # HTML + JS phát tuần tự: ting -> tts
    html = f"""
    <div>
      <audio id="ting" preload="auto" src="{ting_uri}"></audio>
      <audio id="tts" preload="auto" src="{tts_uri}"></audio>
    </div>
    <script>
      const ting = document.getElementById("ting");
      const tts = document.getElementById("tts");
      ting.play().catch(e => {{
          console.log("Không tự phát được ting:", e);
          tts.play().catch(e2 => console.log("Không tự phát được TTS:", e2));
      }});
      ting.onended = () => {{
          tts.play().catch(e => console.log("Không tự phát được TTS:", e));
      }};
    </script>
    """
    st.markdown(html, unsafe_allow_html=True)

    # Reset flag
    st.session_state.phat_am_thanh = False

# =============================
# Ghi chú cuối trang
# =============================
st.markdown("---")
st.caption("© 2025 - Ứng dụng Gọi Cơm | Phiên bản thử nghiệm")
