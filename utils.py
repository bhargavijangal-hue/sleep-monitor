import datetime

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
