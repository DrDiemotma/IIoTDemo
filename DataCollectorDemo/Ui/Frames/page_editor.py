import os

import streamlit as st
import json
from CollectorNode.OpcUaClient import OpcUaConfig
from CollectorNode.CentralConfig import configuration
from CollectorNode.CentralConfig import constants

config: configuration.Config = configuration.Config()

config_directory: str = config.get_entry(constants.Namespaces.FileConfigs, constants.ExchangeEntry.GlobalClientConfigDirectory)
IP_ADDRESS: str = "ip address"
PORT: str = "port"
SERVER_ID: str = "server id"
SERVER_URI: str = "server uri"
DEFAULT_SELECTED_FILE: str = "None"
DEFAULT_IP_ADDRESS: str = "0.0.0.0"
DEFAULT_PORT: int = 4840
DEFAULT_SERVER_ID: str = "None"
DEFAULT_SERVER_URI: str = "http://example.org/opcua"



_selected_file: str = config.get_entry(constants.Namespaces.FileConfigs, constants.ExchangeEntry.SelectedConfigFile,
                                       DEFAULT_SELECTED_FILE)
_ip_address: str = config.get_entry(constants.Namespaces.ConfigEdit, IP_ADDRESS, DEFAULT_IP_ADDRESS)
_port: int = config.get_entry(constants.Namespaces.ConfigEdit, PORT, DEFAULT_PORT)
_server_id: str = config.get_entry(constants.Namespaces.ConfigEdit, SERVER_ID, DEFAULT_SERVER_ID)
_uri: str = config.get_entry(constants.Namespaces.ConfigEdit, SERVER_URI,DEFAULT_SERVER_URI)

st.title("Configuration Editor")

def persist():
    global config
    selected_file = config.get_entry(constants.Namespaces.FileConfigs, constants.ExchangeEntry.SelectedConfigFile)
    ip_address = config.get_entry(constants.Namespaces.ConfigEdit, IP_ADDRESS)
    port = config.get_entry(constants.Namespaces.ConfigEdit, PORT)
    server_id = config.get_entry(constants.Namespaces.ConfigEdit, SERVER_ID)
    uri = config.get_entry(constants.Namespaces.ConfigEdit, SERVER_URI)

    config = OpcUaConfig(server_id=server_id, uri=uri, ip=ip_address, port=port)
    with open(os.path.join(config_directory, selected_file), "w") as f:
        json.dump(config.__dict__, f, indent=4)

def restore():
    global config

    with open(os.path.join(config_directory, _selected_file + ".json"), "r") as f:
        d = json.load(f)

    config.set_entry(constants.Namespaces.FileConfigs, constants.ExchangeEntry.SelectedConfigFile, _selected_file,
                     False)
    config.set_entry(constants.Namespaces.ConfigEdit, IP_ADDRESS, d["ip"], False)
    config.set_entry(constants.Namespaces.ConfigEdit, PORT, d["port"], False)
    config.set_entry(constants.Namespaces.ConfigEdit, SERVER_ID, d["server_id"], False)
    config.set_entry(constants.Namespaces.ConfigEdit, SERVER_URI, d["uri"], False)
    config.persist()


@st.dialog("Open configuration")
def select_file_form():
    global _selected_file
    if not os.path.isdir(config_directory):
        os.mkdir(config_directory)
    files = [os.path.splitext(x)[0] for x in os.listdir(config_directory) if x.endswith(".json")]
    if len(files) == 0:
        files = [""]

    _selected_file = files[0]
    _selected_file = st.selectbox("Select file", files)

    if st.button("Submit"):
        if os.path.isfile(os.path.join(config_directory, _selected_file + ".json")):
            restore()

        st.rerun()

@st.dialog("Edit OPC UA config")
def config_form():
    global config
    input_name = st.text_input("File name", config.get_entry(constants.Namespaces.FileConfigs,
                                                             constants.ExchangeEntry.SelectedConfigFile))
    ip_address = st.text_input("IP address", config.get_entry(constants.Namespaces.ConfigEdit, IP_ADDRESS))
    port = st.text_input("Port", str(config.get_entry(constants.Namespaces.ConfigEdit, PORT)))
    server_id = st.text_input("Server ID", config.get_entry(constants.Namespaces.ConfigEdit, SERVER_ID))
    uri = st.text_input("URI", config.get_entry(constants.Namespaces.ConfigEdit, SERVER_URI))

    if st.button("Submit"):
        if not input_name.endswith(".json"):
            input_name += ".json"
        config.set_entry(constants.Namespaces.FileConfigs, constants.ExchangeEntry.SelectedConfigFile, input_name,
                         False)
        config.set_entry(constants.Namespaces.ConfigEdit, IP_ADDRESS, ip_address, False)
        config.set_entry(constants.Namespaces.ConfigEdit, PORT, port, False)
        config.set_entry(constants.Namespaces.ConfigEdit, SERVER_ID, server_id, False)
        config.set_entry(constants.Namespaces.ConfigEdit, SERVER_URI, uri, False)
        config.persist()  # write the configuration - now it is on the hard drive
        persist()  # not the new configuration is written
        st.rerun()  # restart the script

@st.dialog("Delete configuration")
def delete_form():
    global config
    selected_file = config.get_entry(constants.Namespaces.FileConfigs, constants.ExchangeEntry.SelectedConfigFile)
    if not os.path.isdir(config_directory):
        os.mkdir(config_directory)
    files = [os.path.splitext(x)[0] for x in os.listdir(config_directory) if x.endswith(".json")]
    if len(files) == 0:
        files = [""]

    file_to_delete = st.selectbox("Select file", files)

    if st.button("Delete"):
        #  todo - confirmation message
        if file_to_delete == selected_file:
            config.set_entry(constants.Namespaces.FileConfigs, constants.ExchangeEntry.SelectedConfigFile, DEFAULT_SELECTED_FILE, False)
            config.set_entry(constants.Namespaces.ConfigEdit, IP_ADDRESS, DEFAULT_IP_ADDRESS, False)
            config.set_entry(constants.Namespaces.ConfigEdit, PORT, DEFAULT_PORT, False)
            config.set_entry(constants.Namespaces.ConfigEdit, SERVER_ID, DEFAULT_SERVER_ID, False)
            config.set_entry(constants.Namespaces.ConfigEdit, SERVER_URI, DEFAULT_SERVER_URI, False)
            config.persist()

        os.remove(os.path.join(config_directory, file_to_delete + ".json"))
        st.rerun()

col1, col2 = st.columns([1, 2])
with col1:
    st.text("Selected Configuration:")
    st.text("Set IP address:")
    st.text("Server ID:")
    st.text("Server URI:")


with col2:
    st.text(_selected_file)
    st.text(_ip_address + ":" + str(_port))
    st.text(_server_id)
    st.text(_uri)

col1, col2, col3 = st.columns(3)

with col1:
    if st.button("New Config"):
        config_form()

with col2:
    if st.button("Load config"):
        select_file_form()

with col3:
    if st.button("Delete config"):
        delete_form()

