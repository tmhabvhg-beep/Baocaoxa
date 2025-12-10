import streamlit as st
import pandas as pd
import os
from datetime import datetime

# 1. CẤU HÌNH TÀI KHOẢN (Tên đăng nhập : Mật khẩu)
# Bạn có thể thêm/sửa các phòng ban tại đây
USERS = {
    "admin": "admin123",      # Tài khoản của bạn để xem tổng hợp
    "vanhoa": "123456",       # Phòng Văn hóa
    "kinhte": "123456",       # Phòng Kinh tế
    "dothi": "123456",        # Giao thông/Đô thị
    "channuoi": "123456",     # Chăn nuôi/Thú y
    "motcua": "123456"        # Bộ phận Một cửa (TTHC)
}

# Tên file lưu dữ liệu
DATA_FILE = 'du_lieu_bao_cao.csv'

# Hàm để kiểm tra đăng nhập
def check_login(username, password):
    return username in USERS and USERS[username] == password

# Hàm tải dữ liệu hiện có
def load_data():
    if not os.path.exists(DATA_FILE):
        return pd.DataFrame(columns=["Thời gian", "Người gửi", "Lĩnh vực", "Nội dung báo cáo", "Số liệu nổi bật"])
    return pd.read_csv(DATA_FILE)

# Hàm lưu dữ liệu mới
def save_data(data):
    # Nếu file chưa có header thì ghi header, ngược lại ghi nối tiếp (append)
    if not os.path.exists(DATA_FILE):
        data.to_csv(DATA_FILE, index=False)
    else:
        data.to_csv(DATA_FILE, mode='a', header=False, index=False)

# --- GIAO DIỆN CHÍNH ---
st.set_page_config(page_title="Hệ thống Báo cáo Xã", layout="wide")

st.title("📋 Hệ thống Tổng hợp Báo cáo Xã")

# Sidebar cho Đăng nhập
with st.sidebar:
    st.header("Đăng nhập hệ thống")
    username = st.text_input("Tên đăng nhập")
    password = st.text_input("Mật khẩu", type="password")
    login_btn = st.button("Đăng nhập")

if login_btn and check_login(username, password):
    st.session_state['logged_in'] = True
    st.session_state['user'] = username
    st.success(f"Xin chào {username}!")

# Kiểm tra trạng thái đăng nhập
if 'logged_in' not in st.session_state or not st.session_state['logged_in']:
    st.info("Vui lòng đăng nhập để tiếp tục.")
else:
    user = st.session_state['user']
    
    # === GIAO DIỆN DÀNH CHO ADMIN (BẠN) ===
    if user == "admin":
        st.header("TỔNG HỢP SỐ LIỆU TOÀN XÃ")
        df = load_data()
        
        # Bộ lọc dữ liệu
        st.subheader("Dữ liệu đã gửi")
        st.dataframe(df, use_container_width=True)

        # Xuất báo cáo
        st.subheader("Xuất báo cáo")
        if not df.empty:
            # Chuyển đổi thành CSV để tải về
            csv = df.to_csv(index=False).encode('utf-8-sig')
            st.download_button(
                label="📥 Tải xuống file Excel/CSV",
                data=csv,
                file_name=f"bao_cao_tong_hop_{datetime.now().strftime('%Y%m%d')}.csv",
                mime='text/csv',
            )
        else:
            st.warning("Chưa có dữ liệu nào được gửi.")

    # === GIAO DIỆN DÀNH CHO CÁC PHÒNG BAN ===
    else:
        st.header(f"Nhập liệu báo cáo - Bộ phận: {user.upper()}")
        
        with st.form("form_bao_cao"):
            linh_vuc = st.selectbox("Chọn lĩnh vực", 
                                    ["Kinh tế", "Văn hóa xã hội", "Giao thông đô thị", "Chăn nuôi", "TTHC (Một cửa)", "Khác"])
            
            noi_dung = st.text_area("Nội dung công việc đã thực hiện (Chi tiết)", height=150)
            so_lieu = st.text_input("Số liệu nổi bật (Ví dụ: Đã giải quyết 50 hồ sơ, Tiêm phòng 100 con...)")
            
            submitted = st.form_submit_button("Gửi báo cáo")
            
            if submitted:
                if noi_dung:
                    # Tạo dòng dữ liệu mới
                    new_data = pd.DataFrame([{
                        "Thời gian": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Người gửi": user,
                        "Lĩnh vực": linh_vuc,
                        "Nội dung báo cáo": noi_dung,
                        "Số liệu nổi bật": so_lieu
                    }])
                    
                    save_data(new_data)
                    st.success("Đã gửi báo cáo thành công! Cảm ơn đồng chí.")
                else:
                    st.error("Vui lòng nhập nội dung công việc.")