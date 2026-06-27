import streamlit as st
import pandas as pd
import datetime

# Sahifa sozlamalari
st.set_page_config(page_title="CEO Grand Command Center", page_icon="👑", layout="wide")

# Tillarni sozlash lug'ati
lang_dict = {
    "O'zbekcha": {
        "title": "👑 CEO Executive Grand Center",
        "welcome": "Xonim, kompaniyangizning oliy boshqaruv markaziga xush kelibsiz!",
        "nav_header": "Asosiy Menyu",
        "nav_choose": "Bo'limni tanlang:",
        "menu": ["CEO Dashboard", "Keldi-Ketdi Nazorati (10 ishchi)", "QR-Kod Menejer", "Moliyaviy Hisobot"],
        "metrics_title": "🚀 Bugungi Oliy Ko'rsatkichlar",
        "metric_1": "Kunlik Daromad",
        "metric_2": "Yangi Mijozlar",
        "metric_3": "Faol Loyihalar",
        "system_status": "Tizim barqaror ishlamoqda. Barcha departamentlar nazorat ostida.",
        "attendance_title": "👥 Ishchilar Keldi-Ketdi Jadvali",
        "attendance_desc": "Bugungi sana bo'yicha 10 ta asosiy xodimning davomati va holati:",
        "qr_title": "📱 QR-Kod Menejer Oynasi",
        "qr_desc": "Xonim, bu yerda tizim uchun yangi QR kodlar yaratishingiz yoki mavjudlarini boshqarishingiz mumkin.",
        "qr_btn": "Yangi QR Kod Generatsiya Qilish",
        "finance_title": "💰 Kompaniya Moliyaviy Tahlili",
        "finance_desc": "Oylik daromad va xarajatlar grafigi:"
    },
    "English": {
        "title": "👑 CEO Executive Grand Center",
        "welcome": "Welcome to your Supreme Command Center, Ma'am!",
        "nav_header": "Main Menu",
        "nav_choose": "Select a section:",
        "menu": ["CEO Dashboard", "Attendance Control (10 Staff)", "QR-Code Manager", "Financial Report"],
        "metrics_title": "🚀 Key Metrics for Today",
        "metric_1": "Daily Revenue",
        "metric_2": "New Customers",
        "metric_3": "Active Projects",
        "system_status": "System is running smoothly. All departments are under control.",
        "attendance_title": "👥 Staff Attendance Matrix",
        "attendance_desc": "Attendance and status of the 10 core employees for today:",
        "qr_title": "📱 QR-Code Manager Panel",
        "qr_desc": "Ma'am, here you can generate new system QR codes or manage existing ones.",
        "qr_btn": "Generate New QR Code",
        "finance_title": "💰 Corporate Financial Analysis",
        "finance_desc": "Monthly revenue and expenses chart:"
    },
    "한국어": {
        "title": "👑 CEO 최고 경영 관리 센터",
        "welcome": "대표님, 회사 최고 경영 통합 관제 센터에 오신 것을 환영합니다!",
        "nav_header": "메인 메뉴",
        "nav_choose": "메뉴를 선택하세요:",
        "menu": ["CEO 대시보드", "근태 관리 (10명 직원)", "QR코드 매니저", "재무 보고서"],
        "metrics_title": "🚀 오늘의 주요 경영 지표",
        "metric_1": "일일 매출",
        "metric_2": "신규 고객",
        "metric_3": "진행 중인 프로젝트",
        "system_status": "시스템이 안정적으로 작동 중입니다. 모든 부서가 통제 하에 있습니다.",
        "attendance_title": "👥 직원 출퇴근 및 근태 현황",
        "attendance_desc": "오늘 기준 핵심 직원 10명의 출근 시간 및 상태:",
        "qr_title": "📱 QR코드 매니저 윈도우",
        "qr_desc": "대표님, 이곳에서 시스템용 새 QR 코드를 생성하거나 기존 코드를 관리할 수 있습니다.",
        "qr_btn": "새 QR 코드 생성하기",
        "finance_title": "💰 기업 재무 tahlil 보고서",
        "finance_desc": "월별 매출 및 지출 차트:"
    }
}

# Sidebar - Tilni tanlash qismi
st.sidebar.header("🌐 Language / Til / 언어")
selected_lang = st.sidebar.selectbox("Choose language:", ["O'zbekcha", "English", "한국어"])
lang = lang_dict[selected_lang]

