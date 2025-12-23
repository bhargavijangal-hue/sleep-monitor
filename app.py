import streamlit as st
from utils import suggest_bedtime, get_sleep_advice

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
