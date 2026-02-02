import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import urllib.parse
import os

# --- הגדרות עיצוב וכותרת ---
st.set_page_config(page_title="HR Manager - Knobel", layout="centered", page_icon="⚖️")

# כותרת ראשית
st.title("⚖️ HR Manager - משרד קנובל")
st.markdown("---")

# --- פונקציות עזר ---

def create_whatsapp_link(phone, message):
    """מייצר קישור לפתיחת וואטסאפ עם הודעה מוכנה"""
    # ניקוי המספר והתאמה לפורמט בינלאומי (ישראל)
    clean_phone = ''.join(filter(str.isdigit, str(phone)))
    if clean_phone.startswith('0'):
        clean_phone = '972' + clean_phone[1:]
    
    # קידוד ההודעה לקישור
    encoded_message = urllib.parse.quote(message)
    return f"https://wa.me/{clean_phone}?text={encoded_message}"

def load_data():
    """טעינת נתוני עובדים מקובץ"""
    if os.path.exists('employees.csv'):
        return pd.read_csv('employees.csv')
    return pd.DataFrame(columns=["שם העובד", "תאריך לידה", "טלפון"])

def save_data(df):
    """שמירת נתוני עובדים לקובץ"""
    df.to_csv('employees.csv', index=False)

# --- תפריט צד ---
menu = st.sidebar.radio("תפריט ראשי", ["זימון לראיון", "ימי הולדת", "ניהול עובדים"])

# ==========================
# מסך 1: זימון לראיון
# ==========================
if menu == "זימון לראיון":
    st.header("📅 זימון מועמד לראיון")
    
    col1, col2 = st.columns(2)
    with col1:
        candidate_name = st.text_input("שם המועמד/ת")
        phone_number = st.text_input("מספר טלפון (נייד)")
    
    with col2:
        interview_date = st.date_input("תאריך הראיון")
        interview_time = st.time_input("שעה")
    
    # בניית ההודעה
    if candidate_name and phone_number:
        full_date_str = f"{interview_date.strftime('%d/%m/%Y')} בשעה {interview_time.strftime('%H:%M')}"
        
        message_body = (
            f"היי {candidate_name}, כאן תאיר ממשרד עורכי הדין קנובל.\n"
            f"בהמשך לשיחתנו, אשמח לזמן אותך לראיון עבודה אצלנו בתאריך {full_date_str}.\n"
            f"הכתובת שלנו היא: [הכנס כתובת כאן].\n\n"
            f"אודה לאישור הגעה,\n"
            f"אוהבים, משפחת קנובל"
        )
        
        st.info("תצוגה מקדימה להודעה:")
        st.text_area("", message_body, height=150)
        
        wa_link = create_whatsapp_link(phone_number, message_body)
        
        st.markdown(f'''
            <a href="{wa_link}" target="_blank">
                <button style="background-color:#25D366; color:white; border:none; padding:10px 20px; border-radius:5px; font-size:16px; cursor:pointer;">
                    📞 לחץ כאן לשליחה בוואטסאפ
                </button>
            </a>
            ''', unsafe_allow_html=True)

# ==========================
# מסך 2: ימי הולדת
# ==========================
elif menu == "ימי הולדת":
    st.header("🎂 חגיגות יום הולדת")
    
    df = load_data()
    
    if not df.empty:
        # המרת עמודת התאריך לפורמט תאריך אמיתי לחישובים
        df['תאריך לידה'] = pd.to_datetime(df['תאריך לידה'])
        
        # חישוב יום הולדת קרוב
        today = datetime.now()
        current_year = today.year
        
        # יצירת רשימה לבחירה
        employee_names = df['שם העובד'].tolist()
        selected_employee = st.selectbox("בחר עובד לשליחת ברכה:", employee_names)
        
        if selected_employee:
            emp_data = df[df['שם העובד'] == selected_employee].iloc[0]
            emp_phone = emp_data['טלפון']
            
            # אפשרויות לברכות
            st.subheader("בחר סגנון ברכה:")
            wishes_options = {
                "רשמי וחם": f"מזל טוב {selected_employee}! 🎉\nיום הולדת שמח! מאחלים לך שנה של צמיחה, הצלחות והמון רגעים מאושרים.\nשמחים שאת/ה איתנו.\n\nאוהבים, משפחת קנובל",
                "קליל ומשפחתי": f"היי {selected_employee}, המון מזל טוב ליום ההולדת! 🎂\nשתהיה שנה מדהים, מלאה בכיף ובשורות טובות.\n\nאוהבים, משפחת קנובל",
                "קצר ולעניין": f"מזל טוב {selected_employee}!\nיום הולדת שמח והרבה בריאות והצלחה!\n🎈\n\nאוהבים, משפחת קנובל"
            }
            
            wishes_type = st.radio("", list(wishes_options.keys()), horizontal=True)
            final_message = wishes_options[wishes_type]
            
            st.text_area("ההודעה שתשלח:", final_message, height=130)
            
            wa_link_bday = create_whatsapp_link(emp_phone, final_message)
            st.markdown(f'''
                <a href="{wa_link_bday}" target="_blank">
                    <button style="background-color:#25D366; color:white; border:none; padding:10px 20px; border-radius:5px; font-size:16px; cursor:pointer;">
                        🎁 שלח ברכה בוואטסאפ
                    </button>
                </a>
                ''', unsafe_allow_html=True)
    else:
        st.warning("עדיין אין עובדים במערכת. עבור ללשונית 'ניהול עובדים' כדי להוסיף.")

# ==========================
# מסך 3: ניהול עובדים (הוספה)
# ==========================
elif menu == "ניהול עובדים":
    st.header("👥 ניהול מאגר עובדים")
    
    with st.form("add_employee"):
        st.write("הוספת עובד חדש:")
        new_name = st.text_input("שם מלא")
        new_phone = st.text_input("טלפון")
        new_bday = st.date_input("תאריך לידה", min_value=datetime(1950, 1, 1))
        
        submitted = st.form_submit_button("שמור עובד")
        
        if submitted and new_name and new_phone:
            df = load_data()
            new_data = pd.DataFrame({
                "שם העובד": [new_name],
                "תאריך לידה": [new_bday],
                "טלפון": [new_phone]
            })
            df = pd.concat([df, new_data], ignore_index=True)
            save_data(df)
            st.success(f"העובד {new_name} נוסף בהצלחה!")
            st.rerun()

    # הצגת טבלה קיימת
    st.markdown("### רשימת עובדים קיימת")
    df = load_data()
    if not df.empty:
        st.dataframe(df)
        
        # כפתור מחיקה (אופציונלי - פשוט כרגע מוחק את כל הרשימה בדוגמה פשוטה)
        if st.button("ניקוי כל הרשימה (זהירות!)"):
            save_data(pd.DataFrame(columns=["שם העובד", "תאריך לידה", "טלפון"]))
            st.rerun()