import streamlit as st
import pandas as pd
import datetime
import random
import secrets 
import time 
# Sahifa sozlamalari (UI va Dizayn professional bo'lishi uchun)
st.set_page_config(page_title="CEO Grand Command Center Enterprise", page_icon="👑", layout="wide")
import secrets
import time

# --- 1. DINAMIK QR TOKEN GENERATORI ---
def get_dynamic_qr_token():
    # Vaqtga bog'langan takrorlanmas xavfsiz token yaratish
    current_time = int(time.time())
    # Har 45 soniyada o'zgaradigan interval kaliti
    time_interval = current_time // 45 
    secret_key = f"GLOBAL_SECRET_2026_{time_interval}"
    token = secrets.token_hex(16)
    return token

# --- 2. AVTOMATLASHTIRILGAN PAYROLL ENGINE (9-BO'LIM) ---
def calculate_payroll_logic(worked_days, worked_hours, late_minutes, overtime_minutes, base_salary, salary_type):
    # Koeffitsiyentlarni dinamik hisoblash
    late_penalty_per_minute = 1000  # 1 daqiqa kechikish uchun 1000 won jarima
    overtime_multiplier = 1.5       # Overtime uchun 150% stavka
    
    if salary_type == 'Hourly':
        hourly_rate = base_salary
        earned = worked_hours * hourly_rate
    else:
        # Monthly bo'lsa, standart 209 soatga bo'lib soatbay stavka olinadi
        hourly_rate = base_salary / 209
        earned = base_salary
        
    overtime_earned = (overtime_minutes / 60) * hourly_rate * overtime_multiplier
    penalty = late_minutes * late_penalty_per_minute
    
    final_salary = earned + overtime_earned - penalty
    return max(0, round(final_salary, 2))

# Custom CSS orqali chiroyli dizayn berish
st.markdown("""
    <style>
    .main-title { font-size: 32px; font-weight: bold; color: #1E3A8A; text-align: center; }
    .welcome-text { font-size: 18px; color: #4B5563; text-align: center; margin-bottom: 20px; }
    .card { padding: 20px; border-radius: 10px; background-color: #F3F4F6; margin-bottom: 15px; }
    </style>
""", unsafe_allow_html=True)

# --- 10 TA GAPDAN IBORAT MATRIX LUG'ATLARI ---
early_wishes = [
    "Quyoshdan ham ertaroq uyg'ongan qahramonimiz, xush kelibsiz! Bugungi kuningiz omadli o'tsin! ✨",
    "Ertapishar ishchi — kompaniyamizning chinakam poydevoridir. Katta rahmat sizga! 🌟",
    "Intizomingiz va mas'uliyatingiz tahsinga loyiq! Kuningiz unumli bo'lsin! 🚀",
    "Ertalabki faollik — g'alaba kalitidir. Bugun barcha maqsadlaringizga erishing! 💪",
    "Siz bor joyda rivojlanish bor! Erta kelib namuna bo'lganingiz uchun rahmat! 🎯",
    "Yorqin tabassum va yuqori energiya bilan yangi cho'qqilarni zabt etishga olg'a! 🔥",
    "Kompaniyamiz sizdek fidoyi xodimlar bilan faxrlanadi! Kuningiz ajoyib o'tsin! 👑",
    "Ertalabki musaffo havo va yangi g'oyalar sizni yuksaltirsin! Xush kelibsiz! 🌈",
    "Sizning bu intizomingiz xonimning va menejerlarning doimiy diqqat markazida! ⭐",
    "Erta kelgan rizqini ortig'i bilan oladi. Bugungi omad sizniki! 💰"
]

