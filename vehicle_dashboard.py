import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from streamlit_autorefresh import st_autorefresh

# ✅ Set page config FIRST (IMPORTANT!)
st.set_page_config(page_title="Kiran's Smart Automotive Dashboard", layout="wide")

# Session State Initialization
if "start" not in st.session_state:
    st.session_state.start = False
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=[
        "Time", "Speed", "RPM", "Fuel", "Battery", "Temperature", "Gear", "Distance", "Alert"
    ])

# ✅ Auto-refresh every second if monitoring is ON
if st.session_state.start:
    st_autorefresh(interval=1000, key="auto_refresh")

# Title
st.title("🚘 Kiran's Smart Automotive Dashboard")

# Sidebar
with st.sidebar:
    st.header("About Project")
    st.markdown("""
    **By:** Kiran Bishnoi  
    **Tech Used:** Python, Streamlit, NumPy, Pandas
    **Purpose:** Simulates real-time vehicle sensor metrics.
    """)

# Buttons
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("▶️ Start Monitoring"):
        st.session_state.start = True
with col2:
    if st.button("⏹️ Stop Monitoring"):
        st.session_state.start = False
with col3:
    if not st.session_state.data.empty:
        csv = st.session_state.data.to_csv(index=False).encode('utf-8')
        st.download_button("📤 Export CSV", csv, file_name="vehicle_logs.csv", mime="text/csv")

# Gear Logic
def get_gear(speed):
    if speed == 0: return "P"
    elif speed < 10: return "1"
    elif speed < 30: return "2"
    elif speed < 50: return "3"
    elif speed < 70: return "4"
    else: return "5"

# Alert Logic
def get_alert(temp, battery):
    alerts = []
    if temp > 110: alerts.append("🔥 Overheat")
    if battery < 11.5: alerts.append("🔋 Battery Low")
    return " | ".join(alerts) if alerts else "✅ OK"

# Generate Sensor Data
def generate_data():
    speed = np.random.randint(0, 120)
    rpm = np.random.randint(1000, 5000)
    fuel = np.random.randint(10, 100)
    battery = round(np.random.uniform(11.0, 14.8), 2)
    temp = np.random.randint(70, 120)
    gear = get_gear(speed)
    alert = get_alert(temp, battery)
    distance = round(speed * 0.01, 2)

    return {
        "Time": datetime.now().strftime("%H:%M:%S"),
        "Speed": speed,
        "RPM": rpm,
        "Fuel": fuel,
        "Battery": battery,
        "Temperature": temp,
        "Gear": gear,
        "Distance": distance,
        "Alert": alert
    }

# Add new row if monitoring is ON
if st.session_state.start:
    new_data = generate_data()
    new_df = pd.DataFrame([new_data])
    st.session_state.data = pd.concat([st.session_state.data, new_df], ignore_index=True)

# Show Dashboard
if not st.session_state.data.empty:
    latest = st.session_state.data.iloc[-1]

    st.subheader("📊 Live Vehicle Metrics")
    cols = st.columns(8)
    cols[0].metric("Speed", latest["Speed"])
    cols[1].metric("RPM", latest["RPM"])
    cols[2].metric("Fuel", f'{latest["Fuel"]}%')
    cols[3].metric("Battery", f'{latest["Battery"]}V')
    cols[4].metric("Temp", f'{latest["Temperature"]}°C')
    cols[5].metric("Gear", latest["Gear"])
    cols[6].metric("Distance", f'{latest["Distance"]} km')
    cols[7].metric("Alert", latest["Alert"])

    # Charts
    st.subheader("📈 Real-Time Sensor Graphs")
    df = st.session_state.data.tail(20)
    fig, ax = plt.subplots(3, 2, figsize=(10, 8))

    ax[0][0].plot(df["Time"], df["Speed"], color="blue")
    ax[0][0].set_title("Speed")
    ax[0][1].plot(df["Time"], df["RPM"], color="green")
    ax[0][1].set_title("RPM")
    ax[1][0].plot(df["Time"], df["Fuel"], color="orange")
    ax[1][0].set_title("Fuel Level")
    ax[1][1].plot(df["Time"], df["Battery"], color="red")
    ax[1][1].set_title("Battery Voltage")
    ax[2][0].plot(df["Time"], df["Temperature"], color="purple")
    ax[2][0].set_title("Engine Temperature")

    for axes in ax.flat:
        axes.tick_params(axis='x', labelrotation=45)
    st.pyplot(fig)

    # Table
    st.subheader("📋 Live Sensor Data Table")
    st.dataframe(df, use_container_width=True)
