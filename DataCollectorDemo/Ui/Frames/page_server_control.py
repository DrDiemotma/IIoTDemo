import streamlit as st
from Ui.Communication import OpcUaServer
from Ui.Frames.ServerControlHelper import create_temperature_sensor, create_pressure_sensor, delete_sensor

base_url: str = "http://localhost:8765"
v01_url = f"{base_url}/v0.1"
timeout: float = 1.0


## page layout

st.title("Server configuration")
placeholder = st.empty()

is_online = OpcUaServer.is_server_online(base_url, timeout)
if is_online:
    placeholder.success("Server is running")
else:
    placeholder.error("Server is offline")

sensors = OpcUaServer.get_sensors(v01_url, timeout)
st.dataframe(sensors['sensors'], height=300)

## add sensors
sensor_column, pressure_column, delete_column = st.columns(3)

if is_online and sensor_column.button("Add Temperature Sensor"):
    create_temperature_sensor(v01_url, timeout)

if is_online and pressure_column.button("Add Pressure Sensor"):
    create_pressure_sensor(v01_url, timeout)

if is_online and delete_column.button("❌ Delete Sensor"):
    delete_sensor(v01_url, timeout, sensors['sensors'])