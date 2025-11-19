import streamlit as st
from Ui.Communication import OpcUaServer

base_url: str = "http://localhost:8765"
v01_url = f"{base_url}/v0.1"
timeout: float = 1.0


@st.dialog("Create new temperature sensor")
def create_temperature_sensor():
    identifier = st.number_input("Identifier", min_value=1, step=1, value=1)
    start_value = st.number_input("Start Value", value=23.0, step=0.1)
    value_idle = st.number_input("Value Idle", value=23.0, step=0.1)
    value_running = st.number_input("Value Running", value=85.0, step=0.1)
    value_running_broken = st.number_input("Value Running (broken)", value=105.5, step=0.1)
    st_dev = st.number_input("Standard Deviation", min_value=0.001, step=0.001, value=0.5)
    adaption_rate = st.number_input("Adaption Rate", min_value=0.001, max_value=0.999, step=0.001, value=0.05)
    random_seed = st.number_input("Random Seed", min_value=0, step=1, value=42)

    if st.button("Submit"):
        payload = {
            "type": "Temperature",
            "identifier": int(identifier),
            "simulator_config": {
                "start_value": start_value,
                "value_idle": value_idle,
                "value_running": value_running,
                "value_running_broken": value_running_broken,
                "random_seed": int(random_seed),
                "adaption_rate": adaption_rate,
                "st_dev": st_dev
            }
        }
        OpcUaServer.add_sensor(v01_url, payload, timeout)
        st.rerun()


@st.dialog("Create new pressure sensor")
def create_pressure_sensor():
    identifier = st.number_input("Identifier", min_value=1, step=1, value=1)
    start_value = st.number_input("Start Value",min_value=0.0, value=1013.0, step=0.1)
    value_idle = st.number_input("Value Idle", min_value=0.0, value=1013.0, step=0.1)
    value_running = st.number_input("Value Running", min_value=0.0, value=1220.0, step=0.1)
    value_running_broken = st.number_input("Value Running (broken)", min_value=0.0, value=1120.5, step=0.1)
    st_dev = st.number_input("Standard Deviation", min_value=0.001, step=0.001, value=4.5)
    st_dev_broken = st.number_input("Standard Deviation (broken)", min_value=0.001, step=0.001, value=8.5)
    adaption_rate = st.number_input("Adaption Rate", min_value=0.001, max_value=0.999, step=0.001, value=0.05)
    random_seed = st.number_input("Random Seed", min_value=0, step=1, value=42)
    if st.button("Submit"):
        payload = {
            "type": "Pressure",
            "identifier": identifier,
            "simulator_config": {
                "start_value": start_value,
                "random_seed": random_seed,
                "st_dev": st_dev,
                "st_dev_broken": st_dev_broken,
                "value_idle": value_idle,
                "value_running": value_running,
                "value_running_broken": value_running_broken,
                "adaption_rate": adaption_rate
            }
        }
        OpcUaServer.add_sensor(v01_url, payload, timeout)
        st.rerun()


## page layout

st.title("Server configuration")
placeholder = st.empty()

main_col, button_col = st.columns([5, 1])
is_online = OpcUaServer.is_server_online(base_url, timeout)
if is_online:
    placeholder.success("Server is running")
else:
    placeholder.error("Server is offline")

## MAIN COLUMN

sensors = OpcUaServer.get_sensors(v01_url, timeout)
main_col.dataframe(sensors, height=300)

## BUTTON COLUMN

if is_online and button_col.button("Add temperature sensor"):
    create_temperature_sensor()

if is_online and button_col.button("Add pressure sensor"):
    create_pressure_sensor()
