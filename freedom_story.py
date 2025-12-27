import streamlit as st
import plotly.graph_objects as go

# הגדרות עמוד
st.set_page_config(page_title="סיפור החופש הכלכלי", layout="centered")

# CSS - יישור לימין, שילוב פקדים בטקסט והחזרת כפתורי +/-
st.markdown("""
    <style>
    .stApp { direction: rtl; text-align: right; background-color: #fcfcfc; }
    
    /* עיצוב הפסקה המרכזית */
    .story-container {
        font-size: 24px;
        line-height: 2.5;
        color: #2c3e50;
    }

    /* עיצוב שדות המספרים שיהיו חלק מהשורה */
    div[data-testid="stNumberInput"], div[data-testid="stSelectbox"] {
        display: inline-block !important;
        vertical-align: middle !important;
        margin: 0 4px !important;
    }

    /* גדלים מותאמים למניעת חיתוך */
    .num-small { width: 110px !important; }
    .num-med { width: 150px !important; }
    .num-large { width: 190px !important; }
    .select-small { width: 120px !important; }

    .stNumberInput input, .stSelectbox div[data-baseweb="select"] {
        font-size: 20px !important;
        font-weight: bold !important;
        color: #1e3a8a !important;
        text-align: center !important;
        border: none !important;
        border-bottom: 2px solid #bdc3c7 !important;
        background: transparent !important;
    }

    /* הסתרת תוויות labels */
    label { display: none !important; }
    
    .vanguard-header {
        color: #1e3a8a;
        font-size: 42px;
        font-weight: bold;
        text-align: center;
        margin-bottom: 40px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<div class='vanguard-header'>סיפור הפרישה שלך</div>", unsafe_allow_html=True)

# --- תחילת הפסקה ---
# שורה 1: גילאים
col1, col2, col3, col4, col5 = st.columns([1, 1.2, 2.5, 1.2, 0.2])
with col1: st.write("אני בן")
with col2: age = st.number_input("גיל", 20, 80, 35, key="age")
with col3: st.write("ומתכנן לפרוש בגיל")
with col4: ret_age = st.number_input("פרישה", 40, 85, 67, key="ret")
with col5: st.write(".")

# שורה 2: הכנסה ובחירת סוג חיסכון בתוך המשפט
c1, c2, c3, c4, c5, c6 = st.columns([1.2, 1.8, 1.8, 1.2, 1.5, 1.5])
with c1: st.write("אני מרוויח")
with c2: inc_m = st.number_input("שכר", 0, 200000, 20000, step=500, key="inc")
with c3: st.write("₪ בחודש וחוסך")
with c4: save_type = st.selectbox("סוג חיסכון", ["אחוזים", "שקלים"], key="s_type")
with c5: 
    if save_type == "אחוזים":
        save_val = st.number_input("אחוז", 0, 100, 18, key="s_val")
        monthly_deposit = inc_m * (save_val / 100)
    else:
        save_val = st.number_input("סכום", 0, 100000, 3600, step=100, key="s_val_ils")
        monthly_deposit = save_val
with c6: st.write("ממנה לפרישה.")

# שורה 3: צבירה ותשואה
c7, c8, c9, c10, c11 = st.columns([2.5, 2, 3, 1.2, 1])
with c7: st.write("כבר צברתי בחיסכון")
with c8: saved = st.number_input("צבירה", 0, 50000000, 500000, step=10000, key="saved")
with c9: st.write("₪, ואני מצפה לתשואה של")
with c10: yield_val = st.number_input("תשואה", 0.0, 15.0, 6.0, step=0.1, key="yield")
with c11: st.write("אחוזים.")

# שורה 4: יעד פרישה (שוב, בחירה בתוך המשפט)
c12, c13, c14, c15, c16 = st.columns([2, 1.2, 1.2, 1.8, 1.5])
with c12: st.write("בפרישה אצטרך")
with c13: target_type = st.selectbox("סוג יעד", ["אחוזים", "שקלים"], key="t_type")
with c14:
    if target_type == "אחוזים":
        target_val = st.number_input("יעד %", 0, 200, 80, key="t_val")
        target_income = inc_m * (target_val / 100)
    else:
        target_val = st.number_input("יעד ₪", 0, 200000, 16000, step=500, key="t_val_ils")
        target_income = target_val
with c15:
    label_suffix = "מהכנסתי הנוכחית" if target_type == "אחוזים" else "₪ בכל חודש"
    st.write(label_suffix)
with c16: st.write("כדי לחיות ברווחה.")

# --- חישובים ---
years_to_ret = max(0, ret_age - age)
# מקדם דינמי (67=200, 60=210.5)
current_coeff = 200 + ((67 - ret_age) * 1.5)
r = (yield_val / 100) / 12
n = years_to_ret * 12

# צבירה עד הפרישה
future_val = saved * (1 + r)**n + (monthly_deposit * (((1 + r)**n - 1) / r) if r > 0 else monthly_deposit * n)
projected_pension = future_val / current_coeff
confidence = min(100, int((projected_pension / target_income) * 100)) if target_income > 0 else 0

# --- תצוגת תוצאות ---
st.markdown("<br><hr>", unsafe_allow_html=True)
st.markdown(f"""
<div style="text-align: center; font-size: 20px; color: #34495e;">
    יעד קצבה: <b>₪{target_income:,.0f}</b> | קצבה חזויה: <b>₪{projected_pension:,.0f}</b><br>
    <small>מבוסס על תשואה של {yield_val}% עד גיל {ret_age} ומקדם {current_coeff:.1f}</small>
</div>
""", unsafe_allow_html=True)

fig = go.Figure(go.Indicator(
    mode = "gauge+number", value = confidence, number = {'suffix': "%", 'font': {'color': '#1e3a8a'}},
    gauge = {'axis': {'range': [None, 100], 'visible': False}, 'bar': {'color': "#1e3a8a"}}
))
fig.update_layout(height=260, margin=dict(t=10, b=10))
st.plotly_chart(fig, use_container_width=True)

if st.button("לניתוח מעמיק בסימולטור המקצועי ➔"):
    st.info("כאן נחבר את הסימולטור המפורט...")