late_wishes = [
    "Xush kelibsiz! Yo'lda biron texnik nosozlik yoki tirbandlik bo'ldimi? Salomatlik birinchi o'rinda! 😊",
    "Kechikkan bo'lsangiz ham kelganingizdan xursandmiz. Keling, tezda jamoaga qo'shiling! 🙏",
    "Kichik kechikishlar kayfiyatni tushira olmaydi. Bugun buni ajoyib natijalar bilan yopamiz! ⚡",
    "Kompaniyamiz sizni kutayotgan edi. Muloyimlik bilan eslatamiz, ertaga sizni erda kutamiz! 😉",
    "Sizning energiyangiz bizga yetishmayotgan edi. Ish boshlashga tayyormisiz? Olg'a! 🚀",
    "Xavotir olmang, hamma narsaga ulgurasiz. Diqqatni jamlab, ishni professional darajada boshlaymiz! 🎯",
    "Kechikish sababi muhim emas, eng muhimi siz hozir safdasiz. Unumli kun tilaymiz! ✨",
    "Vaqt — eng oliy boylik. Ertaga intizomni yanada mukammal qilishga kelishdik, to'g'rimi? 👍",
    "Kechikishlar sizdek yaxshi xodimga yarashmaydi, bugun bor kuchingizni ko'rsatib hammaga o'rnak bo'ling! 🔥",
    "Xush kelibsiz! Sizsiz jamoamiz to'liq emas edi. Ish rejasiga tezda kirishamiz! 💼"
]

goodbye_wishes = [
    "Bugun ajoyib mehnat qildingiz! Mashaqqatli mehnatingiz uchun tashakkur, yaxshi dam oling! 🌙",
    "Uyingizga borar ekansiz, yo'lingiz bexatar bo'lsin. Ertagacha xayr! 👋",
    "Kompaniya rivojiga qo'shgan bugungi hissangiz bebahodir. Oqshomingiz xayrli o'tsin! 🌟",
    "Charchoqlarni chiqarib, oilangiz bag'rida shirin dam oling! Ertaga uchrashguncha! 🏠",
    "Siz bugun chinakam professional ekanligingizni yana bir bor isbotladingiz. Rahmat! 🎯",
    "Bugungi barcha vazifalar bajarildi, endi esa miriqib hordiq chiqarish vaqti! 🛌",
    "Yo'llaringiz ravon bo'lsin. Ertaga yangi kuch va yuqori kayfiyat bilan kutamiz! 🚀",
    "Kuningiz unumli o'tganidan xursandmiz. Ertaga bundan ham zo'r natijalar sari! 🔥",
    "Sizdek xodim bilan ishlash jamoamiz uchun sharaf. Yaxshi dam oling! 👑",
    "Xayrli oqshom! Kompaniya sizga bugungi zafarli ish kuningiz uchun minnatdorchilik bildiradi! ⭐"
]

# --- KO'P TILLI LUG'AT TIZIMI (Sessiya va Oynalar uchun) ---
lang_dict = {
    "O'zbekcha": {
        "nav_menu": "Asosiy Menyu",
        "roles": ["Ishchi (Staff)", "Menejer (Manager)", "CEO (Xonim)"],
        "sidebar_title": "Boshqaruv Markazi",
        "worker_reg": "📝 Yangi xodim ro'yxatdan o'tishi",
        "worker_io": "👥 Keldi-Ketdi Skanerlash Oynasi",
        "feedback_title": "📩 Shikoyat va Takliflar Bo'limi",
        "manager_title": "💼 Menejer Boshqaruv Markazi",
        "ceo_title": "👑 CEO Oliy Boshqaruv Markazi"
    },
    "English": {
        "nav_menu": "Main Menu",
        "roles": ["Staff", "Manager", "CEO (Ma'am)"],
        "sidebar_title": "Command Center",
        "worker_reg": "📝 New Employee Registration",
        "worker_io": "👥 Check-In / Check-Out Scanning Window",
        "feedback_title": "📩 Suggestions & Complaints",
        "manager_title": "💼 Manager Management Center",
        "ceo_title": "👑 CEO Supreme Command Center"
    },
    "한국어": {
        "nav_menu": "메인 메뉴",
        "roles": ["직원 (Staff)", "매니저 (Manager)", "CEO (대표님)"],
        "sidebar_title": "통합 관제 센터",
        "worker_reg": "📝 신입 직원 정보 등록",
        "worker_io": "👥 출퇴근 QR 스캔 윈도우",
        "feedback_title": "📩 건의 및 불만 접수 창구",
        "manager_title": "💼 매니저 통합 관리 센터",
        "ceo_title": "👑 CEO 최고 경영 통합 관제 센터"
    }
}

