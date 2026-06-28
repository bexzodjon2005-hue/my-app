import streamlit as st
import pandas as pd
import datetime
import random

# 1. SAHIFA SOZLAMALARI
st.set_page_config(page_title="Integratsiyalashgan TIZIM", layout="wide")

# 2. DIZAYN VA CSS
st.markdown("""
    <style>
    .main-title { font-size: 30px; font-weight: bold; text-align: center; color: #2C3E50; }
    </style>
""", unsafe_allow_html=True)

# 3. KO'P TILLI LUG'AT (DICTIONARY)
lang_dict = {
    "O'zbekcha": {
        "nav_menu": "Asosiy Menyu",
        "roles": ["Ishchi (Staff)", "Menejer (Manager)", "CEO (Boshqaruv)"],
        "sidebar_title": "Boshqaruv Markazi",
        "worker_reg": "Yangi xodim ro'yxatdan o'tishi",
        "worker_io": "Keldi-Ketdi Skanerlash",
        "feedback_title": "Shikoyat va Takliflar",
        "manager_title": "Menejer Boshqaruv Markazi",
        "ceo_title": "CEO Oliy Boshqaruv",
        "check_in": "🚪 KELISH (Check-In)",
        "check_out": "🏠 KETISH (Check-Out)",
        "select_worker": "Ism-familiyangizni tanlang:",
        "save_btn": "Saqlash",
    },
    "English": {
        "nav_menu": "Main Menu",
        "roles": ["Staff", "Manager", "CEO"],
        "sidebar_title": "Command Center",
        "worker_reg": "New Employee Registration",
        "worker_io": "Check-In / Check-Out",
        "feedback_title": "Suggestions & Complaints",
        "manager_title": "Manager Management Center",
        "ceo_title": "CEO Supreme Command",
        "check_in": "🚪 CHECK-IN",
        "check_out": "🏠 CHECK-OUT",
        "select_worker": "Select your name:",
        "save_btn": "Save",
    },
    "한국어": {
        "nav_menu": "메인 메뉴",
        "roles": ["직원 (Staff)", "매니저 (Manager)", "CEO (대표)"],
        "sidebar_title": "통합 관제 센터",
        "worker_reg": "신입 직원 정보 등록",
        "worker_io": "출퇴근 QR 스캔 윈도우",
        "feedback_title": "건의 및 불만 접수",
        "manager_title": "매니저 통합 관리 센터",
        "ceo_title": "CEO 최고 경영 관제",
        "check_in": "🚪 출근 (Check-In)",
        "check_out": "🏠 퇴근 (Check-Out)",
        "select_worker": "직원 이름을 선택하세요:",
        "save_btn": "저장",
    }
}

# 4. SESSİYA BAZASINI YARATISH (Ma'lumotlar saqlanib qolishi uchun)
if 'lang' not in st.session_state:
    st.session_state.lang = "O'zbekcha"

if "workers_list" not in st.session_state:
    st.session_state.workers_list = [
        {"ID": "EMP-01", "Ism": "Anvarov Dilshod", "Tugilgan_sana": "1990-05-15"},
        {"ID": "EMP-02", "Ism": "Karimova Zilola", "Tugilgan_sana": "1995-08-22"},
        {"ID": "EMP-03", "Ism": "Sultonov Bekzod", "Tugilgan_sana": "1992-11-10"}
    ]

if "attendance_logs" not in st.session_state:
    st.session_state.attendance_logs = []

if "feedbacks" not in st.session_state:
    st.session_state.feedbacks = []

if "vacation_requests" not in st.session_state:
    st.session_state.vacation_requests = {}

# Tilni sessiyadan o'qib olish
lang = st.session_state.lang

# 5. YON MENYU (SIDEBAR) VA TIL SOZLAMALARI
st.sidebar.title("🌍 Til / Language / 언어")
lang_options = ["O'zbekcha", "English", "한국어"]
selected_lang = st.sidebar.selectbox("", lang_options, index=lang_options.index(lang))

if selected_lang != lang:
    st.session_state.lang = selected_lang
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.subheader(lang_dict[lang]["sidebar_title"])
role = st.sidebar.selectbox(lang_dict[lang]["nav_menu"], lang_dict[lang]["roles"])

# 6. PAROL TIZIMI (Manager va CEO uchun)
authenticated = False
if "Manager" in role or "매니저" in role or "Menejer" in role:
    pwd = st.sidebar.text_input("Parol (Password):", type="password")
    if pwd == "mgr123":
        authenticated = True
