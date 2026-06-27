import streamlit as st
import pandas as pd

st.set_page_config(page_title="CEO Executive Command Center", page_icon="📊", layout="wide")
st.title("📊 CEO Executive Command Center")
st.write("Xonim, kompaniyangizning boshqaruv paneliga xush kelibsiz!")

st.sidebar.header("Navigatsiya")
page = st.sidebar.radio("Bo'limni tanlang:", ["Asosiy Dashboard", "Moliyaviy Hisobot", "Vazifalar"])

if page == "Asosiy Dashboard":
    st.subheader("🚀 Bugungi asosiy ko'rsatkichlar")
    col1, col2, col3 = st.columns(3)
    col1.metric("Kunlik Daromad", "$1,250", "+12%")
    col2.metric("Yangi Mijozlar", "45", "+5%")
    col3.metric("Faol Loyihalar", "8", "0")
    st.success("Tizim barqaror ishlamoqda. Barcha bo'limlar nazorat ostida.")

elif page == "Moliyaviy Hisobot":
    st.subheader("💰 Moliyaviy tahlil")
    data = {'Oy': ['Yanvar', 'Fevral', 'Mart', 'Aprel'], 'Daromad ($)': [5000, 7000, 8500, 12000], 'Xarajat ($)': [3000, 3500, 4000, 4500]}
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True)
    st.line_chart(df.set_index('Oy'))

elif page == "Vazifalar":
    st.subheader("📌 Rejadagi vazifalar ro'yxati")
    st.checkbox("Yangi marketing strategiyasini tasdiqlash", value=True)
    st.checkbox("Moliyaviy chorak hisobotini ko'rib chiqish")
    st.checkbox("Katta mijoz bilan shartnoma imzolash")