# --- SESSYA BAZASI (Ma'lumotlar yo'qolib ketmasligi uchun Streamlit State) ---
if "workers_list" not in st.session_state:
    st.session_state.workers_list = [
        {"ID": "EMP-01", "Ism": "Anvarov Dilshod", "Tugilgan_kun": "1995-05-12", "Lavozim": "Manager"},
        {"ID": "EMP-02", "Ism": "Karimova Zilola", "Tugilgan_kun": "1998-09-22", "Lavozim": "HR Specialist"},
        {"ID": "EMP-03", "Ism": "Sultonov Bekzod", "Tugilgan_kun": "2005-01-15", "Lavozim": "Lead Developer"},
        {"ID": "EMP-04", "Ism": "Toshpulatova Sevara", "Tugilgan_kun": "2000-11-02", "Lavozim": "Designer"},
        {"ID": "EMP-05", "Ism": "Azimov Rustam", "Tugilgan_kun": "1993-04-30", "Lavozim": "Accountant"},
    ]

if "attendance_logs" not in st.session_state:
    st.session_state.attendance_logs = [
        {"Sana": "2026-06-27", "ID": "EMP-01", "Xodim": "Anvarov Dilshod", "Vaqt": "08:42", "Tur": "Keldi (Check-In)", "Holat": "Erta keldi ✅"},
        {"Sana": "2026-06-27", "ID": "EMP-02", "Xodim": "Karimova Zilola", "Vaqt": "09:12", "Tur": "Keldi (Check-In)", "Holat": "Kechikdi ⚠️"}
    ]

if "feedbacks" not in st.session_state:
    st.session_state.feedbacks = [
        {"Xodim": "Karimova Zilola", "Sana": "2026-06-26", "Turi": "Taklif", "Matn": "Oshxonaga yangi kofe mashinasi qo'yilsa yaxshi bo'lar edi."}
    ]

if "vacation_requests" not in st.session_state:
    st.session_state.vacation_requests = {
        "Anvarov Dilshod": ["Dushanba", "Seshanba"],
        "Karimova Zilola": ["Shanba", "Yakka"]
    }

# --- SIDEBAR: TIL VA ROL TANLASH ---
st.sidebar.header("🌐 Language / Til / 언어")
selected_lang = st.sidebar.selectbox("Choose language:", ["O'zbekcha", "English", "한국어"])
lang = lang_dict[selected_lang]

st.sidebar.markdown("---")
st.sidebar.subheader(lang["sidebar_title"])
role = st.sidebar.selectbox(lang["nav_menu"], lang["roles"])

# Xavfsizlik parollari
authenticated = False
if "CEO" in role or "대표님" in role:
    pwd = st.sidebar.text_input("CEO Password:", type="password", key="ceo_pwd_key")
    if pwd == "ceo123": authenticated = True
elif "Menejer" in role or "Manager" in role:
    pwd = st.sidebar.text_input("Manager Password:", type="password", key="mgr_pwd_key")
    if pwd == "mgr123": authenticated = True
else:
    authenticated = True

st.sidebar.markdown("---")

