import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse
import os

# ==========================================
# 👇 הקישור הקבוע לסרטון יום ההולדת 👇
# ==========================================
VIDEO_URL = "https://youtu.be/j5F708M4by0"

# --- הגדרות עמוד ---
st.set_page_config(page_title="Shapira Law HR", layout="centered", page_icon="⚖️")

# --- עיצוב מתוקן (ללא רווחים, תפריט עובד) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;600;700;800&display=swap');

    /* הגדרות בסיס */
    html, body, [class*="css"] {
        font-family: 'Assistant', sans-serif;
        direction: rtl;
        background-color: #ffffff; /* רקע לבן נקי */
    }

    /* תיקון התפריט - החזרת כפתור ההמבורגר */
    header[data-testid="stHeader"] {
        background-color: transparent;
        z-index: 999;
    }
    
    /* הסתרת רק הפוטר למטה, לא את התפריט למעלה */
    footer {visibility: hidden;}
    #MainMenu {visibility: visible;} 

    /* הסרת הרווחים הגדולים בראש העמוד */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 1rem !important;
    }

    /* כותרות */
    h1 {
        color: #880e4f;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.5rem;
    }
    
    h2, h3 {
        color: #ad1457;
        font-weight: 600;
        margin-bottom: 1rem;
    }

    /* כפתורים - עיצוב הדוק יותר */
    .stButton>button {
        background: linear-gradient(45deg, #d81b60, #ff80ab);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 10px 20px;
        font-size: 16px;
        font-weight: 600;
        width: 100%;
        margin-top: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    /* שדות קלט - עיצוב נקי וברור */
    .stTextInput>div>div>input, .stDateInput>div>div>input, .stSelectbox>div>div {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        border-radius: 8px;
        color: #333;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #d81b60;
        background-color: #fff;
    }

    /* מסך פתיחה */
    .welcome-container {
        text-align: center;
        padding: 40px 20px;
        background: linear-gradient(135deg, #fce4ec 0%, #ffffff 100%);
        border-radius: 20px;
        margin-top: 20px;
    }
    .welcome-title {
        font-size: 2.5rem;
        color: #880e4f;
        margin-bottom: 10px;
    }
    .welcome-text {
        font-size: 1.2rem;
        color: #555;
    }

    </style>
    """, unsafe_allow_html=True)

# --- פונקציות עזר ---
def get_hebrew_day(date_obj):
    days = {0: "ב'", 1: "ג'", 2: "ד'", 3: "ה'", 4: "ו'", 5: "שבת", 6: "א'"}
    return days[date_obj.weekday()]

def create_whatsapp_link(phone, message):
    clean_phone = ''.join(filter(str.isdigit, str(phone)))
    if clean_phone.startswith('0'):
        clean_phone = '972' + clean_phone[1:]
    encoded_message = urllib.parse.quote(message)
    return f"https://wa.me/{clean_phone}?text={encoded_message}"

def load_data():
    if os.path.exists('employees.csv'):
        return pd.read_csv('employees.csv', dtype={'טלפון': str})
    return pd.DataFrame(columns=["שם העובד", "תאריך לידה", "טלפון"])

def save_data(df):
    df.to_csv('employees.csv', index=False)

def normalize_columns(df):
    cols = df.columns
    mapping = {}
    for col in cols:
        if 'שם' in str(col) or 'name' in str(col).lower():
            mapping[col] = 'שם העובד'
        elif 'טלפון' in str(col) or 'נייד' in str(col) or 'phone' in str(col).lower():
            mapping[col] = 'טלפון'
        elif 'לידה' in str(col) or 'birthday' in str(col).lower():
            mapping[col] = 'תאריך לידה'
    return df.rename(columns=mapping)

# --- תפריט צד ---
with st.sidebar:
    st.markdown("### תפריט")
    menu = st.radio("", ["דף הבית", "זימון לראיון", "ימי הולדת", "הודעה בתפוצה רחבה", "ניהול עובדים"])

# ==========================
# מסך 0: דף הבית
# ==========================
if menu == "דף הבית":
    # אזור קבלת פנים מרוכז
    st.markdown("""
        <div class="welcome-container">
            <div class="welcome-title">שלום תאיר! 👋</div>
            <div class="welcome-text">ברוכה הבאה למערכת הניהול של משרד י.שפירא ושות'.<br>בחרי פעולה מהתפריט (החץ למעלה מימין) כדי להתחיל.</div>
        </div>
    """, unsafe_allow_html=True)

# ==========================
# מסך 1: זימון לראיון
# ==========================
elif menu == "זימון לראיון":
    st.markdown("### 📅 פרטי המועמד/ת")
    
    col1, col2 = st.columns(2)
    with col1:
        candidate_name = st.text_input("שם מלא")
        phone_number = st.text_input("נייד")
    with col2:
        interview_date = st.date_input("תאריך הראיון")
        interview_time = st.time_input("שעה")
    
    if candidate_name and phone_number:
        date_str = interview_date.strftime('%d/%m')
        time_str = interview_time.strftime('%H:%M')
        day_hebrew = get_hebrew_day(interview_date)
        
        message_body = (
            f"היי {candidate_name}, זאת תאיר ממשרד עורכי דין י.שפירא.\n"
            f"בהמשך לשיחתנו נקבע ראיון עבודה ליום {day_hebrew} בתאריך ה-{date_str} בשעה {time_str}.\n"
            f"כתובתנו נירים 4 תל אביב. אני יושבת בקומה ה-2.\n\n"
            f"לכל שאלה אני זמינה במספר הזה, אנא אשר/י את קבלת ההודעה."
        )
        
        st.markdown("**תצוגה מקדימה:**")
        st.info(message_body)
        
        wa_link = create_whatsapp_link(phone_number, message_body)
        
        st.markdown(f'''
            <a href="{wa_link}" target="_blank" style="text-decoration: none;">
                <button>📞 שליחה בוואטסאפ</button>
            </a>
            ''', unsafe_allow_html=True)

# ==========================
# מסך 2: ימי הולדת
# ==========================
elif menu == "ימי הולדת":
    st.markdown("### 🎂 ימי הולדת")
    
    df = load_data()
    if not df.empty:
        df['תאריך לידה'] = pd.to_datetime(df['תאריך לידה'], errors='coerce')
        employee_names = df['שם העובד'].tolist()
        
        # בחירה קומפקטית
        selected_employee = st.selectbox("למי חוגגים?", employee_names)
        
        if selected_employee:
            emp_data = df[df['שם העובד'] == selected_employee].iloc[0]
            emp_phone = emp_data['טלפון']
            
            video_text = f"\n\n🎬 הכנו לך משהו קטן: {VIDEO_URL}"
            
            wishes_options = {
                "רשמי": f"מזל טוב {selected_employee}! 🎉\nיום הולדת שמח! מאחלים לך שנה של צמיחה, הצלחות והמון רגעים מאושרים.\nשמחים שאת/ה חלק מהצוות שלנו.\n\nאוהבים משרד י.שפירא ושות' עורכי דין{video_text}",
                "משפחתי": f"היי {selected_employee}, המון מזל טוב ליום ההולדת! 🎂\nשתהיה שנה מדהימה, מלאה בכיף ובשורות טובות.\n\nאוהבים משרד י.שפירא ושות' עורכי דין{video_text}",
            }
            wishes_type = st.radio("סגנון:", list(wishes_options.keys()), horizontal=True)
            final_message = wishes_options[wishes_type]
            
            st.text_area("הודעה:", final_message, height=120)
            wa_link_bday = create_whatsapp_link(emp_phone, final_message)
            
            st.markdown(f'''<a href="{wa_link_bday}" target="_blank" style="text-decoration: none;"><button>🎁 שליחה בוואטסאפ</button></a>''', unsafe_allow_html=True)
    else:
        st.warning("המאגר ריק. טעני קובץ בניהול עובדים.")

# ==========================
# מסך 3: תפוצה רחבה
# ==========================
elif menu == "הודעה בתפוצה רחבה":
    st.markdown("### 📢 הודעה לכולם")
    st.caption("כלי להעתקת מספרי טלפון לרשימת תפוצה בוואטסאפ")
    
    general_msg = st.text_area("תוכן ההודעה:", height=100)
    
    if general_msg:
        df = load_data()
        if not df.empty:
            all_phones = df['טלפון'].astype(str).str.replace('.0', '', regex=False).tolist()
            phones_text = ",".join(all_phones)
            
            st.markdown("**1. העתקי מספרים לרשימת תפוצה:**")
            st.code(phones_text, language="text")
            
            st.markdown("**2. העתקי את ההודעה:**")
            st.code(general_msg, language="text")
        else:
            st.error("אין עובדים ברשימה.")

# ==========================
# מסך 4: ניהול עובדים
# ==========================
elif menu == "ניהול עובדים":
    st.markdown("### 👥 מאגר עובדים")
    
    uploaded_file = st.file_uploader("📂 טעינת אקסל", type=['xlsx', 'xls', 'csv'])
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                new_df = pd.read_csv(uploaded_file)
            else:
                new_df = pd.read_excel(uploaded_file)
            
            new_df = normalize_columns(new_df)
            required_cols = ['שם העובד', 'טלפון', 'תאריך לידה']
            
            if all(col in new_df.columns for col in required_cols):
                new_df = new_df[required_cols]
                new_df['טלפון'] = new_df['טלפון'].astype(str).str.replace('.0', '', regex=False)
                existing_df = load_data()
                combined_df = pd.concat([existing_df, new_df]).drop_duplicates(subset=['שם העובד', 'טלפון'], keep='last')
                save_data(combined_df)
                st.success(f"עודכן! ({len(new_df)} רשומות)")
                st.rerun()
            else:
                st.error("קובץ לא תקין.")
        except Exception as e:
            st.error(f"שגיאה: {e}")

    st.markdown("---")
    st.markdown("**עריכת טבלה:**")
    df = load_data()
    edited_df = st.data_editor(
        df,
        num_rows="dynamic",
        column_config={
            "שם העובד": st.column_config.TextColumn("שם מלא", required=True),
            "טלפון": st.column_config.TextColumn("טלפון", required=True),
            "תאריך לידה": st.column_config.DateColumn("תאריך לידה", format="DD/MM/YYYY")
        },
        use_container_width=True,
        hide_index=True
    )

    if st.button("💾 שמירה"):
        save_data(edited_df)
        st.success("נשמר!")
