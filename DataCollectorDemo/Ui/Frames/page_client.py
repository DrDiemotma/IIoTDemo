import os.path

import streamlit as st

from CollectorNode.CentralConfig import Config
from CollectorNode.CentralConfig import Namespaces
from CollectorNode.CentralConfig import ExchangeEntry

config: Config = Config()
selected_client: str = config.get_entry(Namespaces.Client, ExchangeEntry.SelectedConfigFile)
config_directory: str = config.get_entry(Namespaces.FileConfigs, ExchangeEntry.GlobalClientConfigDirectory)

files = [os.path.splitext(x)[0] for x in os.listdir(config_directory) if x.endswith(".json")]

st.title("Client")

selected_file = st.selectbox("Select file", files)



if st.button("Load"):
    pass