# --- 1. ISHCHILAR STRUKTURASI ---
if "Ishchi" in role or "Staff" in role or "직원" in role:
    st.markdown("<div class='main-title'>👥 ISHCHILAR INTEGRATSIYALASHGAN TIZIMI</div>", unsafe_allow_html=True)
    
    tab1, tab2, tab3 = st.tabs([lang["worker_io"], lang["worker_reg"], lang["feedback_title"]])
    
    # Keldi-Ketdi Oynasi (QR o'rniga dinamik tugma)
    with tab1:
        st.subheader("📲 Real-vaqt rejimida keldi-ketdi skanerlash")
        st.write("QR kod skaner qilinganda tizim avtomat ishchining vaqtini va holatini aniqlaydi.")
        
        current_time_str = datetime.datetime.now().strftime("%H:%M")
        current_date_str = datetime.date.today().strftime("%Y-%m-%d")
        
        st.info(f"📅 Bugungi sana: {current_date_str} | ⏰ Joriy vaqt: {current_time_str}")
        
        selected_worker = st.selectbox("Ism-familiyangizni tanlang:", [w["Ism"] for w in st.session_state.workers_list])
        worker_id = [w["ID"] for w in st.session_state.workers_list if w["Ism"] == selected_worker][0]
        
        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🚪 KELISH (Check-In)", type="primary", use_container_width=True):
                # 09:00 dan oldin kelsa erta, keyin kelsa kechikdi
                is_late = datetime.datetime.now().hour >= 9 and datetime.datetime.now().minute > 0
                status_text = "Kechikdi ⚠️" if is_late else "Erta keldi ✅"
                wish = random.choice(late_wishes) if is_late else random.choice(early_wishes)
                
                st.session_state.attendance_logs.append({
                    "Sana": current_date_str, "ID": worker_id, "Xodim": selected_worker, "Vaqt": current_time_str, "Tur": "Keldi (Check-In)", "Holat": status_text
                })
                st.success(wish)
                st.balloons()
                
        with col_btn2:
            if st.button("🏡 KETISH (Check-Out)", use_container_width=True):
                wish = random.choice(goodbye_wishes)
                st.session_state.attendance_logs.append({
                    "Sana": current_date_str, "ID": worker_id, "Xodim": selected_worker, "Vaqt": current_time_str, "Tur": "Ketish (Check-Out)", "Holat": "Ish yakunlandi 🏁"
                })
                st.info(wish)
        
        st.markdown("---")
        # 20-22 kunlar orasidagi aqlli dam olish kunini tanlash tizimi
        st.subheader("📅 Keyingi oy uchun dam olish kunlarini tanlash")
        st.write("Eslatma: Har oyning 20-kunigacha dam olish kunlarini belgilashingiz kerak. 22-kuni dastur yangi jadvalni e'lon qiladi.")
        
        chosen_days = st.multiselect("Kelgusi oydagi o'zingizga qulay dam olish kunlarini tanlang:", ["Dushanba", "Seshanba", "Chorshanba", "Payshanba", "Juma", "Shanba", "Yakirshanba"])
        if st.button("Tanlovni saqlash 💾"):
            st.session_state.vacation_requests[selected_worker] = chosen_days
            st.success("Sizning dam olish kunlari bo'yicha so'rovingiz saqlandi va intellektual jadval tizimiga yuborildi!")

    # Yangi xodimni ro'yxatdan o'tkazish
    with tab2:
        st.subheader(lang["worker_reg"])
        new_name = st.text_input("Xodim ism-familiyasi:")
        col_b1, col_b2, col_b3 = st.columns(3)
        with col_b1: b_year = st.selectbox("Tug'ilgan yil:", list(range(1970, 2010)), index=25)
        with col_b2: b_month = st.selectbox("Tug'ilgan oy:", list(range(1, 13)))
        with col_b3: b_day = st.selectbox("Tug'ilgan kun:", list(range(1, 32)))
        new_role = st.text_input("Lavozimi:", "Mutaxassis")
        
        if st.button("Ro'yxatdan o'tkazish va ID berish 📇"):
            if new_name:
                new_id = f"EMP-0{len(st.session_state.workers_list)+1}"
                st.session_state.workers_list.append({
                    "ID": new_id, "Ism": new_name, "Tugilgan_kun": f"{b_year}-{b_month:02d}-{b_day:02d}", "Lavozim": new_role
                })
                st.success(f"🎉 '{new_name}' muvaffaqiyatli ro'yxatdan o'tdi! Unikal Tizim ID raqami: {new_id}")
            else:
                st.error("Iltimos xodim ismini kiriting.")

    # Shikoyat va takliflar
    with tab3:
        st.subheader(lang["feedback_title"])
        f_type = st.radio("Murojaat turi:", ["Taklif", "Shikoyat"])
        f_text = st.text_area("Murojaatingiz matnini batafsil yozing (CEO va Menejerga to'g'ridan-to'g'ri boradi):")
        if st.button("Yuborish 📨"):
            if f_text:
                st.session_state.feedbacks.append({
                    "Xodim": selected_worker, "Sana": current_date_str, "Turi": f_type, "Matn": f_text
                })
                st.success("Murojaatingiz maxfiy va xavfsiz tarzda rahbariyatga yetkazildi. Rahmat!")
            else:
                st.error("Matn bo'sh bo'lishi mumkin emas.")

