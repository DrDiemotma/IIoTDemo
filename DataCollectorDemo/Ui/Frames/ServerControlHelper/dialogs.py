import streamlit as st
import pandas as pd
from Ui.Communication import OpcUaServer

@st.dialog("Create new temperature sensor")
def create_temperature_sensor(url: str, timeout: float) -> None:
    """
    Create a dialog for a temperature sensor.
    :param url: URL of the server call, including port.
    :param timeout: timeout for the request.
    :return: None.
    """
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
        OpcUaServer.add_sensor(url, payload, timeout)
        st.rerun()


@st.dialog("Create new pressure sensor")
def create_pressure_sensor(url: str, timeout: float) -> None:
    """

    :param url:
    :param timeout:
    :return:
    """
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
        OpcUaServer.add_sensor(url, payload, timeout)
        st.rerun()


@st.dialog("Delete sensor")
def delete_sensor(url: str, timeout: float, sensors: list) -> None:
    if not any(sensors):
        st.rerun()

    df = pd.DataFrame(sensors)
    selected = st.data_editor(df, num_rows="dynamic", width='stretch')

    if st.button("Confirm"):
        if not selected.empty:
            sensor_type = selected['type'][0]
            sensor_identifier = selected['identifier'][0]
            payload = {"type": str(sensor_type), "identifier": int(sensor_identifier)}
            OpcUaServer.delete_sensor(url, payload, timeout)
        st.rerun()
