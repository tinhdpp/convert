import streamlit as st
import pandas as pd
import json

# Hàm để tách và chuyển đổi Completion result
def extract_content(row):
    try:
        result = json.loads(row['Completion result'])
        content = result.get('content', '')
        ai_content = content.split('[AI CONTENT]')[1].split('[AI DESIGN BRIEF]')[0].strip()
        ai_design_brief = content.split('[AI DESIGN BRIEF]')[1].strip() if '[AI DESIGN BRIEF]' in content else ''
        ai_content = ai_content.replace('\\n', '\n')
        ai_design_brief = ai_design_brief.replace('\\n', '\n')
        return pd.Series([ai_content, ai_design_brief])
    except (json.JSONDecodeError, KeyError, IndexError):
        return pd.Series(['', ''])

# Tiêu đề ứng dụng
st.title("CSV to Excel Converter")

# Tải lên tệp CSV
uploaded_file = st.file_uploader("Chọn tệp CSV", type="csv")

if uploaded_file is not None:
    # Đọc tệp CSV
    data = pd.read_csv(uploaded_file)
    
    # Xử lý dữ liệu
    result = data.dropna(subset=['Completion result'])
    filtered_df = result.drop(columns=['Campaign description'])
    filtered_df[['AI content', 'AI Design Brief']] = filtered_df.apply(extract_content, axis=1)

    # Xuất ra tệp Excel
    output_file = "content_output.xlsx"
    filtered_df.to_excel(output_file, index=False)

    # Cung cấp liên kết tải xuống
    st.success("Tệp Excel đã được tạo!")
    with open(output_file, "rb") as f:
        st.download_button("Tải xuống tệp Excel", f, file_name=output_file)