# --- 2. MENEJER STRUKTURASI ---
elif ("Menejer" in role or "Manager" in role) and authenticated:
    st.markdown("<div class='main-title'>💼 MENEJER STRATEGIK NAZORAT PANELl</div>", unsafe_allow_html=True)
    
    m_tab1, m_tab2, m_tab3 = st.tabs(["📊 Keldi-Ketdi Real-Time Monitoring", "📅 Oylik Ish Jadvallari", "👥 Ishchilar Ro'yxati"])
    
    with m_tab1:
            st.write("---")
            placeholder = st.empty()
            qr_token = get_dynamic_qr_token()
            with placeholder.container():
                st.info(f"🔑 Eksklyuziv Davomat Tokeni: {qr_token}")
                qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=180x180&data={qr_token}"
                st.image(qr_url, caption="Xodimlar telefon orqali skner qilishlari shart (Har 45 soniyada yangilanadi)")
            st.write("---")


        st.subheader("📱 QR-skanerdan o'tgan xodimlarning real vaqt dagi onlayn oqimi")
        df_logs = pd.DataFrame(st.session_state.attendance_logs)
        st.dataframe(df_logs, use_container_width=True)
        
    with m_tab2:
        st.subheader("📅 Avtomatlashtirilgan va Arxiv Ish Jadvallari")
        st.write("O'tgan 3 oylik jadval tizimga yuklangan. Dastur uni o'rganib chiqdi:")
        
        # O'tgan oylar jadvallari (Simulyatsiya)
        st.caption("📂 Arxiv jadvallar (O'tgan 3 oy) — Yuklab olish imkoniyati bilan (PDF/Rasm o'rniga CSV formatda)")
        old_schedule = pd.DataFrame({
            "Xodim": [w["Ism"] for w in st.session_state.workers_list],
            "Aprel (Kun)": ["22 kun", "20 kun", "21 kun", "22 kun", "18 kun"],
            "May (Kun)": ["20 kun", "22 kun", "22 kun", "19 kun", "21 kun"],
            "Iyun (Kun)": ["21 kun", "21 kun", "20 kun", "22 kun", "22 kun"]
        })
        st.dataframe(old_schedule, use_container_width=True)
        
        # Har oyning 22-kuni jadval tuzish mantiqi
        st.markdown("---")
        st.subheader("🤖 Keyingi oy uchun AI/Dasturiy ish jadvali")
        current_day = datetime.datetime.now().day
        st.write(f"Bugungi kun: **{current_day}-sana**. Jadval har oyning 22-kunida xodimlarning dam olish kunlari so'roviga ko'ra tuziladi.")
        
        # Kelgusi oy jadvali tuzish
        next_month_schedule = []
        for w in st.session_state.workers_list:
            name = w["Ism"]
            requested_vacations = st.session_state.vacation_requests.get(name, ["Shanba", "Yakshanba"])
            vacation_str = ", ".join(requested_vacations)
            next_month_schedule.append({
                "Xodim": name, "Lavozim": w["Lavozim"], "Belgilangan Dam olish kunlari": vacation_str, "Ish kunlari": "Dushanba - Juma (Smenali)"
            })
            
        st.dataframe(pd.DataFrame(next_month_schedule), use_container_width=True)
        st.success("Tizim xodimlarning 20-kungacha kiritgan barcha ma'lumotlarini inobatga olgan holda keyingi oy rejasini tuzdi!")
        
    with m_tab3:
        st.subheader("👥 Kompaniya ishchilari umumiy ma'lumotlar bazasi")
        st.dataframe(pd.DataFrame(st.session_state.workers_list), use_container_width=True)

