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
if is_online:
    st.dataframe(sensors['sensors'], height=300)

## add sensors
sensor_column, pressure_column, delete_column = st.columns(3)

if sensor_column.button("Add Temperature Sensor", disabled=not is_online):
    create_temperature_sensor(v01_url, timeout)

if pressure_column.button("Add Pressure Sensor", disabled=not is_online):
    create_pressure_sensor(v01_url, timeout)

if delete_column.button("❌ Delete Sensor", disabled=not is_online):
    delete_sensor(v01_url, timeout, sensors['sensors'])

st.divider()

## Machine Controls

number_of_sensors: int = 0 if "sensors" not in sensors else len(sensors['sensors'])
is_running: bool = OpcUaServer.is_server_running(v01_url, timeout)
is_initialized: bool =  OpcUaServer.is_initialized(v01_url, timeout)

if st.button("Initialize Machine", disabled=is_initialized or number_of_sensors == 0):
    OpcUaServer.initialize(v01_url, timeout)
    st.rerun()

start_column, stop_column = st.columns(2)
if start_column.button("Start Machine", disabled=not is_online
                                                 or number_of_sensors == 0
                                                 or is_running
                                                 or not is_initialized):
    OpcUaServer.start_server(v01_url, timeout)
    st.rerun()

if stop_column.button("Stop Machine", disabled=not is_online
                                               or number_of_sensors == 0
                                               or not is_running
                                               or not is_initialized):
    OpcUaServer.stop_server(v01_url, timeout)
    st.rerun()

