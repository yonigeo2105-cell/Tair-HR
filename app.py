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

# --- עיצוב "בוטיק" יוקרתי (CSS Custom Injection) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Assistant:wght@300;400;600;700;800&display=swap');

    /* איפוס כללי ופונטים */
    html, body, [class*="css"] {
        font-family: 'Assistant', sans-serif;
        direction: rtl;
        color: #4a4a4a;
    }

    /* רקע האפליקציה - ורוד פנינה יוקרתי */
    .stApp {
        background-color: #fdfbfb;
        background-image: linear-gradient(120deg, #fdfbfb 0%, #ebedee 100%);
    }
    
    /* הסתרת כותרות ברירת מחדל של סטרימליט */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* עיצוב כותרת דף הבית */
    .welcome-title {
        font-size: 3.5rem;
        font-weight: 800;
        color: #880e4f;
        text-align: center;
        margin-top: 50px;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        animation: fadeIn 2s;
    }
    
    .welcome-subtitle {
        font-size: 1.5rem;
        color: #ad1457;
        text-align: center;
        margin-top: -10px;
        font-weight: 300;
        animation: fadeIn 3s;
    }

    /* עיצוב הכרטיס המרכזי (הקופסה הלבנה) */
    .css-1r6slb0, .stForm, div[data-testid="stVerticalBlock"] > div {
        background-color: #ffffff;
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.05);
        border: 1px solid #fff0f5;
        margin-bottom: 20px;
    }

    /* כפתורים - גרדיאנט ורוד-זהב */
    .stButton>button {
        background: linear-gradient(45deg, #d81b60, #ff80ab);
        color: white;
        border: none;
        border-radius: 50px;
        padding: 15px 30px;
        font-size: 18px;
        font-weight: 600;
        box-shadow: 0 10px 20px rgba(216, 27, 96, 0.2);
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 25px rgba(216, 27, 96, 0.3);
    }
    
    /* אנימציה */
    @keyframes fadeIn {
        0% { opacity: 0; }
        100% { opacity: 1; }
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

# --- תפריט צד (מוסתר כברירת מחדל בנייד) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2910/2910756.png", width=60)
    st.markdown("### תפריט פעולות")
    # הוספתי את "דף הבית" כאופציה ראשונה
    menu = st.radio("", ["דף הבית", "זימון לראיון", "ימי הולדת", "הודעה בתפוצה רחבה", "ניהול עובדים"])

# ==========================
# מסך 0: דף הבית (Landing Page)
# ==========================
if menu == "דף הבית":
    # הכותרת הגדולה שביקשת
    st.markdown("<div class='welcome-title'>שלום תאיר! ❤️</div>", unsafe_allow_html=True)
    st.markdown("<div class='welcome-subtitle'>מה תרצי לעשות היום?</div>", unsafe_allow_html=True)
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.info("👈 לחצי על החץ למעלה בצד ימין כדי לפתוח את התפריט")

# ==========================
# מסך 1: זימון לראיון
# ==========================
elif menu == "זימון לראיון":
    st.markdown("<h2>📅 פרטי המועמד/ת</h2>", unsafe_allow_html=True)
    
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
        
        st.markdown("---")
        wa_link = create_whatsapp_link(phone_number, message_body)
        
        st.markdown(f'''
            <a href="{wa_link}" target="_blank" style="text-decoration: none;">
                <button>📞 פתח וואטסאפ לשליחה</button>
            </a>
            ''', unsafe_allow_html=True)

# ==========================
# מסך 2: ימי הולדת
# ==========================
elif menu == "ימי הולדת":
    st.markdown("<h2>🎂 שליחת ברכה</h2>", unsafe_allow_html=True)
    
    df = load_data()
    if not df.empty:
        df['תאריך לידה'] = pd.to_datetime(df['תאריך לידה'], errors='coerce')
        employee_names = df['שם העובד'].tolist()
        selected_employee = st.selectbox("למי חוגגים היום?", employee_names)
        
        if selected_employee:
            emp_data = df[df['שם העובד'] == selected_employee].iloc[0]
            emp_phone = emp_data['טלפון']
            
            video_text = f"\n\n🎬 הכנו לך משהו קטן: {VIDEO_URL}"
            
            wishes_options = {
                "רשמי": f"מזל טוב {selected_employee}! 🎉\nיום הולדת שמח! מאחלים לך שנה של צמיחה, הצלחות והמון רגעים מאושרים.\nשמחים שאת/ה חלק מהצוות שלנו.\n\nאוהבים משרד י.שפירא ושות' עורכי דין{video_text}",
                "משפחתי": f"היי {selected_employee}, המון מזל טוב ליום ההולדת! 🎂\nשתהיה שנה מדהימה, מלאה בכיף ובשורות טובות.\n\nאוהבים משרד י.שפירא ושות' עורכי דין{video_text}",
            }
            wishes_type = st.radio("סגנון הברכה:", list(wishes_options.keys()), horizontal=True)
            final_message = wishes_options[wishes_type]
            
            st.text_area("תוכן ההודעה:", final_message, height=150)
            wa_link_bday = create_whatsapp_link(emp_phone, final_message)
            
            st.markdown(f'''<br><a href="{wa_link_bday}" target="_blank" style="text-decoration: none;"><button>🎁 שלח ברכה מעוצבת</button></a>''', unsafe_allow_html=True)
    else:
        st.warning("המאגר ריק. נא לטעון נתונים.")

# ==========================
# מסך 3: הודעה בתפוצה רחבה (הפיצ'ר החדש)
# ==========================
elif menu == "הודעה בתפוצה רחבה":
    st.markdown("<h2>📢 שליחת הודעה לכולם</h2>", unsafe_allow_html=True)
    
    st.info("💡 טיפ: וואטסאפ לא מאפשר שליחה המונית בלחיצה אחת. הכלי הזה יעזור לך להכין את ההודעה ולהעתיק את מספרי הטלפון ל'רשימת תפוצה' בוואטסאפ.")
    
    general_msg = st.text_area("כתבי כאן את ההודעה לכל העובדים:", height=150)
    
    if general_msg:
        st.markdown("### שלב 1: העתקת המספרים")
        df = load_data()
        if not df.empty:
            # יצירת רשימת מספרים מופרדת בפסיקים
            all_phones = df['טלפון'].astype(str).str.replace('.0', '', regex=False).tolist()
            phones_text = ",".join(all_phones)
            
            st.code(phones_text, language="text")
            st.caption("העתיקי את המספרים האלו והדביקי אותם ביצירת רשימת תפוצה בוואטסאפ.")
            
            st.markdown("### שלב 2: העתקת ההודעה")
            st.code(general_msg, language="text")
            
        else:
            st.error("אין עובדים ברשימה להצגת מספרים.")

# ==========================
# מסך 4: ניהול עובדים
# ==========================
elif menu == "ניהול עובדים":
    st.markdown("<h2>👥 מאגר עובדים</h2>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader("📂 גרירת קובץ אקסל לטעינה מהירה", type=['xlsx', 'xls', 'csv'])
    
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
                st.success(f"✅ רשימת העובדים עודכנה! ({len(new_df)} רשומות)")
                st.rerun()
            else:
                st.error("⚠️ מבנה הקובץ שגוי. חובה עמודות: שם, טלפון, תאריך לידה.")
        except Exception as e:
            st.error(f"שגיאה: {e}")

    st.markdown("---")
    st.markdown("#### ✏️ עריכת טבלה")
    
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

    if st.button("💾 שמור שינויים"):
        save_data(edited_df)
        st.success("הנתונים נשמרו בהצלחה!")
