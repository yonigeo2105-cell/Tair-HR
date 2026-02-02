import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse
import os

# --- הגדרות עמוד ---
st.set_page_config(page_title="HR Manager", layout="centered", page_icon="🌸")

# --- עיצוב יוקרתי ונקי (Clean & Chic) ---
st.markdown("""
    <style>
    /* פונט נקי */
    @import url('https://fonts.googleapis.com/css2?family=Rubik:wght@300;400;500;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Rubik', sans-serif;
        direction: rtl;
    }

    /* רקע נקי ואלגנטי */
    .stApp {
        background-color: #fdfbfd;
        background-image: radial-gradient(#f3e5f5 1px, transparent 1px);
        background-size: 20px 20px;
    }

    /* כותרות */
    h1 {
        color: #880e4f;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0px;
    }
    
    h3 {
        color: #bc477b;
        text-align: center;
        font-weight: 300;
        margin-top: -10px;
        font-size: 1.2rem;
    }

    /* קופסאות (Cards) */
    .css-1r6slb0, .stForm {
        background-color: #ffffff;
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.03);
        border: 1px solid #fce4ec;
    }

    /* כפתורים משודרגים */
    .stButton>button {
        background: linear-gradient(135deg, #ec407a 0%, #c2185b 100%);
        color: white;
        border-radius: 12px;
        border: none;
        padding: 12px 24px;
        font-weight: 500;
        width: 100%;
        box-shadow: 0 4px 10px rgba(233, 30, 99, 0.2);
        transition: transform 0.2s;
    }
    
    .stButton>button:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 15px rgba(233, 30, 99, 0.3);
        color: white;
    }

    /* שדות קלט */
    .stTextInput input, .stDateInput input, .stTimeInput input {
        border-radius: 10px;
        border: 1px solid #e1bee7;
        padding: 10px;
    }
    
    /* הסתרת אלמנטים מיותרים */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    </style>
    """, unsafe_allow_html=True)

# --- לוגו וכותרת ---
st.markdown("<h1>HR Manager 🌸</h1>", unsafe_allow_html=True)
st.markdown("<h3>משרד י.שפירא ושות'</h3>", unsafe_allow_html=True)
st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

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
        # קריאה עם המרת טלפון לטקסט
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

# --- תפריט צד נקי ---
with st.sidebar:
    st.markdown("### 🌸 תפריט")
    menu = st.radio("", ["זימון לראיון", "ימי הולדת", "ניהול עובדים"])

# ==========================
# מסך 1: זימון לראיון
# ==========================
if menu == "זימון לראיון":
    st.subheader("📅 זימון מועמד לראיון")
    
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            candidate_name = st.text_input("שם המועמד/ת")
            phone_number = st.text_input("מספר טלפון")
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
        st.markdown("**תצוגה מקדימה:**")
        st.text_area("", message_body, height=120)
        
        wa_link = create_whatsapp_link(phone_number, message_body)
        
        st.markdown(f'''
            <br>
            <a href="{wa_link}" target="_blank" style="text-decoration: none; display: flex; justify-content: center;">
                <button style="
                    background: #25D366; 
                    color: white; 
                    border: none; 
                    padding: 12px 30px; 
                    border-radius: 50px; 
                    font-size: 18px; 
                    cursor: pointer; 
                    box-shadow: 0 4px 10px rgba(37, 211, 102, 0.3);">
                    📞 פתח וואטסאפ לשליחה
                </button>
            </a>
            ''', unsafe_allow_html=True)

