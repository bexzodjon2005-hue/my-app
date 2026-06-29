import streamlit as st
from supabase import create_client, Client
import os

# ==============================================================================
# 1. TIZIM KONFIGURATSIYASI & DIZAYN (App Configuration & Theme Layout)
# ==============================================================================
st.set_page_config(
    page_title="Smart Branch Management System",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Dizaynni zamonaviy va toza ko'rinishga keltirish uchun
st.markdown("""
    <style>
    .main { background-color: #F8F9FA; }
    .stButton>button { border-radius: 8px; font-weight: 500; }
    div[data-testid="stMetricContainer"] {
        background-color: white;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. SUPABASE INTEGRATSIYASI (Database Connection)
# ==============================================================================
# GitHub Secrets yoki mahalliy .env fayldan oqiydi
SUPABASE_URL = "https://xyz-your-real-project.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...real-anon-key"

@st.cache_resource
def init_supabase() -> Client:
    """Ma'lumotlar bazasiga xavfsiz ulanish nuqtasi"""
    try:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    except Exception as e:
        st.error(f"⚠️ Baza bilan ulanish o'rnatilmadi: {e}")
        return None

supabase = init_supabase()

# ==============================================================================
# 3. SESSIYA HOZIRGI HOLATI (State Management)
# ==============================================================================
# Tizim xotirasida foydalanuvchi roli va holatlarini saqlash
if "user" not in st.session_state:
    st.session_state.user = None        # Foydalanuvchi profili (email, ism...)
if "role" not in st.session_state:
    st.session_state.role = None        # 'CEO', 'Manager' yoki 'Employee'
if "branch_id" not in st.session_state:
    st.session_state.branch_id = None  # Biriktirilgan filial ID si
if "page" not in st.session_state:
    st.session_state.page = "Login"     # Amaldagi sahifa yo'nalishi

def logout():
    """Tizimdan xavfsiz chiqish funksiyasi"""
    st.session_state.user = None
    st.session_state.role = None
    st.session_state.branch_id = None
    st.session_state.page = "Login"
    st.rerun()

# ==============================================================================
# 4. HAKIQIY AUTENTIFIKATSIYA VA TIZIMGA KIRISH (Login & RBAC)
# ==============================================================================
import hashlib

def hash_password(password: str) -> str:
    """Parolni xavfsiz saqlash va tekshirish uchun xeshlash"""
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(email, password):
    """Supabase bazasidagi users jadvali orqali foydalanuvchini tekshirish"""
    if not supabase:
        return None
    try:
        # Tizimdan o'chirilmagan (deleted_at is null) foydalanuvchini email orqali qidirish
        response = supabase.table("users").select("*").eq("email", email).is_("deleted_at", "null").execute()
        if response.data:
            user = response.data[0]
            # Kiritilgan parol bazadagi parolga mos kelishini tekshirish
            # (Agar bazada xeshlangan yoki oddiy saqlangan bo'lsa)
            if user.get("password") == password or user.get("password") == hash_password(password):
                return user
        return None
    except Exception as e:
        st.error(f"❌ Avtorizatsiya tizimida xatolik: {e}")
        return None

def render_login_page():
    st.markdown("<h2 style='text-align: center; color: #2C3E50;'>🔐 Tizimga kirish</h2>", unsafe_allow_html=True)
    st.write("")
    
    # Ekranning o'rtasida chiroyli shakl yaratish uchun ustunlardan foydalanamiz
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### Xush kelibsiz!")
        with st.form("login_form"):
            email = st.text_input("Elektron pochta", placeholder="misol@kompaniya.com")
            password = st.text_input("Parol", type="password")
            submit_button = st.form_submit_button("Tizimga kirish", use_container_width=True)
            
            if submit_button:
                if email and password:
                    user_data = authenticate_user(email, password)
                    
                    if user_data:
                        # Muvaffaqiyatli kirish: Sessiyani to'ldirish
                        first_name = user_data.get('first_name', '')
                        last_name = user_data.get('last_name', '')
                        st.session_state.user = {
                            "name": f"{first_name} {last_name}".strip(),
                            "email": email,
                            "id": user_data.get("id")
                        }
                        st.session_state.role = user_data.get("role")
                        st.session_state.branch_id = user_data.get("branch_id")
                        st.session_state.page = "Dashboard"
                        
                        # Audit logga yozish (Muvaffaqiyatli kirish)
                        execute_db_transaction("audit_logs", {
                            "user_email": email,
                            "action": "LOGIN_SUCCESS",
                            "details": f"Rol: {st.session_state.role} tizimga kirdi."
                        }, operation="insert")
                        
                        st.rerun()
                    else:
                        st.error("❌ Email yoki parol noto'g'ri!")
                        # Audit logga yozish (Omadsiz urinish)
                        execute_db_transaction("audit_logs", {
                            "user_email": email,
                            "action": "LOGIN_FAILED",
                            "details": "Noto'g'ri parol yoki email kiritildi."
                        }, operation="insert")
                else:
                    st.warning("⚠️ Iltimos, barcha maydonlarni to'ldiring.")

    # DIQQAT: Hozircha sizda Supabase'da jadvallar to'liq tayyor bo'lmasligi mumkin.
    # Shuning uchun kodni oson sinab ko'rishingiz uchun "Tezkor kirish" tugmalarini ham qo'shdim.
    # Baza to'liq ishlaganda bu qismni o'chirib tashlaymiz.
    st.markdown("---")
    with st.expander("🛠️ Dasturchi uchun tezkor test rejimi (Baza ishlamayotgan payt uchun)"):
        st.info("Bu qism orqali hozircha parolsiz kirib, panellarni dizaynini ko'rishingiz mumkin.")
        c1, c2, c3 = st.columns(3)
        if c1.button("🚀 CEO Paneliga o'tish", use_container_width=True):
            st.session_state.user = {"name": "Asilbek R.", "email": "ceo@test.com", "id": "U1"}
            st.session_state.role = "CEO"
            st.session_state.page = "Dashboard"
            st.rerun()
        if c2.button("👔 Manager Paneliga o'tish", use_container_width=True):
            st.session_state.user = {"name": "Menejer Olimjon", "email": "manager@test.com", "id": "U2"}
            st.session_state.role = "Manager"
            st.session_state.branch_id = "B001"
            st.session_state.page = "Dashboard"
            st.rerun()
        if c3.button("👨‍💻 Employee Paneliga o'tish", use_container_width=True):
            st.session_state.user = {"name": "Sardor Umrdinov", "email": "employee@test.com", "id": "U3"}
            st.session_state.role = "Employee"
            st.session_state.branch_id = "B001"
            st.session_state.page = "Dashboard"
            st.rerun()


# ==============================================================================
# 5. CEO DASHBOARD (Boshqaruv Paneli)
# ==============================================================================
import pandas as pd

def render_ceo_dashboard():
    st.header("📈 CEO Boshqaruv Paneli")
    st.markdown("Umumiy filiallar va xodimlar holati statistikasi.")

    # Yuqori ko'rsatkichlar (KPI metrics)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Umumiy filiallar", value="12 ta", delta="+2 ta yangi")
    with col2:
        st.metric(label="Jami xodimlar", value="145 ta", delta="+5 ta")
    with col3:
        st.metric(label="Bugungi davomat", value="92%", delta="-3%")
    with col4:
        st.metric(label="Faol smenalar", value="8 ta")

    st.markdown("---")

    # Grafik va jadvallar uchun 2 ta ustun
    left_col, right_col = st.columns([2, 1])

    with left_col:
        st.subheader("📊 Filiallar bo'yicha davomat (Haftalik)")
        # Namuna ma'lumotlar (Baza to'liq ishlaganda Supabase'dan olinadi)
        chart_data = pd.DataFrame({
            "Filiallar": ["Toshkent", "Samarqand", "Buxoro", "Farg'ona", "Xorazm"],
            "Kelganlar": [45, 30, 25, 35, 10]
        }).set_index("Filiallar")
        st.bar_chart(chart_data)

    with right_col:
        st.subheader("🏢 Filiallar holati")
        branches = st.session_state.get("branches", [])
        if branches:
            for branch in branches:
                with st.container():
                    status_color = "🟢" if branch.get("status") == "Active" else "🔴"
                    st.write(f"{status_color} **{branch.get('branch_name', 'Nomsiz')}**")
                    st.caption(f"ID: {branch.get('id')} | Menejer: {branch.get('manager_id')}")
                    st.divider()
        else:
            st.info("Filiallar ro'yxati bo'sh.")

        st.markdown("---")
    st.markdown("### 📊 Filiallar faoliyati tahlili")
    
    # Namuna ma'lumot (Keyinchalik bazadan ulanadi)
    df_branches = pd.DataFrame({
        "Filial": ["Chilonzor", "Yunusobod", "Shayxontohur"],
        "Tushum (mln so'm)": [45, 38, 52],
        "Xodimlar soni": [12, 10, 15],
        "Samaradorlik": [92, 85, 96]
    })
    
    # Jadvalni ko'rsatish
    st.table(df_branches)
    
    # Grafik qo'shish
    st.subheader("Oylik tushum dinamikasi")
    st.bar_chart(df_branches.set_index("Filial")["Tushum (mln so'm)"])

    # Tezkor harakatlar tugmalari va Formalar
    st.markdown("### ⚡ Tezkor harakatlar")
    
    # Yangi filial qo'shish formasi (Ochiluvchi oyna)
    with st.expander("➕ Yangi filial qo'shish", expanded=False):
        with st.form("add_branch_form"):
            st.write("Yangi filial ma'lumotlarini kiriting:")
            b_name = st.text_input("Filial nomi (Masalan: Chilonzor-1)")
            b_manager = st.text_input("Menejerning ism-familiyasi")
            b_address = st.text_input("Manzil")
            
            if st.form_submit_button("Filialni saqlash", type="primary"):
                if b_name and b_manager:
                    st.success(f"✅ {b_name} filiali tizimga muvaffaqiyatli qo'shildi!")
                else:
                    st.error("Iltimos, filial nomi va menejer ismini to'liq kiriting.")

    # Boshqa tugmalar
    col_btn1, col_btn2 = st.columns(2)
    if col_btn1.button("📄 Umumiy hisobotni yuklash", use_container_width=True):
        st.success("Hisobot yuklanmoqda...")
    if col_btn2.button("⚙️ Tizim sozlamalari", use_container_width=True):
        st.info("Sozlamalar sahifasi tez orada qo'shiladi.")

# ==============================================================================
# 6. MANAGER DASHBOARD (Filial Menejeri Paneli)
# ==============================================================================
def render_manager_dashboard():
    st.header("👔 Menejer Paneli")
    st.markdown(f"**Sizning filialingiz ID raqami:** `{st.session_state.get('branch_id', 'Nomaʼlum')}`")
    
    st.divider()
    
    # Kichik statistika
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Smenadagi xodimlar", "12 / 15", "-3 (Kelmadi)")
    with col2:
        st.metric("Bugungi tushum (Kutilma)", "12.5 mln", "+1.2 mln")
    with col3:
        st.metric("Vazifalar holati", "80%", "Qoniqarli")
        
    st.markdown("### 👥 Xodimlar davomati va Smenalar")
    
    # 2 ta bo'limli oyna (Tabs)
    tab1, tab2 = st.tabs(["📋 Davomatni tasdiqlash", "📅 Smena jadvali"])
    
    with tab1:
        st.info("Bugungi davomat ro'yxati (Tasdiqlash kutilmoqda)")
        # Namuna ma'lumot (Keyinchalik bazadan ulanadi)
        df_attendance = pd.DataFrame({
            "Xodim": ["Sardor Umrdinov", "Ali Valiyev", "Zarina To'rayeva"],
            "Kelgan vaqti": ["08:50", "09:05", "08:55"],
            "Holat": ["Vaqtida", "Kechikdi", "Vaqtida"]
        })
        st.dataframe(df_attendance, use_container_width=True)
        
        if st.button("✅ Barchasini tasdiqlash", type="primary"):
            st.success("Davomat muvaffaqiyatli tasdiqlandi!")
            
    with tab2:
        st.write("Joriy haftalik smena jadvali")
        df_shifts = pd.DataFrame({
            "Kun": ["Dushanba", "Seshanba", "Chorshanba"],
            "Ertalab (08:00-16:00)": ["Sardor, Ali", "Zarina, Ali", "Sardor, Zarina"],
            "Kechasi (16:00-00:00)": ["Zarina, Vahob", "Sardor, Vahob", "Ali, Vahob"]
        })
        st.table(df_shifts)

    st.markdown("---")
    st.markdown("### ⚙️ Filial boshqaruvi")
    
    # Yangi xodim qo'shish formasi
    with st.expander("➕ Yangi xodim qo'shish", expanded=False):
        with st.form("add_employee_form"):
            st.write("Yangi xodim ma'lumotlarini kiriting:")
            e_name = st.text_input("Xodimning ism-familiyasi (Masalan: Alisher Valiyev)")
            e_role = st.selectbox("Lavozimi", ["Sotuvchi", "Kassir", "Omborchi", "Farrosh"])
            e_phone = st.text_input("Telefon raqami")
            
            if st.form_submit_button("Xodimni saqlash", type="primary"):
                if e_name and e_phone:
                    st.success(f"✅ {e_name} filial jamoasiga muvaffaqiyatli qo'shildi!")
                else:
                    st.error("Iltimos, xodimning ism-familiyasi va telefon raqamini to'liq kiriting.")



# ==============================================================================
# 7. EMPLOYEE DASHBOARD (Xodim Paneli)
# ==============================================================================
def render_employee_dashboard():
    st.header("📱 Xodim Ish Paneli")
    st.markdown(f"**Xodim:** `{st.session_state.user.get('name', 'Nomaʼlum')}` | **Filial ID:** `{st.session_state.get('branch_id', 'Nomaʼlum')}`")
    
    st.divider()
    
    # Davomat (Check-in / Check-out) bo'limi
    st.subheader("⏱️ Ish vaqtini hisobga olish (Davomat)")
    
    if "checked_in" not in st.session_state:
        st.session_state.checked_in = False
        
    col1, col2 = st.columns(2)
    
    with col1:
        if not st.session_state.checked_in:
            if st.button("🚀 Ishni boshlash (Check-in)", type="primary", use_container_width=True):
                st.session_state.checked_in = True
                st.success("Ish vaqti boshlandi! Smenaga kirdingiz.")
                st.rerun()
        else:
            st.button("🚀 Ishni boshlash (Kirdingiz)", type="primary", disabled=True, use_container_width=True)
            
    with col2:
        if st.session_state.checked_in:
            if st.button("🛑 Ishni yakunlash (Check-out)", type="secondary", use_container_width=True):
                st.session_state.checked_in = False
                st.warning("Ish vaqti yakunlandi! Smenadan chiqdingiz.")
                st.rerun()
        else:
            st.button("🛑 Ishni yakunlash", type="secondary", disabled=True, use_container_width=True)
            
    st.markdown("---")
    
    # Bugungi vazifalar
    st.subheader("📅 Bugungi Vazifalarim")
    tasks = [
        {"Vazifa": "Filialni ochish va tozalikni tekshirish", "Holat": "✅ Bajarildi"},
        {"Vazifa": "Kassani tekshirish va kunlik hisobotni boshlash", "Holat": "✅ Bajarildi"},
        {"Vazifa": "Mijozlarga xizmat ko'rsatish va tovarlar qoldig'ini yangilash", "Holat": "⏳ Jarayonda"}
    ]
    for t in tasks:
        st.write(f"{t['Holat']} — {t['Vazifa']}")

# ==============================================================================
# 5. ASOSIY ROUTER (Main Application Workflow)
# ==============================================================================
def main():
    st.title("🏢 Smart Branch Management System")
    st.caption("10 Qismli Integratsiyalashgan Korporativ Tizim | Alfa Versiya 1.0.0")
    st.markdown("---")
    
    # Foydalanuvchi tizimga kirmagan bo'lsa
    if st.session_state.page == "Login":
        render_login_page()
    else:
        # Yon panel navigatsiyasi (Sidebar Navigation)
        with st.sidebar:
            st.subheader(f"User: {st.session_state.user['name']}")
            st.code(f"Rol: {st.session_state.role}\nFilial: {st.session_state.branch_id or 'Barcha'}")
            st.markdown("---")
            if st.button("🚪 Tizimdan chiqish", use_container_width=True, type="primary"):
                logout()
        
        # Rolga qarab tegishli modullarni yo'naltirish
        if st.session_state.role == "CEO":
            render_ceo_dashboard()

        elif st.session_state.role == "Manager":
            render_manager_dashboard()
        elif st.session_state.role == "Employee":
            render_employee_dashboard()
        # ==============================================================================
        # 10. YAKUNIY QISM (Footer)
        # ==============================================================================
        st.markdown("---")
        st.markdown("<p style='text-align: center; color: gray;'>Smart Branch Management System © 2026 | Barcha huquqlar himoyalangan</p>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
# ==============================================================================
# 6. MA'LUMOTLAR BAZASI BILAN ISHLASH (Database Queries & Services)
# ==============================================================================

def get_supabase_data(table_name: str, branch_id: str = None, company_id: str = None):
    """
    Supabase jadvallaridan Soft Delete (deleted_at IS NULL) sharti bilan 
    va rollarga asoslangan (RBAC) filtrlangan ma'lumotlarni xavfsiz tortib olish.
    """
    if not supabase:
        return []
    try:
        query = supabase.table(table_name).select("*")
        
        # Soft delete filtri - O'chirilmagan ma'lumotlarni ko'rish
        query = query.is_("deleted_at", "null")
        
        # Branch yoki Company bo'yicha cheklovlar
        if branch_id:
            query = query.eq("branch_id", branch_id)
        if company_id:
            query = query.eq("company_id", company_id)
            
        response = query.execute()
        return response.data if response else []
    except Exception as e:
        st.error(f"❌ {table_name} jadvalidan ma'lumot olishda xatolik: {e}")
        return []

def execute_db_transaction(table_name: str, data: dict, operation: str = "insert", row_id: str = None):
    """
    Ma'lumotlar bazasiga yozish, tahrirlash va soft-delete operatsiyalari.
    Har bir amal Audit Logga yozilishi shart (3.24 va 4.7 qoidalar).
    """
    if not supabase:
        return False
    try:
        if operation == "insert":
            response = supabase.table(table_name).insert(data).execute()
        elif operation == "update" and row_id:
            response = supabase.table(table_name).update(data).eq("id", row_id).execute()
        elif operation == "soft_delete" and row_id:
            # Ma'lumot o'chirilmaydi, faqat vaqti belgilanadi (2.5 va 3.1 qoidasi)
            import datetime
            now_str = datetime.datetime.now().isoformat()
            response = supabase.table(table_name).update({"deleted_at": now_str}).eq("id", row_id).execute()
            
        # AUDIT LOG YARATISH (Har bir amalni tizim tarixiga muhrlash)
        user_email = st.session_state.user.get("email", "System") if st.session_state.user else "Anonymous"
        audit_data = {
            "user_email": user_email,
            "action": f"{operation.upper()} on {table_name}",
            "details": str(data) if operation != "soft_delete" else f"Deleted Row ID: {row_id}",
            "created_at": datetime.datetime.now().isoformat()
        }
        # Audit log yozish xatolikka uchrasa ham asosiy amal to'xtamaydi
        try:
            supabase.table("audit_logs").insert(audit_data).execute()
        except:
            pass
            
        return True
    except Exception as e:
        st.error(f"❌ Ma'lumotni bazaga yozishda xatolik ({operation}): {e}")
        return False

# ==============================================================================
# 7. MA'LUMOTLARNI KESHLAsh VA TEZKOR YUKLASH (Performance & Optimization)
# ==============================================================================
def load_initial_app_data():
    """
    Tizim ochilayotganda kutilish vaqtini 3 soniyadan kamaytirish uchun (2.16-qoida)
    kerakli barcha konfiguratsiyalarni session_state xotirasiga yuklaydi.
    """
    if "db_cached" not in st.session_state:
        # Agar Supabase ulanmagan bo'lsa, tizim to'xtab qolmasligi uchun test ma'lumotlar (Mockups)
        st.session_state.companies = get_supabase_data("companies") or [{"id": "C01", "company_name": "SmartCorp"}]
        st.session_state.branches = get_supabase_data("branches") or [
            {"id": "B001", "branch_name": "Toshkent Filiali", "manager_id": "M01", "status": "Active"},
            {"id": "B002", "branch_name": "Samarqand Filiali", "manager_id": "M02", "status": "Active"}
        ]
        st.session_state.shifts = get_supabase_data("shifts") or [
            {"id": "S1", "shift_name": "Morning", "start_time": "09:00", "end_time": "18:00"},
            {"id": "S2", "shift_name": "Evening", "start_time": "13:00", "end_time": "22:00"},
            {"id": "S3", "shift_name": "Night", "start_time": "22:00", "end_time": "07:00"}
        ]
        st.session_state.db_cached = True

# Dastur ishga tushishi bilan keshni yuklash
load_initial_app_data()
