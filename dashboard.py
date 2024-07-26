import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import time

# Set the layout of the dashboard
st.set_page_config(layout="wide", page_title="Dashboard", page_icon="📊")

# Function to read and update CSV file
@st.cache_data(ttl=60)  # Cache data for 60 seconds
def load_data():
    return pd.read_csv(r'C:\Users\User\Desktop\dashbaord\dht11_data.csv')

def update_data():
    # Here you can add your logic to update the CSV file
    # For demonstration, I'm just reading the file
    data = load_data()
    return data

# Sidebar with switches and sliders
with st.sidebar:
    st.title("Controls")
    pump_toggle = st.toggle("Pump Toggle", value=False)
    st.select_slider("Displayed values:", ["Normalized", "Absolute"]) 
    on = st.toggle("Activate feature")

    if on:
        st.write("Feature activated!")
    pump_seconds = st.slider("Pump Seconds", min_value=0, max_value=60, value=0)
    reset_slave = st.button("Reset Slave")
    generator_toggle = st.toggle("Generator Toggle", value=False)

# Main dashboard
st.title("Dashboard")

# Dummy data
data = {
    "last_reading_time": "14:55:45",
    "site_status": "Active",
    "voltages": [230, 232, 231, 229],
    "door_status": "Closed",
    "fuel_level": 75,
    "gauge_value": 500,
    "temperature": 28,
    "humidity": 48,
    "soil": 66,
}

# Columns for layout
col1, col2, col3 = st.columns(3)

# Display the data
with col1:
    st.metric("Last Reading Time", data["last_reading_time"])
    st.metric("Site Status", data["site_status"], delta="Active", delta_color="inverse")
    st.metric("Temperature", f"{data['temperature']} °C")
    st.metric("Humidity", f"{data['humidity']} %")

with col2:
    st.metric("Main Voltage 3", f"{data['voltages'][2]} V")
    st.metric("Main Voltage 4", f"{data['voltages'][3]} V")
    st.metric("Door Status", data["door_status"], delta="Closed", delta_color="inverse")
    st.metric("Generator Fuel Level", f"{data['fuel_level']} %")

# Create more engaging Gauge
fig_gauge = go.Figure(go.Indicator(
    mode="gauge+number+delta",
    value=data["gauge_value"],
    title={"text": "Gauge"},
    delta={'reference': 512, 'increasing': {'color': "green"}},
    gauge={
        'axis': {'range': [0, 1023]},
        'bar': {'color': "darkblue"},
        'steps': [
            {'range': [0, 512], 'color': "lightgray"},
            {'range': [512, 1023], 'color': "gray"}],
        'threshold': {
            'line': {'color': "red", 'width': 4},
            'thickness': 0.75,
            'value': 900}}))

with col3:
    st.plotly_chart(fig_gauge, use_container_width=True)

# Create charts for temperature and humidity
time_series = pd.date_range(start="2022-01-01", periods=60, freq="min")
temp_data = np.random.normal(loc=25, scale=5, size=len(time_series))
humidity_data = np.random.normal(loc=50, scale=10, size=len(time_series))

fig_temp = go.Figure()
fig_temp.add_trace(go.Scatter(x=time_series, y=temp_data, mode="lines", name="Temperature", line=dict(color='firebrick', width=2)))
fig_temp.update_layout(title="Temperature Over Time", xaxis_title="Time", yaxis_title="Temperature (°C)", template="plotly_dark")

fig_humidity = go.Figure()
fig_humidity.add_trace(go.Scatter(x=time_series, y=humidity_data, mode="lines", name="Humidity", line=dict(color='royalblue', width=2)))
fig_humidity.update_layout(title="Humidity Over Time", xaxis_title="Time", yaxis_title="Humidity (%)", template="plotly_dark")

col4, col5 = st.columns(2)
with col4:
    st.plotly_chart(fig_temp, use_container_width=True)

with col5:
    st.plotly_chart(fig_humidity, use_container_width=True)

# Create bar chart for voltages
fig_bar = px.bar(x=["Voltage 1", "Voltage 2", "Voltage 3", "Voltage 4"], y=data['voltages'],
                 labels={'x': 'Voltage Type', 'y': 'Voltage (V)'}, title="Voltage Levels")
fig_bar.update_traces(marker_color='indianred')

# Create pie chart for site status
fig_pie = px.pie(values=[1], names=['Active'], title="Site Status")
fig_pie.update_traces(marker=dict(colors=['royalblue']))

# Create area chart for fuel level over time
fuel_time = pd.date_range(start="2022-01-01", periods=60, freq="min")
fuel_level_data = np.random.uniform(70, 80, size=len(fuel_time))

fig_area = go.Figure()
fig_area.add_trace(go.Scatter(x=fuel_time, y=fuel_level_data, fill='tozeroy', mode='none', name='Fuel Level', fillcolor='green'))
fig_area.update_layout(title="Fuel Level Over Time", xaxis_title="Time", yaxis_title="Fuel Level (%)", template="plotly_dark")

col6, col7, col8 = st.columns(3)

with col6:
    st.plotly_chart(fig_pie, use_container_width=True)

with col7:
    st.plotly_chart(fig_bar, use_container_width=True)

with col8:
    st.plotly_chart(fig_area, use_container_width=True)

# Display pump and generator switch status
st.markdown("### Device Status")
col9, col10 = st.columns(2)
with col9:
    pump_status = "ON" if pump_toggle else "OFF"
    st.metric("Pump Switch", pump_status)

with col10:
    generator_status = "ON" if generator_toggle else "OFF"
    st.metric("Generator Switch", generator_status)

# Update data periodically and show it
while True:
    data_df = update_data()
    st.write(data_df.head())  # This line can be removed if you don't want to display the raw data
    time.sleep(60)  # Wait for 60 seconds before updating again

# Add footer with some styling
st.markdown("""
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #333;
        color: white;
        text-align: center;
        padding: 10px 0;
    }
    </style>
    <div class="footer">
        <p>Dashboard by Your Name</p>
    </div>
""", unsafe_allow_html=True)
