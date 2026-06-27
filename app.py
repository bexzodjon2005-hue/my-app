import streamlit as st
import pandas as pd
import datetime

# Sahifa sozlamalari
st.set_page_config(page_title="Kompaniya Boshqaruv Tizimi", page_icon="🏢", layout="wide")

# Tillarni sozlash lug'ati
lang_dict = {
    "O'zbekcha": {
        "login_title": "🔒 Tizimga kirish",
        "role_select": "Rolingizni tanlang:",
        "pass_label": "Parolni kiriting:",
        "login_btn": "Kirish",
        "worker_section": "👥 Ishchilar bo'limi (Ruxsat ochiq)",
        "worker_btn": "QR Kodni skner qildim (Keldim deb belgilash) ✅",
        "success_reg": "Muvaffaqiyatli ro'yxatga olindi!",
        "ceo_title": "👑 CEO Executive Grand Center",
        "mgr_title": "💼 Menejer Boshqaruv Paneli",
        "menu_ceo": ["CEO Dashboard", "Keldi-Ketdi Nazorati (10 ishchi)", "QR-Kod Menejer", "Moliyaviy Hisobot"],
        "menu_mgr": ["Keldi-Ketdi Nazorati (10 ishchi)", "QR-Kod Menejer"]
    },
    "English": {
        "login_title": "🔒 System Login",
        "role_select": "Select your role:",
        "pass_label": "Enter Password:",
        "login_btn": "Login",
        "worker_section": "👥 Staff Section (Public Access)",
        "worker_btn": "Scanned QR Code (Check-In) ✅",
        "success_reg": "Successfully registered!",
        "ceo_title": "👑 CEO Executive Grand Center",
        "mgr_title": "💼 Manager Control Panel",
        "menu_ceo": ["CEO Dashboard", "Attendance Control", "QR-Code Manager", "Financial Report"],
        "menu_mgr": ["Attendance Control", "QR-Code Manager"]
    },
    "한국어": {
        "login_title": "🔒 시스템 로그인",
        "role_select": "권한을 선택하세요:",
        "pass_label": "비밀번호를 입력하세요:",
        "login_btn": "로그인",
        "worker_section": "👥 직원 공간 (공개 접근)",
        "worker_btn": "QR 코드 스캔 완료 (출근 등록) ✅",
        "success_reg": "출근이 성공적으로 등록되었습니다!",
        "ceo_title": "👑 CEO 최고 경영 관리 센터",
        "mgr_title": "💼 매니저 관리 창",
        "menu_ceo": ["CEO 대시보드", "근태 관리 (10명)", "QR코드 매니저", "재무 보고서"],
        "menu_mgr": ["근태 관리 (10명)", "QR코드 매니저"]
    }
}

# Sidebar - Tilni tanlash
st.sidebar.header("🌐 Language / Til / 언어")
selected_lang = st.sidebar.selectbox("Choose language:", ["O'zbekcha", "English", "한국어"])
lang = lang_dict[selected_lang]

st.sidebar.markdown("---")
st.sidebar.subheader(lang["login_title"])

# Rolni tanlash
role = st.sidebar.selectbox(lang["role_select"], ["Ishchi (Staff)", "Menejer (Manager)", "CEO (Xonim)"])

# Parol tizimi (Sodda xavfsizlik)
authenticated = False
if role == "CEO (Xonim)":
    password = st.sidebar.text_input(lang["pass_label"], type="password", key="ceo_p")
    if password == "ceo123":  # Xonim uchun parol
        authenticated = True
    elif password:
        st.sidebar.error("Xato parol!")
elif role == "Menejer (Manager)":
    password = st.sidebar.text_input(lang["pass_label"], type="password", key="mgr_p")
    if password == "mgr123":  # Menejer uchun parol
        authenticated = True
    elif password:
        st.sidebar.error("Xato parol!")
else:
    authenticated = True  # Ishchilarga parol shart emas

st.sidebar.markdown("---")

# --- INTERFEYS MANTIQLARI ---

