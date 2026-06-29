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
SUPABASE_URL = st.secrets.get("SUPABASE_URL", os.getenv("SUPABASE_URL", "https://your-project.supabase.co"))
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY", os.getenv("SUPABASE_KEY", "your-anon-key"))

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
            st.success("🎯 Siz CEO tizimidasiz. 5-bo'lim (CEO Dashboard) kodi shu yerga joylashadi.")
        elif st.session_state.role == "Manager":
            st.info("📊 Siz Manager tizimidasiz. 6-bo'lim (Manager Panel) kodi shu yerga joylashadi.")
        elif st.session_state.role == "Employee":
            st.warning("📱 Siz Employee tizimidasiz. 7-bo'lim (Employee Panel) kodi shu yerga joylashadi.")

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