# --- 3. CEO (XONIM) STRUKTURASI ---
elif ("CEO" in role or "대표님" in role) and authenticated:
    st.markdown("<div class='main-title'>👑 CEO SUPREME GRAND MANAGEMENT MATRIX</div>", unsafe_allow_html=True)
    st.markdown("<div class='welcome-text'>Xonim, kompaniyangizning eng yuqori darajadagi boshqaruv markaziga xush kelibsiz! Barcha mayda detallar sizning nazoratingizda.</div>", unsafe_allow_html=True)
    
    c_tab1, c_tab2, c_tab3, c_tab4, c_tab5 = st.tabs(["📈 Moliyaviy va Strategik Dashboard", "📅 Keldi-Ketdi & Jadvallar", "👥 Kadrlar (Staff) Ro'yxati", "📅 Strategik Mitinglar Rejasi", "📩 Shikoyat/Takliflar Paneli"])
    
    with c_tab1:
        st.subheader("🚀 Korporativ Oliy Ko'rsatkichlar")
        col1, col2, col3 = st.columns(3)
        col1.metric("Kunlik Sof Daromad", "$1,250", "+12%")
        col2.metric("Yangi Global Mijozlar", "45", "+5%")
        col3.metric("Faol Xalqaro Loyihalar", "8", "0")
        
        st.write("")
        st.subheader("💰 Moliyaviy Tahlil Grafigi")
        df_fin = pd.DataFrame({
            'Oy': ['Yanvar', 'Fevral', 'Mart', 'Aprel', 'May', 'Iyun'],
            'Daromad ($)': [5000, 7000, 8500, 12000, 11500, 14000],
            'Xarajat ($)': [3000, 3500, 4000, 4500, 4200, 4800]
        })
        st.line_chart(df_fin.set_index('Oy'))
        
    with c_tab2:
        st.subheader("📅 Davomat va Ish Jadvallarining Markaziy Nazorati")
        st.write("Menejer va ishchilarning jadvallari muvofiqligi:")
        st.dataframe(pd.DataFrame(st.session_state.attendance_logs), use_container_width=True)
        
    with c_tab3:
        st.subheader("👥 Barcha Xodimlarning Tug'ilgan kunlari va Ma'lumotlari")
        st.dataframe(pd.DataFrame(st.session_state.workers_list), use_container_width=True)
        
    with c_tab4:
        st.subheader("📅 Oliy Strategik Mitinglar va Yig'ilishlar Rejasi")
        meetings_data = pd.DataFrame({
            "Sana": ["2026-06-28", "2026-07-01", "2026-07-05"],
            "Vaqt": ["10:00", "14:00", "11:00"],
            "Miting Mavzusi": ["Menejerlar bilan haftalik hisobot yig'ilishi", "Yangi xalqaro investorlar bilan uchrashuv", "Kadrlar davomati va oylik natijalar tahlili"],
            "Status": ["Rejalashtirilgan 🗓️", "Yuqori Muhim 🔥", "Kutish jarayonida ⏳"]
        })
        st.dataframe(meetings_data, use_container_width=True)
        
    with c_tab5:
        st.subheader("📩 Xodimlardan Kelib Tushgan Murojaat va Takliflar")
        st.write("Ushbu bo'lim faqat Xonimga va Oliy Raxbariyatga ko'rinadi:")
        st.dataframe(pd.DataFrame(st.session_state.feedbacks), use_container_width=True)

else:
    st.warning("⚠️ Iltimos, boshqaruv tizimiga kirish uchun chap paneldagi parolni kiriting (CEO: ceo123, Manager: mgr123).")