# 1. ISHCHILAR OYNASI (Parolsiz kirganda)
if role == "Ishchi (Staff)":
    st.title(lang["worker_section"])
    st.write("Xodimlar kelgan vaqtda QR kodni skanerlab yoki quyidagi tugmani bosib davomatdan o'tadilar:")
    
    col_w1, col_w2 = st.columns([2, 1])
    with col_w1:
        worker_name = st.selectbox("Ism-familiyangizni tanlang:", [
            "Anvarov Dilshod", "Karimova Zilola", "Sultonov Bekzod", "Toshpulatova Sevara", 
            "Azimov Rustam", "Smith John", "Alieva Madina"
        ])
        if st.button(lang["worker_btn"], type="primary"):
            st.balloons()
            st.success(f"🎉 {worker_name} — {lang['success_reg']} (Vaqt: {datetime.datetime.now().strftime('%H:%M')})")
    with col_w2:
        st.write("📷 **Skanerlash uchun QR kod matni:**")
        st.image("https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=STAFF_CHECKIN", width=150)

# 2. MENEJER YOKI CEO OYNASI (Faqat to'g'ri parol yozilganda ochiladi)
elif authenticated:
    if role == "CEO (Xonim)":
        st.title(lang["ceo_title"])
        menu = lang["menu_ceo"]
    else:
        st.title(lang["mgr_title"])
        menu = lang["menu_mgr"]
        
    page = st.sidebar.radio("Bo'limlar:", menu)
    
    # Keldi-ketdi jadvali (Menejer va CEO ko'ra oladi)
    if "Keldi-Ketdi" in page or "Attendance" in page or "근태" in page:
        st.subheader("👥 Ishchilar Davomati Matrix")
        workers_data = {
            "ID": [f"EMP-0{i}" for i in range(1, 11)],
            "Xodim (Staff)": ["Anvarov Dilshod", "Karimova Zilola", "Sultonov Bekzod", "Toshpulatova Sevara", "Azimov Rustam", "Kim Min-ji", "Lee Jun-ho", "Park Soyun", "Smith John", "Alieva Madina"],
            "Lavozimi (Role)": ["Manager", "HR Specialist", "Lead Developer", "Designer", "Accountant", "Korean Translator", "QA Engineer", "Project Manager", "Consultant", "CEO Assistant"],
            "Kelgan Vaqti": ["08:45", "08:50", "08:58", "09:15", "08:30", "08:40", "08:55", "09:00", "08:52", "08:25"],
            "Holati": ["Faol ✅", "Faol ✅", "Faol ✅", "Kechikdi ⚠️", "Faol ✅", "Faol ✅", "Faol ✅", "Faol ✅", "Faol ✅", "Oliy Nazorat ⭐"]
        }
        st.dataframe(pd.DataFrame(workers_data), use_container_width=True)
        
    # QR kod boshqaruvi (Menejer va CEO ko'ra oladi)
    elif "QR-Kod" in page or "QR-Code" in page or "QR코드" in page:
        st.subheader("📱 QR-Kod Menejer Paneli")
        qr_name = st.text_input("Yangi QR Kod Nomi:", "Omborxona ruxsatnomasi")
        if st.button("QR Kod yaratish"):
            st.success(f"'{qr_name}' muvaffaqiyatli yaratildi va bazaga qo'shildi!")
            st.image("https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=NEW_DYNAMIC_QR", width=150)
            
    # Faqat CEO ko'radigan qismlar (CEO Dashboard va Moliya)
    elif "CEO Dashboard" in page or "대시보드" in page:
        st.subheader("🚀 Bugungi Oliy Ko'rsatkichlar")
        col1, col2, col3 = st.columns(3)
        col1.metric("Kunlik Daromad", "$1,250", "+12%")
        col2.metric("Yangi Mijozlar", "45", "+5%")
        col3.metric("Faol Loyihalar", "8", "0")
        st.text_area("Xonim uchun maxsus qaydlar:", "Ertaga hamma bo'lim boshliqlari yig'ilsin.")
        
    elif "Moliyaviy" in page or "Financial" in page or "재무" in page:
        st.subheader("💰 Kompaniya Maxfiy Moliyaviy Tahlili")
        df_fin = pd.DataFrame({
            'Oy': ['Yanvar', 'Fevral', 'Mart', 'Aprel'],
            'Daromad ($)': [5000, 7000, 8500, 12000],
            'Xarajat ($)': [3000, 3500, 4000, 4500]
        })
        st.line_chart(df_fin.set_index('Oy'))
        st.dataframe(df_fin, use_container_width=True)

else:
    st.warning("⚠️ Iltimos, ushbu bo'limni ko'rish uchun chap menyudan parolni kiriting.")
