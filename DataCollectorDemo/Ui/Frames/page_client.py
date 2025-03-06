import os.path

import streamlit as st
import requests

from CollectorNode.OpcUaClient import ClientManager
from CollectorNode.CentralConfig import Config
from CollectorNode.CentralConfig import Namespaces
from CollectorNode.CentralConfig import ExchangeEntry

config: Config = Config()
selected_client: str = config.get_entry(Namespaces.Client, ExchangeEntry.SelectedConfigFile)
config_directory: str = config.get_entry(Namespaces.FileConfigs, ExchangeEntry.GlobalClientConfigDirectory)

files = [os.path.splitext(x)[0] for x in os.listdir(config_directory) if x.endswith(".json")]

st.title("Client")

selected_file = st.selectbox("Select file", files)

def send_command(cmd: str, *args):
    payload = {"action": cmd, "parameters": list(args)}
    response = requests.post("http://127.0.0.1:8000/ControlServer", json=payload)
    return response.json()

if st.button("Load"):
    pass
