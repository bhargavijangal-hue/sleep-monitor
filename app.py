import streamlit as st
import datetime

# ----------------- UTILITY FUNCTIONS -----------------
# Function to calculate suggested bedtime based on wake-up goal
def suggest_bedtime(wake_time: str, sleep_hours: int = 8):
    wake_hour, wake_min = map(int, wake_time.split(":"))
    wake_dt = datetime.datetime.combine(datetime.date.today(), datetime.time(wake_hour, wake_min))
    sleep_delta = datetime.timedelta(hours=sleep_hours)
    bedtime = wake_dt - sleep_delta
    return bedtime.strftime("%H:%M")

# Function to give simple AI-like advice
def get_sleep_advice(habits: dict):
    advice = []
    if habits.get("caffeine"):
        advice.append("Avoid caffeine 6 hours before bedtime.")
    if habits.get("screen_time"):
        advice.append("Reduce screen exposure 30 mins before sleep.")
    if habits.get("stress_level", 0) > 7:
        advice.append("Try meditation or deep breathing to relax.")
    return advice if advice else ["Your sleep routine looks good!"]

# ----------------- STREAMLIT APP -----------------
st.set_page_config(page_title="AI Sleep Routine Advisor", page_icon="🛌", layout="centered")

# ---- CSS Styling ----
st.markdown("""
    <style>
    body {
        background-image: url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e'); 
        background-size: cover;
    }
    .stButton>button {
        background: linear-gradient(90deg, #6a11cb, #2575fc);
        color: white;
        font-size: 18px;
        border-radius: 10px;
        padding: 10px 20px;
        transition: transform 0.2s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
    }
    </style>
""", unsafe_allow_html=True)

st.title("🛌 AI Sleep Routine Advisor")
st.subheader("Personalized sleep suggestions for better rest")

# ---- User Inputs ----
wake_time = st.time_input("What time do you want to wake up?", value=datetime.time(7, 0))
sleep_hours = st.slider("How many hours do you want to sleep?", 4, 12, 8)

caffeine = st.checkbox("Did you consume caffeine today?")
screen_time = st.checkbox("Heavy screen usage before bed?")
stress_level = st.slider("Stress level today (1-10)", 1, 10, 5)

# ---- Generate Routine ----
if st.button("Generate My Sleep Routine"):
    bedtime = suggest_bedtime(wake_time.strftime("%H:%M"), sleep_hours)
    habits = {
        "caffeine": caffeine,
        "screen_time": screen_time,
        "stress_level": stress_level
    }
    advice = get_sleep_advice(habits)
    
    st.success(f"💤 Suggested bedtime: **{bedtime}**")
    st.subheader("AI Recommendations:")
    for tip in advice:
        st.write(f"• {tip}")
