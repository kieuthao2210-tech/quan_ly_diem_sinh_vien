import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

# ==========================================
# #1. TẠO FRAME DỮ LIỆU GỐC CỦA BẠN
# ==========================================
data = {
    'MSSV': [
        'SV001',
        'SV002',
        'SV003',
        'SV004',
        'SV005',
        'SV006',
        'SV007',
        'SV008',
        'SV009',
        'SV010',
    ],
    'Họ và tên': [
        'Nguyễn Văn An',
        'Trần Thị Bình',
        'Lê Hoàng Cường',
        'Phạm Thị Dung',
        'Hoàng Văn Em',
        'Vũ Thị Phương',
        'Đặng Quốc Huy',
        'Bùi Thị Linh',
        'Ngô Minh Khang',
        'Dương Thu Thảo',
    ],
    'Điểm chuyên cần': [8, 8.5, 5.0, 9.0, 8.5, 7.0, 9.0, 8.0, 6.0, 9.5],
    'Điểm giữa kỳ': [8.5, 7.0, 6.5, 9.0, 5.5, 4.0, 8.0, 7.5, 5.0, 8.5],
    'Điểm cuối kỳ': [9.0, 8.0, 7.5, 8.5, 6.0, 5.0, 8.5, 9.0, 4.5, 9.0],
}
df = pd.DataFrame(data)

# ==========================================
# #2. TÍNH ĐIỂM TỔNG KẾT
# ==========================================
df['Điểm tổng kết'] = (
    0.2 * df['Điểm chuyên cần']
    + 0.3 * df['Điểm giữa kỳ']
    + 0.5 * df['Điểm cuối kỳ']
)

# ==========================================
# #3. XẾP LOẠI SINH VIÊN
# ==========================================
def tinh_xep_loai(diem):
  if diem >= 8.5:
    return 'Giỏi'
  elif diem >= 7.0:
    return 'Khá'
  elif diem >= 5.0:
    return 'Trung bình'
  else:
    return 'Yếu'


df['Xếp loại'] = df['Điểm tổng kết'].apply(tinh_xep_loai)

# ==========================================
# #4. STREAMLIT WEB APP - HIỂN THỊ THEO YÊU CẦU
# ==========================================

# • Hiển thị tiêu đề: QUẢN LÝ ĐIỂM SINH VIÊN-
st.title('QUẢN LÝ ĐIỂM SINH VIÊN-')

# • Hiển thị bảng điểm của 10 sinh viên gồm: Họ tên, Chuyên cần, Giữa kỳ, Cuối kỳ, Tổng kết và Xếp loại.
st.subheader('Bảng điểm sinh viên')
st.dataframe(df, use_container_width=True)
st.markdown('---')

# Tính toán các thông số thống kê
dtk_tb = df['Điểm tổng kết'].mean()
sv_cao_nhat = df.loc[df['Điểm tổng kết'].idxmax()]
sv_thap_nhat = df.loc[df['Điểm tổng kết'].idxmin()]
so_sv_dat = (df['Điểm tổng kết'] >= 5.0).sum()

st.subheader('Thông tin thống kê lớp học')
# • Hiển thị điểm trung bình của lớp.
st.write(f'- Điểm trung bình của lớp: **{dtk_tb:.2f}**')
# • Hiển thị sinh viên có điểm tổng kết cao nhất và thấp nhất.
st.write(
    f"- Sinh viên có điểm tổng kết cao nhất: **{sv_cao_nhat['Họ và tên']} ({sv_cao_nhat['Điểm tổng kết']})**"
)
st.write(
    f"- Sinh viên có điểm tổng kết thấp nhất: **{sv_thap_nhat['Họ và tên']} ({sv_thap_nhat['Điểm tổng kết']})**"
)
# • Hiển thị số sinh viên đạt.
st.write(f'- Số sinh viên đạt: **{so_sv_dat} sinh viên**')
st.markdown('---')

# • Tạo danh sách xổ xuống (Selectbox) để người dùng chọn một sinh viên.
st.subheader('Tra cứu thông tin sinh viên')
ten_chon = st.selectbox('Chọn một sinh viên:', df['Họ và tên'].tolist())

# • Khi chọn sinh viên, hiển thị điểm Chuyên cần, Giữa kỳ, Cuối kỳ, Điểm tổng kết và Xếp loại của sinh viên đó.
thong_tin_sv = df[df['Họ và tên'] == ten_chon].iloc[0]
st.write(f'**Thông tin chi tiết của sinh viên {ten_chon}:**')
st.write(f"- Điểm Chuyên cần: **{thong_tin_sv['Điểm chuyên cần']}**")
st.write(f"- Điểm Giữa kỳ: **{thong_tin_sv['Điểm giữa kỳ']}**")
st.write(f"- Điểm Cuối kỳ: **{thong_tin_sv['Điểm cuối kỳ']}**")
st.write(f"- Điểm Tổng kết: **{thong_tin_sv['Điểm tổng kết']}**")
st.write(f"- Xếp loại: **{thong_tin_sv['Xếp loại']}**")
st.markdown('---')

# • Hiển thị biểu đồ cột điểm tổng kết của 10 sinh viên (Màu hồng - Chữ nằm ngang)
st.subheader('Biểu đồ điểm tổng kết')
fig, ax = plt.subplots(figsize=(8, 4))
ten_sinh_vien = df['Họ và tên'].str.split().str[-1]

ax.bar(ten_sinh_vien, df['Điểm tổng kết'], color='pink', edgecolor='black')
ax.set_title('Biểu đồ điểm tổng kết của sinh viên', fontsize=12)
ax.set_xlabel('Tên sinh viên')
ax.set_ylabel('Điểm tổng kết')
ax.set_ylim(0, 10)
plt.xticks(rotation=0)  # Chữ nằm ngang thẳng hàng
st.pyplot(fig)

# • Hiển thị họ tên và MSSV chữ nhỏ ở cuối trang Web App.
st.markdown('<br><hr>', unsafe_allow_html=True)
st.caption('Người tạo ứng dụng: Kiều Phương Thảo - MSSV: KiềuPhươngThảo50')
