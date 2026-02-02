import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse
import os

# --- הגדרות עמוד ---
st.set_page_config(page_title="HR Manager - Shapira Law", layout="centered", page_icon="⚖️")

# --- עיצוב CSS מתקדם (Premium UI) ---
st.markdown("""
    <style>
    /* ייבוא פונט מודרני בעברית */
    @import url('https://fonts.googleapis.com/css2?family=Heebo:wght@300;400;700&display=swap');

    /* הגדרת פונט כללית */
    html, body, [class*="css"] {
        font-family: 'Heebo', sans-serif;
        direction: rtl;
    }

    /* רקע האפליקציה - גרדיאנט עדין */
    .stApp {
        background: linear-gradient(180deg, #FFF5F7 0%, #FFFFFF 100%);
    }

    /* עיצוב כותרת ראשית */
    h1 {
        color: #880e4f;
        text-align: center;
        font-weight: 700;
        text-shadow: 0px 2px 4px rgba(0,0,0,0.1);
        padding-bottom: 20px;
    }

    h3 {
        color: #ad1457;
        font-weight: 400;
    }

    /* עיצוב שדות קלט (Input Fields) */
    .stTextInput input, .stDateInput input, .stTimeInput input, .stSelectbox div[data-baseweb="select"] {
        background-color: #ffffff;
        border: 1px solid #f8bbd0;
        border-radius: 12px;
        padding: 10px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.02);
        transition: all 0.3s;
    }

    .stTextInput input:focus, .stDateInput input:focus {
        border-color: #ec407a;
        box-shadow: 0 2px 8px rgba(236, 64, 122, 0.2);
    }

    /* עיצוב כפתורים - גרדיאנט יוקרתי */
    .stButton>button {
        background: linear-gradient(45deg, #ec407a, #d81b60);
        color: white;
        border-radius: 30px;
        border: none;
        padding: 12px 30px;
        font-weight: bold;
        font-size: 16px;
        box-shadow: 0 4px 15px rgba(216, 27, 96, 0.3);
        transition: all 0.3s ease;
        width: 100%;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(216, 27, 96, 0.4);
        background: linear-gradient(45deg, #f06292, #e91e63);
        color: white;
    }

    /* עיצוב מסגרות (Containers) */
    div[data-testid="stForm"] {
        background-color: white;
        padding: 30px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
        border: 1px solid #fce4ec;
    }
    
    /* הסתרת התפריט העליון של סטרימליט למראה נקי */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    </style>
    """, unsafe_allow_html=True)

# --- לוגו וכותרת ---
st.markdown("<h1 style='font-size: 3rem;'>⚖️ HR Manager</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>משרד י.שפירא ושות' | פורטל ניהול</h3>", unsafe_allow_html=True)
st.markdown("---")

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

# --- תפריט צד מעוצב ---
with st.sidebar:
    st.markdown("### 📌 תפריט ניווט")
    menu = st.radio("", ["זימון לראיון", "ימי הולדת", "ניהול עובדים"])
    st.markdown("---")
    st.info("💡 טיפ: ניתן לגרור קבצי אקסל במסך 'ניהול עובדים' לטעינה מהירה.")

