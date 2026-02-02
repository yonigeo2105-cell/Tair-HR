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
st.set_page_config(page_title="Shapira Law HR", layout="wide", page_icon="⚖️")

# --- עיצוב CSS מתקדם (תפריט קבוע) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;600;700;800&display=swap');

    /* הגדרות בסיס */
    html, body, [class*="css"] {
        font-family: 'Assistant', sans-serif;
        direction: rtl;
        background-color: #f8f9fa;
    }

    /* הסתרת האלמנטים המובנים של סטרימליט כדי לקבל מראה נקי */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* עיצוב עמודות */
    div[data-testid="column"] {
        background-color: transparent;
    }

    /* עיצוב עמודת התפריט (צד ימין) */
    .menu-container {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        border: 1px solid #e9ecef;
        height: 100%;
    }
    
    /* כותרות */
    h1 {
        color: #880e4f;
        font-weight: 800;
        margin-bottom: 0;
        font-size: 2.2rem;
    }
    
    h3 {
        color: #ad1457;
        font-size: 1.1rem;
        margin-top: 5px;
        font-weight: 400;
    }
    
    h2 {
        color: #880e4f;
        font-size: 1.8rem;
        margin-bottom: 25px;
        border-bottom: 2px solid #fce4ec;
        padding-bottom: 10px;
    }

    /* עיצוב כפתורי הבחירה (Radio Buttons) שייראו כמו תפריט */
    div[role="radiogroup"] > label {
        background-color: #ffffff;
        border: 1px solid #f1f3f5;
        padding: 15px 20px;
        border-radius: 10px;
        margin-bottom: 10px;
        transition: all 0.2s;
        box-shadow: 0 2px 5px rgba(0,0,0,0.02);
        cursor: pointer;
        display: flex;
        align-items: center;
    }

    div[role="radiogroup"] > label:hover {
        background-color: #fce4ec;
        border-color: #f8bbd0;
        transform: translateX(-5px);
    }
    
    /* סימון הפריט הנבחר */
    div[role="radiogroup"] > label[data-checked="true"] {
        background: linear-gradient(45deg, #d81b60, #ec407a);
        color: white !important;
        border: none;
        box-shadow: 0 5px 15px rgba(216, 27, 96, 0.3);
    }
    
    div[role="radiogroup"] > label[data-checked="true"] p {
        color: white !important;
        font-weight: 700;
    }

    /* כפתורי פעולה (שליחה) */
    .stButton>button {
        background: linear-gradient(45deg, #d81b60, #ff80ab);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 12px 24px;
        font-size: 16px;
        font-weight: 600;
        width: 100%;
        box-shadow: 0 4px 10px rgba(216, 27, 96, 0.2);
        transition: transform 0.2s;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 15px rgba(216, 27, 96, 0.3);
    }

    /* קופסאות תוכן */
    .content-box {
        background-color: white;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.03);
        border: 1px solid #f8f9fa;
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

# --- פריסת עמוד (Layout) ---
# יצירת שתי עמודות: ימין לתפריט (קטן), שמאל לתוכן (גדול)
menu_col, content_col = st.columns([1, 4])

# ==========================
# צד ימין: תפריט קבוע
# ==========================
with menu_col:
    st.markdown("""
        <div style="text-align: center; padding: 20px 0;">
            <h1>HR</h1>
            <h3>Shapira Law</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # תפריט הניווט (כפתורי רדיו מעוצבים)
    selected_page = st.radio(
        "",
        ["דף הבית", "זימון לראיון", "ימי הולדת", "הודעה בתפוצה רחבה", "ניהול עובדים"],
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.caption("מערכת ניהול משרדית v2.0")

# ==========================
# צד שמאל: תוכן משתנה
# ==========================
with content_col:
    # שימוש ב-Container כדי לתחום את התוכן במסגרת יפה
    with st.container():
        st.markdown('<div class="content-box">', unsafe_allow_html=True)

        # --- לוגיקה של העמודים ---
        
        if selected_page == "דף הבית":
            st.markdown("""
                <div style="text-align: center; padding: 50px;">
                    <h1 style="font-size: 3rem;">שלום תאיר! 👋</h1>
                    <h3 style="font-size: 1.5rem; margin-top: 10px;">ברוכה הבאה למשרד הדיגיטלי.</h3>
                    <br>
                    <p style="color: #666; font-size: 1.1rem;">
                        התפריט מימינך (או למעלה בנייד) פתוח תמיד לשירותך.<br>
                        בחרי פעולה כדי להתחיל.
                    </p>
                </div>
            """, unsafe_allow_html=True)

        elif selected_page == "זימון לראיון":
            st.markdown("<h2>📅 זימון מועמד לראיון</h2>", unsafe_allow_html=True)
            
            c1, c2 = st.columns(2)
            with c1:
                candidate_name = st.text_input("שם מלא")
                phone_number = st.text_input("נייד")
            with c2:
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
                
                st.info("תצוגה מקדימה:")
                st.text(message_body)
                wa_link = create_whatsapp_link(phone_number, message_body)
                st.markdown(f'''<a href="{wa_link}" target="_blank" style="text-decoration: none;"><button>📞 שליחה בוואטסאפ</button></a>''', unsafe_allow_html=True)

        elif selected_page == "ימי הולדת":
            st.markdown("<h2>🎂 ברכת יום הולדת</h2>", unsafe_allow_html=True)
            
            df = load_data()
            if not df.empty:
                df['תאריך לידה'] = pd.to_datetime(df['תאריך לידה'], errors='coerce')
                names = df['שם העובד'].tolist()
                
                selected = st.selectbox("למי חוגגים?", names)
                
                if selected:
                    emp_data = df[df['שם העובד'] == selected].iloc[0]
                    emp_phone = emp_data['טלפון']
                    
                    video_text = f"\n\n🎬 הכנו לך משהו קטן: {VIDEO_URL}"
                    
                    types = {
                        "רשמי": f"מזל טוב {selected}! 🎉\nיום הולדת שמח! מאחלים לך שנה של צמיחה, הצלחות והמון רגעים מאושרים.\nשמחים שאת/ה חלק מהצוות שלנו.\n\nאוהבים משרד י.שפירא ושות' עורכי דין{video_text}",
                        "משפחתי": f"היי {selected}, המון מזל טוב ליום ההולדת! 🎂\nשתהיה שנה מדהימה, מלאה בכיף ובשורות טובות.\n\nאוהבים משרד י.שפירא ושות' עורכי דין{video_text}",
                    }
                    choice = st.radio("סגנון:", list(types.keys()), horizontal=True)
                    msg = types[choice]
                    
                    st.text_area("הודעה:", msg, height=120)
                    wa_link = create_whatsapp_link(emp_phone, msg)
                    st.markdown(f'''<a href="{wa_link}" target="_blank" style="text-decoration: none;"><button>🎁 שליחה בוואטסאפ</button></a>''', unsafe_allow_html=True)
            else:
                st.warning("המאגר ריק. יש לטעון עובדים.")

        elif selected_page == "הודעה בתפוצה רחבה":
            st.markdown("<h2>📢 הודעה לכל העובדים</h2>", unsafe_allow_html=True)
            st.info("כאן מעתיקים את כל המספרים כדי לפתוח 'רשימת תפוצה' בוואטסאפ.")
            
            msg = st.text_area("תוכן ההודעה:", height=100)
            
            if msg:
                df = load_data()
                if not df.empty:
                    phones = df['טלפון'].astype(str).str.replace('.0', '', regex=False).tolist()
                    phones_str = ",".join(phones)
                    
                    st.markdown("1. העתקי את המספרים:")
                    st.code(phones_str, language="text")
                    st.markdown("2. העתקי את ההודעה:")
                    st.code(msg, language="text")
                else:
                    st.error("אין נתונים.")

        elif selected_page == "ניהול עובדים":
            st.markdown("<h2>👥 מאגר עובדים</h2>", unsafe_allow_html=True)
            
            uploaded = st.file_uploader("טעינת אקסל", type=['xlsx', 'csv'])
            if uploaded:
                try:
                    if uploaded.name.endswith('.csv'):
                        new = pd.read_csv(uploaded)
                    else:
                        new = pd.read_excel(uploaded)
                    new = normalize_columns(new)
                    req = ['שם העובד', 'טלפון', 'תאריך לידה']
                    if all(c in new.columns for c in req):
                        new = new[req]
                        new['טלפון'] = new['טלפון'].astype(str).str.replace('.0', '', regex=False)
                        exist = load_data()
                        combo = pd.concat([exist, new]).drop_duplicates(subset=['שם העובד', 'טלפון'], keep='last')
                        save_data(combo)
                        st.success(f"עודכן בהצלחה! ({len(new)} רשומות)")
                        st.rerun()
                    else:
                        st.error("חסרות עמודות: שם, טלפון, תאריך לידה")
                except Exception as e:
                    st.error(f"שגיאה: {e}")
            
            st.markdown("---")
            st.markdown("### ✏️ עריכה חיה")
            
            df = load_data()
            edited = st.data_editor(
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
            
            if st.button("💾 שמור שינויים"):
                save_data(edited)
                st.success("נשמר!")

        st.markdown('</div>', unsafe_allow_html=True) # סגירת ה-div של התוכן
