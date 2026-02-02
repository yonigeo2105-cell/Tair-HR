import streamlit as st
import pandas as pd
from datetime import datetime
import urllib.parse
import os

# --- הגדרות עמוד ---
st.set_page_config(page_title="HR Manager - Shapira Law", layout="centered", page_icon="⚖️")

# --- עיצוב מותאם אישית (CSS) ---
st.markdown("""
    <style>
    /* רקע כללי לאפליקציה - גרדיאנט עדין */
    .stApp {
        background-image: linear-gradient(to bottom right, #fff0f5, #ffffff);
    }
    
    /* עיצוב כותרות */
    h1 {
        color: #5D3A5D; /* סגול חציל עמוק */
        font-family: 'Helvetica Neue', sans-serif;
        text-align: center;
        border-bottom: 2px solid #D8BFD8;
        padding-bottom: 10px;
    }
    
    h2, h3 {
        color: #8B5F8B; /* סגול בהיר יותר */
    }
    
    /* עיצוב כפתורים */
    .stButton>button {
        background-color: #C08497; /* ורוד עתיק */
        color: white;
        border-radius: 20px;
        border: none;
        padding: 10px 24px;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background-color: #B06D85; /* ורוד כהה יותר במעבר עכבר */
        color: white;
        transform: scale(1.02);
    }
    
    /* מסגרות לקלט */
    .stTextInput>div>div>input {
        border-radius: 10px;
        border: 1px solid #D8BFD8;
    }
    
    /* תיקון ליישור טקסט */
    .css-10trblm {
        text-align: right;
    }
    </style>
    """, unsafe_allow_html=True)

# --- כותרת ראשית ---
st.title("⚖️ HR Manager")
st.markdown("<h3 style='text-align: center; color: #5D3A5D;'>משרד י.שפירא ושות'</h3>", unsafe_allow_html=True)
st.markdown("---")

# --- פונקציות עזר ---

def get_hebrew_day(date_obj):
    """מחזיר את היום בשבוע בעברית"""
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
        return pd.read_csv('employees.csv')
    return pd.DataFrame(columns=["שם העובד", "תאריך לידה", "טלפון"])

def save_data(df):
    df.to_csv('employees.csv', index=False)

# --- תפריט צד ---
# עיצוב מותאם לתפריט הצד לא נתמך מלא ב-CSS פשוט, אבל הוא יקבל את הרקע הכללי
menu = st.sidebar.radio("תפריט ראשי", ["זימון לראיון", "ימי הולדת", "ניהול עובדים"])

# ==========================
# מסך 1: זימון לראיון
# ==========================
if menu == "זימון לראיון":
    st.header("📅 זימון מועמד לראיון")
    
    # שימוש ב-Container כדי לתת קצת "אוויר"
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            candidate_name = st.text_input("שם המועמד/ת")
            phone_number = st.text_input("מספר טלפון (נייד)")
        
        with col2:
            interview_date = st.date_input("תאריך הראיון")
            interview_time = st.time_input("שעה")
    
    if candidate_name and phone_number:
        # חישוב התאריך והיום
        date_str = interview_date.strftime('%d/%m')
        time_str = interview_time.strftime('%H:%M')
        day_hebrew = get_hebrew_day(interview_date)
        
        # הודעה
        message_body = (
            f"היי {candidate_name}, זאת תאיר ממשרד עורכי דין י.שפירא.\n"
            f"בהמשך לשיחתנו נקבע ראיון עבודה ליום {day_hebrew} בתאריך ה-{date_str} בשעה {time_str}.\n"
            f"כתובתנו נירים 4 תל אביב. אני יושבת בקומה ה-2.\n\n"
            f"לכל שאלה אני זמינה במספר הזה, אנא אשר/י את קבלת ההודעה."
        )
        
        st.info("תצוגה מקדימה להודעה:")
        st.text_area("", message_body, height=150)
        
        wa_link = create_whatsapp_link(phone_number, message_body)
        
        # כפתור עם אייקון
        st.markdown(f'''
            <div style="text-align: center; margin-top: 20px;">
                <a href="{wa_link}" target="_blank" style="text-decoration: none;">
                    <button style="
                        background-color: #25D366; 
                        color: white; 
                        border: none; 
                        padding: 12px 25px; 
                        border-radius: 25px; 
                        font-size: 18px; 
                        cursor: pointer; 
                        box-shadow: 0px 4px 6px rgba(0,0,0,0.1);">
                        📞 לחץ לשליחה בוואטסאפ
                    </button>
                </a>
            </div>
            ''', unsafe_allow_html=True)