elif "CEO" in role or "대표" in role or "Boshqaruv" in role:
    pwd = st.sidebar.text_input("Parol (Password):", type="password")
    if pwd == "ceo123":
        authenticated = True
else:
    authenticated = True # Ishchilar (Staff) uchun parol talab qilinmaydi

st.sidebar.markdown("---")
if authenticated:
    # --- 1. ISHCHILAR STRUKTURASI ---
    if "Ishchi" in role or "Staff" in role or "직원" in role:
        st.markdown("<div class='main-title'>👥 ISHCHILAR TIZIMI</div>", unsafe_allow_html=True)
        st.markdown("---")

        # Tablarni lug'atdan chaqiramiz
        tab1, tab2, tab3 = st.tabs([
            lang_dict[lang]["worker_io"], 
            lang_dict[lang]["worker_reg"], 
            lang_dict[lang]["feedback_title"]
        ])

        # ==========================================
        # TAB 1: KELDI-KETDI OYNASI
        # ==========================================
        with tab1:
            st.subheader(f"📲 {lang_dict[lang]['worker_io']}")
            
            # Vaqt va sanani aniqlash
            current_time_str = datetime.datetime.now().strftime("%H:%M")
            current_date_str = datetime.date.today().strftime("%Y-%m-%d")
            
            st.info(f"📅 {current_date_str} | ⏰ {current_time_str}")

            # Xodimni tanlash (Dinamik ro'yxatdan)
            selected_worker = st.selectbox(
                lang_dict[lang]["select_worker"], 
                [w["Ism"] for w in st.session_state.workers_list]
            )
            
            # Tanlangan xodimning ID sini topish
            worker_id = [w["ID"] for w in st.session_state.workers_list if w["Ism"] == selected_worker][0]

            # Tugmalar uchun 2 ta ustun
            col_btn1, col_btn2 = st.columns(2)

            with col_btn1:
                # KELISH TUGMASI
                if st.button(lang_dict[lang]["check_in"], type="primary", use_container_width=True):
                    # Kechikkanlikni tekshirish (09:00 dan keyin)
                    is_late = datetime.datetime.now().hour >= 9 and datetime.datetime.now().minute > 0
                    status_text = "Kechikdi ⚠️" if is_late else "Erta keldi ✅"
                    
                    # Ma'lumotlar bazasiga yozish
                    st.session_state.attendance_logs.append({
                        "Sana": current_date_str,
                        "ID": worker_id,
                        "Xodim": selected_worker,
                        "Vaqt": current_time_str,
                        "Holat": f"KELDI ({status_text})"
                    })
                    st.success(f"✅ {selected_worker} tizimga kirdi ({current_time_str})")
                    st.balloons()

            with col_btn2:
                # KETISH TUGMASI
                if st.button(lang_dict[lang]["check_out"], use_container_width=True):
                    # Ma'lumotlar bazasiga yozish
                    st.session_state.attendance_logs.append({
                        "Sana": current_date_str,
                        "ID": worker_id,
                        "Xodim": selected_worker,
                        "Vaqt": current_time_str,
                        "Holat": "KETDI 🏠"
                    })
                    st.info(f"🏠 {selected_worker} tizimdan chiqdi ({current_time_str})")
            
            st.markdown("---")
            
            # Dam olish kuni so'rovi
            st.write("📅 Keyingi oy uchun dam olish kunlarini tanlang (20-kunigacha):")
            chosen_days = st.multiselect("Dam olish kunlari:", [str(i) for i in range(1, 32)])
            
            if st.button(lang_dict[lang]["save_btn"], key="save_vacation"):
                st.session_state.vacation_requests[selected_worker] = chosen_days
                st.success("Yuborildi! ✅")

        # ==========================================
        # TAB 2: YANGI XODIM RO'YXATDAN O'TISHI
        # ==========================================
        with tab2:
            st.subheader(f"📝 {lang_dict[lang]['worker_reg']}")
            
            new_name = st.text_input("Xodim ism-familiyasi:")
            col_b1, col_b2, col_b3 = st.columns(3)
            
            with col_b1:
                b_year = st.selectbox("Tug'ilgan yil:", list(range(1960, 2010))[::-1])
            with col_b2:
                b_month = st.selectbox("Tug'ilgan oy:", list(range(1, 13)))
            with col_b3:
                b_day = st.selectbox("Tug'ilgan kun:", list(range(1, 32)))
                
            if st.button(lang_dict[lang]["save_btn"], key="save_worker"):
                if new_name:
                    new_id = f"EMP-{len(st.session_state.workers_list) + 1:02d}"
                    st.session_state.workers_list.append({
                        "ID": new_id,
                        "Ism": new_name,
                        "Tugilgan_sana": f"{b_year}-{b_month:02d}-{b_day:02d}"
                    })
                    st.success(f"{new_name} bazaga qo'shildi! ID: {new_id}")
                else:
                    st.error("Iltimos, ism-familiyani kiriting.")
        # ==========================================
        # TAB 3: SHIKOYAT VA TAKLIFLAR
        # ==========================================
        with tab3:
            st.subheader(f"🗣️ {lang_dict[lang]['feedback_title']}")
            
            worker_for_feedback = st.selectbox(
                lang_dict[lang]["select_worker"], 
                [w["Ism"] for w in st.session_state.workers_list],
                key="feedback_worker_select"
            )
            feedback_text = st.text_area("Xabaringizni yozing (Taklif yoki muammo):")
            
            if st.button("Yuborish / Submit", key="submit_feedback"):
                if feedback_text:
                    st.session_state.feedbacks.append({
                        "Sana": datetime.date.today().strftime("%Y-%m-%d"),
                        "Xodim": worker_for_feedback,
                        "Xabar": feedback_text
                    })
                    st.success("Xabaringiz rahbariyatga yuborildi! Katta rahmat.")
                else:
                    st.error("Iltimos, xabar matnini kiriting.")

    # --- 2. MENEJER (MANAGER) STRUKTURASI ---
    elif "Menejer" in role or "Manager" in role or "매니저" in role:
        st.markdown(f"<div class='main-title'>📊 {lang_dict[lang]['manager_title']}</div>", unsafe_allow_html=True)
        st.markdown("---")
        
        m_tab1, m_tab2 = st.tabs(["👥 Ishchilar va Keldi-Ketdi", "📅 Dam olish so'rovlari"])
        
        with m_tab1:
            st.subheader("Bugungi Keldi-Ketdi Hisoboti")
            if st.session_state.attendance_logs:
                df_logs = pd.DataFrame(st.session_state.attendance_logs)
                st.dataframe(df_logs, use_container_width=True)
            else:
                st.info("Hozircha ma'lumot yo'q.")
                
            st.subheader("Barcha Ishchilar Ro'yxati")
            df_workers = pd.DataFrame(st.session_state.workers_list)
            st.dataframe(df_workers, use_container_width=True)
            
        with m_tab2:
            st.subheader("Dam olish kunlari so'rovlari")
            if st.session_state.vacation_requests:
                for worker, days in st.session_state.vacation_requests.items():
                    st.write(f"**{worker}**: {', '.join(days)} - kunlar")
            else:
                st.info("Hozircha so'rovlar kelib tushmadi.")

    # --- 3. CEO (BOSHQARUV) STRUKTURASI ---
    elif "CEO" in role or "대표" in role or "Boshqaruv" in role:
        st.markdown(f"<div class='main-title'>📈 {lang_dict[lang]['ceo_title']}</div>", unsafe_allow_html=True)
        st.markdown("---")
        
        c_tab1, c_tab2 = st.tabs(["Umumiy Statistika", "Shikoyat va Takliflar"])
        
        with c_tab1:
            col1, col2, col3 = st.columns(3)
            col1.metric("Jami Ishchilar", len(st.session_state.workers_list))
            col2.metric("Bugungi Keldi-Ketdi", len(st.session_state.attendance_logs))
            col3.metric("Kutilyotgan Shikoyatlar", len(st.session_state.feedbacks))
            
            st.subheader("To'liq Hisobot")
            if st.session_state.attendance_logs:
                df_logs = pd.DataFrame(st.session_state.attendance_logs)
                st.dataframe(df_logs, use_container_width=True)
            else:
                st.write("Ma'lumot yo'q")
                
        with c_tab2:
            st.subheader("Xodimlar tomonidan bildirilgan fikrlar")
            if st.session_state.feedbacks:
                for idx, fb in enumerate(st.session_state.feedbacks):
                    st.warning(f"**{fb['Xodim']}** ({fb['Sana']}): {fb['Xabar']}")
            else:
                st.success("Hozircha hech qanday shikoyat yoki taklif yo'q.")
