import streamlit as st
import numpy as np
import pandas as pd
import joblib
from datetime import datetime

model = joblib.load('models/sleep_model.pkl')

st.set_page_config(
    page_title="Sleep Quality Predictor",
    page_icon="🛌",
    layout="centered"
)

st.markdown("<h1 style='text-align: center; color: #6C63FF;'>Sleep Quality Predictor 🛌</h1>", unsafe_allow_html=True)
st.write("Monitor and improve your sleep with daily input data.")

st.header("Enter your daily habits:")

sleep_duration = st.number_input("Sleep Duration (hours)", min_value=0.0, max_value=24.0, step=0.1)
bedtime = st.time_input("Bedtime")
wake_time = st.time_input("Wake-up Time")
exercise_duration = st.number_input("Exercise Duration (minutes)", min_value=0, max_value=300)
caffeine_intake = st.selectbox("Caffeine Intake", ["None", "Low", "Moderate", "High"])
screen_time = st.number_input("Screen Time Before Bed (minutes)", min_value=0, max_value=600)
stress_level = st.slider("Stress Level (0–10)", min_value=0, max_value=10)
mood = st.selectbox("Mood Before Sleep", ["Happy", "Neutral", "Sad", "Anxious"])
sleep_interruptions = st.radio("Sleep Interruptions", ["Yes", "No"])

caffeine_map = {"None": 0, "Low": 1, "Moderate": 2, "High": 3}
caffeine_value = caffeine_map[caffeine_intake]

mood_map = {"Happy": 0, "Neutral": 1, "Sad": 2, "Anxious": 3}
mood_value = mood_map[mood]

interruptions_map = {"No": 0, "Yes": 1}
interruptions_value = interruptions_map[sleep_interruptions]


bedtime_hours = bedtime.hour + bedtime.minute/60
wake_hours = wake_time.hour + wake_time.minute/60


if st.button("Predict Sleep Quality"):
    features = np.array([[sleep_duration, exercise_duration, caffeine_value, screen_time, stress_level]])
    prediction = model.predict(features)[0]

    categories = ["Average", "Good", "Poor"]  
    predicted_quality = categories[prediction % len(categories)]

    st.success(f"Predicted Sleep Quality: {predicted_quality}")

    tips = []
    if sleep_duration < 6:
        tips.append("Try increasing your sleep duration to at least 7–8 hours.")
    if screen_time > 120:
        tips.append("Reduce screen time before bed; aim for less than 1–2 hours.")
    if caffeine_value >= 2:
        tips.append("Avoid caffeine in the evening to improve sleep quality.")
    if exercise_duration < 20:
        tips.append("Include at least 20–30 minutes of physical activity daily.")
    if stress_level >= 7:
        tips.append("Practice relaxation techniques like meditation or deep breathing.")
    if mood_value >= 2:
        tips.append("Consider calming activities before bedtime to improve mood.")
    if sleep_interruptions == "Yes":
        tips.append("Maintain a quiet, comfortable sleep environment and consistent bedtime.")

    if not tips:
        tips.append("Great! Your habits look healthy. Keep maintaining them.")

    for tip in tips:
        st.info(tip)

    history = pd.DataFrame({
        'Date': [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        'Sleep_Duration':[sleep_duration],
        'Bedtime':[bedtime.strftime("%H:%M")],
        'Wake_Time':[wake_time.strftime("%H:%M")],
        'Exercise':[exercise_duration],
        'Caffeine':[caffeine_intake],
        'Screen_Time':[screen_time],
        'Stress':[stress_level],
        'Mood':[mood],
        'Sleep_Interruptions':[sleep_interruptions],
        'Predicted_Quality':[predicted_quality]
    })

    history_file = "sleep_history.csv"
    history.to_csv(history_file, mode='a', index=False, header=not pd.io.common.file_exists(history_file))


if st.checkbox("View Past Predictions"):
    try:
        df_history = pd.read_csv("sleep_history.csv")
        st.dataframe(df_history)

      
        st.subheader("Sleep Quality Trends")
        import seaborn as sns
        import matplotlib.pyplot as plt

        plt.figure(figsize=(8,4))
        sns.countplot(data=df_history, x='Predicted_Quality', palette="cool")
        plt.title("Sleep Quality Trend")
        st.pyplot(plt)

    except FileNotFoundError:
        st.warning("No history found yet.")
