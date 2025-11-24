import streamlit as st
import pandas as pd
import os

# 导入计算模块
from calculator import calculate_performance

st.set_page_config(page_title="巴南妇保院绩效系统", layout="wide")
st.title("🏥 巴南妇保院绩效奖金分配系统")

uploaded_file = st.file_uploader("📤 上传奖金分配表（Excel格式）", type=["xlsx"])

if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)
        
        if df.empty:
            st.warning("⚠️ 文件无数据，请检查是否包含实际行。")
            st.stop()
            
        # 清洗列名
        df.columns = df.columns.astype(str).str.strip()
        
        if '科室' not in df.columns:
            st.error(f"❌ 缺少 '科室' 列！当前列: {list(df.columns)}")
            st.stop()
        
        # 计算
        result_df = calculate_performance(df)
        
        st.success("✅ 计算完成！")
        st.dataframe(result_df, use_container_width=True)
        
        # 下载
        csv = result_df.to_csv(index=False, encoding='utf-8-sig').encode('utf-8')
        st.download_button("📥 下载结果 (CSV)", csv, "绩效结果.csv", "text/csv")
        
    except Exception as e:
        st.error(f"💥 错误: {str(e)}")
else:
    st.info("👆 请上传 Excel 文件（需包含 '科室'、'工资总和' 列）")