# ==========================
# מסך 1: זימון לראיון
# ==========================
if menu == "זימון לראיון":
    st.markdown("## 📅 זימון מועמד לראיון")
    
    # שימוש בטופס כדי לתת מסגרת יפה
    with st.container():
        st.markdown('<div style="background-color: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.03);">', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            candidate_name = st.text_input("שם המועמד/ת")
            phone_number = st.text_input("מספר טלפון (נייד)")
        with col2:
            interview_date = st.date_input("תאריך הראיון")
            interview_time = st.time_input("שעה")
            
        st.markdown('</div>', unsafe_allow_html=True)
    
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
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.info("תצוגה מקדימה להודעה:")
        st.text_area("", message_body, height=130)
        
        wa_link = create_whatsapp_link(phone_number, message_body)
        
        st.markdown(f'''
            <div style="text-align: center; margin-top: 25px;">
                <a href="{wa_link}" target="_blank" style="text-decoration: none;">
                    <button style="
                        background: linear-gradient(45deg, #25D366, #128C7E);
                        color: white; 
                        border: none; 
                        padding: 15px 40px; 
                        border-radius: 50px; 
                        font-size: 18px; 
                        font-weight: bold;
                        cursor: pointer; 
                        box-shadow: 0 4px 15px rgba(37, 211, 102, 0.4);
                        transition: transform 0.2s;">
                        📞 לחץ לשליחה בוואטסאפ
                    </button>
                </a>
            </div>
            ''', unsafe_allow_html=True)

# ==========================
# מסך 2: ימי הולדת
# ==========================
elif menu == "ימי הולדת":
    st.markdown("## 🎂 חגיגות יום הולדת")
    
    with st.expander("🎥 הגדרות סרטון (לחץ לפתיחה)", expanded=True):
        video_link = st.text_input("קישור לסרטון (YouTube/Drive):", placeholder="https://youtu.be/...")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    df = load_data()
    if not df.empty:
        df['תאריך לידה'] = pd.to_datetime(df['תאריך לידה'], errors='coerce')
        
        # כרטיס מעוצב לבחירת עובד
        st.markdown('<div style="background-color: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.03);">', unsafe_allow_html=True)
        employee_names = df['שם העובד'].tolist()
        selected_employee = st.selectbox("🎉 למי חוגגים היום?", employee_names)
        st.markdown('</div>', unsafe_allow_html=True)
        
        if selected_employee:
            emp_data = df[df['שם העובד'] == selected_employee].iloc[0]
            emp_phone = emp_data['טלפון']
            video_text = f"\n\n🎬 הכנו לך משהו קטן: {video_link}" if video_link else ""
            
            st.markdown("### בחר סגנון ברכה:")
            wishes_options = {
                "רשמי וחם": f"מזל טוב {selected_employee}! 🎉\nיום הולדת שמח! מאחלים לך שנה של צמיחה, הצלחות והמון רגעים מאושרים.\nשמחים שאת/ה חלק מהצוות שלנו.\n\nאוהבים משרד י.שפירא ושות' עורכי דין{video_text}",
                "קליל ומשפחתי": f"היי {selected_employee}, המון מזל טוב ליום ההולדת! 🎂\nשתהיה שנה מדהימה, מלאה בכיף ובשורות טובות.\n\nאוהבים משרד י.שפירא ושות' עורכי דין{video_text}",
            }
            wishes_type = st.radio("", list(wishes_options.keys()), horizontal=True)
            final_message = wishes_options[wishes_type]
            
            st.text_area("", final_message, height=180)
            wa_link_bday = create_whatsapp_link(emp_phone, final_message)
            
            st.markdown(f'''
                <div style="text-align: center; margin-top: 30px;">
                    <a href="{wa_link_bday}" target="_blank" style="text-decoration: none;">
                        <button style="
                            background: linear-gradient(45deg, #ec407a, #d81b60);
                            color: white; 
                            border: none; 
                            padding: 15px 50px; 
                            border-radius: 50px; 
                            font-size: 20px; 
                            font-weight: bold;
                            cursor: pointer; 
                            box-shadow: 0 5px 20px rgba(236, 64, 122, 0.5);">
                            🎁 שלח ברכה מעוצבת
                        </button>
                    </a>
                </div>
                ''', unsafe_allow_html=True)
    else:
        st.warning("המאגר ריק. עבור ל'ניהול עובדים' כדי לטעון נתונים.")

# ==========================
# מסך 3: ניהול עובדים
# ==========================
elif menu == "ניהול עובדים":
    st.markdown("## 👥 ניהול מאגר עובדים")
    
    st.success("כאן ניתן לטעון קובץ אקסל והמערכת תעדכן את הרשימה אוטומטית.")
    
    # אזור העלאה מעוצב
    uploaded_file = st.file_uploader("גרור לכאן קובץ אקסל (Excel/CSV)", type=['xlsx', 'xls', 'csv'])
    
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
                st.balloons() # קצת אפקטים של בלונים כשהטעינה מצליחה
                st.success(f"✅ עודכנו {len(new_df)} עובדים בהצלחה!")
                st.rerun()
            else:
                st.error("⚠️ לא נמצאו העמודות המתאימות. וודא שיש: שם, טלפון, תאריך לידה.")
        except Exception as e:
            st.error(f"שגיאה בטעינת הקובץ: {e}")

    st.markdown("---")

    with st.expander("➕ הוספת עובד בודד ידנית"):
        with st.form("add_employee"):
            new_name = st.text_input("שם מלא")
            new_phone = st.text_input("טלפון")
            new_bday = st.date_input("תאריך לידה", min_value=datetime(1950, 1, 1))
            
            if st.form_submit_button("שמור עובד"):
                if new_name and new_phone:
                    df = load_data()
                    new_data = pd.DataFrame({
                        "שם העובד": [new_name],
                        "תאריך לידה": [new_bday],
                        "טלפון": [new_phone]
                    })
                    df = pd.concat([df, new_data]).drop_duplicates(subset=['שם העובד', 'טלפון'], keep='last')
                    save_data(df)
                    st.success("נשמר!")
                    st.rerun()

    st.markdown("### 📋 רשימת העובדים במערכת")
    df = load_data()
    if not df.empty:
        st.dataframe(df, use_container_width=True)
        if st.button("🗑️ מחק את כל הרשימה"):
            save_data(pd.DataFrame(columns=["שם העובד", "תאריך לידה", "טלפון"]))
            st.rerun()