# ==========================
# מסך 2: ימי הולדת
# ==========================
elif menu == "ימי הולדת":
    st.header("🎂 חגיגות יום הולדת")
    
    st.markdown("### 🎥 סרטון יום הולדת")
    video_link = st.text_input("הדבק כאן קישור לסרטון (YouTube/Drive):", 
                               placeholder="למשל: https://youtu.be/abcd123")
    
    st.markdown("---")
    
    df = load_data()
    
    if not df.empty:
        df['תאריך לידה'] = pd.to_datetime(df['תאריך לידה'])
        employee_names = df['שם העובד'].tolist()
        selected_employee = st.selectbox("בחר עובד לשליחת ברכה:", employee_names)
        
        if selected_employee:
            emp_data = df[df['שם העובד'] == selected_employee].iloc[0]
            emp_phone = emp_data['טלפון']
            
            video_text = f"\n\n🎬 הכנו לך משהו קטן: {video_link}" if video_link else ""

            st.subheader("בחר סגנון ברכה:")
            wishes_options = {
                "רשמי וחם": f"מזל טוב {selected_employee}! 🎉\nיום הולדת שמח! מאחלים לך שנה של צמיחה, הצלחות והמון רגעים מאושרים.\nשמחים שאת/ה חלק מהצוות שלנו.\n\nאוהבים משרד י.שפירא ושות' עורכי דין{video_text}",
                "קליל ומשפחתי": f"היי {selected_employee}, המון מזל טוב ליום ההולדת! 🎂\nשתהיה שנה מדהימה, מלאה בכיף ובשורות טובות.\n\nאוהבים משרד י.שפירא ושות' עורכי דין{video_text}",
            }
            
            wishes_type = st.radio("", list(wishes_options.keys()), horizontal=True)
            final_message = wishes_options[wishes_type]
            
            st.text_area("ההודעה שתשלח:", final_message, height=180)
            
            wa_link_bday = create_whatsapp_link(emp_phone, final_message)
            
            st.markdown(f'''
                <div style="text-align: center; margin-top: 20px;">
                    <a href="{wa_link_bday}" target="_blank" style="text-decoration: none;">
                        <button style="
                            background-color: #C08497; 
                            color: white; 
                            border: none; 
                            padding: 12px 25px; 
                            border-radius: 25px; 
                            font-size: 18px; 
                            cursor: pointer; 
                            box-shadow: 0px 4px 6px rgba(0,0,0,0.1);">
                            🎁 שלח ברכה מעוצבת
                        </button>
                    </a>
                </div>
                ''', unsafe_allow_html=True)
    else:
        st.warning("עדיין אין עובדים במערכת. עבור ללשונית 'ניהול עובדים' כדי להוסיף.")

# ==========================
# מסך 3: ניהול עובדים
# ==========================
elif menu == "ניהול עובדים":
    st.header("👥 ניהול מאגר עובדים")
    
    with st.form("add_employee"):
        st.write("הוספת עובד חדש:")
        new_name = st.text_input("שם מלא")
        new_phone = st.text_input("טלפון")
        new_bday = st.date_input("תאריך לידה", min_value=datetime(1950, 1, 1))
        
        # כפתור שמירה מעוצב
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

    st.markdown("### רשימת עובדים קיימת")
    df = load_data()
    if not df.empty:
        st.dataframe(df)
        if st.button("מחיקת כל הנתונים (איפוס)"):
            save_data(pd.DataFrame(columns=["שם העובד", "תאריך לידה", "טלפון"]))
            st.rerun()