# ==========================
# מסך 2: ימי הולדת
# ==========================
elif menu == "ימי הולדת":
    st.subheader("🎂 חגיגות יום הולדת")
    
    with st.expander("🎥 לחצי כאן להגדרת קישור לסרטון"):
        video_link = st.text_input("קישור לסרטון:", placeholder="https://youtu.be/...")
    
    df = load_data()
    if not df.empty:
        df['תאריך לידה'] = pd.to_datetime(df['תאריך לידה'], errors='coerce')
        
        # אזור בחירה
        st.markdown("<br>", unsafe_allow_html=True)
        employee_names = df['שם העובד'].tolist()
        selected_employee = st.selectbox("למי חוגגים?", employee_names)
        
        if selected_employee:
            emp_data = df[df['שם העובד'] == selected_employee].iloc[0]
            emp_phone = emp_data['טלפון']
            video_text = f"\n\n🎬 הכנו לך משהו קטן: {video_link}" if video_link else ""
            
            st.markdown("**בחר סגנון:**")
            wishes_options = {
                "רשמי": f"מזל טוב {selected_employee}! 🎉\nיום הולדת שמח! מאחלים לך שנה של צמיחה, הצלחות והמון רגעים מאושרים.\nשמחים שאת/ה חלק מהצוות שלנו.\n\nאוהבים משרד י.שפירא ושות' עורכי דין{video_text}",
                "משפחתי": f"היי {selected_employee}, המון מזל טוב ליום ההולדת! 🎂\nשתהיה שנה מדהימה, מלאה בכיף ובשורות טובות.\n\nאוהבים משרד י.שפירא ושות' עורכי דין{video_text}",
            }
            wishes_type = st.radio("", list(wishes_options.keys()), horizontal=True, label_visibility="collapsed")
            final_message = wishes_options[wishes_type]
            
            st.text_area("", final_message, height=180)
            wa_link_bday = create_whatsapp_link(emp_phone, final_message)
            
            st.markdown(f'''
                <br>
                <a href="{wa_link_bday}" target="_blank" style="text-decoration: none; display: flex; justify-content: center;">
                    <button style="
                        background: linear-gradient(135deg, #ec407a 0%, #c2185b 100%);
                        color: white; 
                        border: none; 
                        padding: 12px 40px; 
                        border-radius: 50px; 
                        font-size: 18px; 
                        cursor: pointer; 
                        box-shadow: 0 4px 15px rgba(233, 30, 99, 0.4);">
                        🎁 שלח ברכה
                    </button>
                </a>
                ''', unsafe_allow_html=True)
    else:
        st.warning("אין נתונים. נא לטעון קובץ ב'ניהול עובדים'.")

# ==========================
# מסך 3: ניהול עובדים (עם עריכה חיה)
# ==========================
elif menu == "ניהול עובדים":
    st.subheader("👥 ניהול מאגר עובדים")
    
    st.info("💡 חדש: ניתן לערוך את פרטי העובדים ישירות בתוך הטבלה למטה! בסיום העריכה יש ללחוץ על הכפתור 'שמור שינויים'.")
    
    # אזור העלאת קובץ
    uploaded_file = st.file_uploader("טעינת קובץ אקסל ראשוני", type=['xlsx', 'xls', 'csv'])
    
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
                st.success(f"נטענו {len(new_df)} רשומות חדשות!")
                st.rerun()
            else:
                st.error("הקובץ לא תקין. חסרות עמודות: שם, טלפון, תאריך לידה.")
        except Exception as e:
            st.error(f"שגיאה: {e}")

    st.markdown("---")
    
    # --- עריכת הטבלה (הפיצ'ר החדש) ---
    st.markdown("### ✏️ עריכת הרשימה")
    
    df = load_data()
    
    # טבלה עריכה אינטראקטיבית
    edited_df = st.data_editor(
        df,
        num_rows="dynamic",  # מאפשר להוסיף ולמחוק שורות
        column_config={
            "שם העובד": st.column_config.TextColumn("שם מלא", required=True),
            "טלפון": st.column_config.TextColumn("טלפון", required=True),
            "תאריך לידה": st.column_config.DateColumn("תאריך לידה", format="DD/MM/YYYY")
        },
        use_container_width=True,
        hide_index=True
    )

    # כפתור שמירה בולט
    if st.button("💾 שמור את כל השינויים בטבלה", type="primary"):
        save_data(edited_df)
        st.balloons()
        st.success("הנתונים נשמרו בהצלחה!")