st.sidebar.markdown("---")
st.sidebar.header(lang["nav_header"])
page = st.sidebar.radio(lang["nav_choose"], lang["menu"])

# Asosiy sarlavhalar (Doim tepada turadi)
st.title(lang["title"])
st.write(lang["welcome"])
st.markdown("---")

# 1-BO'LIM: CEO DASHBOARD
if page == lang["menu"][0]:
    st.subheader(lang["metrics_title"])
    col1, col2, col3 = st.columns(3)
    col1.metric(lang["metric_1"], "$1,250", "+12%")
    col2.metric(lang["metric_2"], "45", "+5%")
    col3.metric(lang["metric_3"], "8", "0")
    
    st.info(lang["system_status"])
    
    # Tezkor eslatma oynasi
    st.write("")
    st.subheader("📌 Executive Notes / Qaydlar")
    st.text_area("Xonim, bugungi muhim ko'rsatmalaringizni shu yerga yozib qo'yishingiz mumkin:", "1. Marketing guruhining hisobotini tekshirish.\n2. Yangi filial rejasini ko'rib chiqish.")

# 2-BO'LIM: KELDI-KETDI (10 TA ISHCHI)
elif page == lang["menu"][1]:
    st.subheader(lang["attendance_title"])
    st.write(lang["attendance_desc"])
    
    # 10 ta ishchi ma'lumotlari jadvallari
    workers_data = {
        "ID": [f"EMP-0{i}" for i in range(1, 11)],
        "Xodim (Staff)": [
            "Anvarov Dilshod", "Karimova Zilola", "Sultonov Bekzod", "Toshpulatova Sevara", 
            "Azimov Rustam", "Kim Min-ji", "Lee Jun-ho", "Park Soyun", "Smith John", "Alieva Madina"
        ],
        "Lavozimi (Role)": [
            "Manager", "HR Specialist", "Lead Developer", "Designer", "Accountant",
            "Korean Translator", "QA Engineer", "Project Manager", "Consultant", "CEO Assistant"
        ],
        "Kelgan Vaqti (Check-In)": [
            "08:45", "08:50", "08:58", "09:15 (Kechikdi)", "08:30", 
            "08:40", "08:55", "09:00", "08:52", "08:25"
        ],
        "Holati (Status)": [
            "Faol ✅", "Faol ✅", "Faol ✅", "Ogohlantirilgan ⚠️", "Faol ✅", 
            "Faol ✅", "Faol ✅", "Faol ✅", "Faol ✅", "Oliy Nazorat ⭐"
        ]
    }
    df_workers = pd.DataFrame(workers_data)
    st.dataframe(df_workers, use_container_width=True)

# 3-BO'LIM: QR-KOD MENEJER
elif page == lang["menu"][2]:
    st.subheader(lang["qr_title"])
    st.write(lang["qr_desc"])
    
    col_qr1, col_qr2 = st.columns([2, 1])
    with col_qr1:
        qr_name = st.text_input("QR kod nomini kiriting (Masalan: Bosh eshik, 2-omborxonasi):", "Asosiy Kirish QR")
        qr_type = st.selectbox("QR turi:", ["Xodimlarni ro'yxatga olish", "Maxfiy bo'limga ruxsat", "Mehmonlar uchun"])
        
        if st.button(lang["qr_btn"], type="primary"):
            st.success(f"🎉 '{qr_name}' muvaffaqiyatli yaratildi va tizimga ulandi!")
    
    with col_qr2:
        # Namuna sifatida chiroyli vizual quti
        st.write("🔍 **QR Preview / Ko'rinishi**")
        st.image("https://api.qrserver.com/v1/create-qr-code/?size=150x150&data=CEO_Grand_Center_Access", width=150)

# 4-BO'LIM: MOLIYAVIY HISOBOT
elif page == lang["menu"][3]:
    st.subheader(lang["finance_title"])
    st.write(lang["finance_desc"])
    
    finance_data = {
        'Month/Oy': ['Yanvar', 'Fevral', 'Mart', 'Aprel', 'May', 'Iyun'],
        'Daromad ($)': [5000, 7000, 8500, 12000, 11500, 14000],
        'Xarajat ($)': [3000, 3500, 4000, 4500, 4200, 4800]
    }
    df_fin = pd.DataFrame(finance_data)
    st.line_chart(df_fin.set_index('Month/Oy'))
    st.dataframe(df_fin, use_container_width=True)
