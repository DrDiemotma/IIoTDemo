import json
import os.path

from CollectorNode.OpcUaClient import OpcUaClient, OpcUaClientFactory, OpcUaConfig

test_config: OpcUaConfig = OpcUaConfig(
    ip="127.0.0.1",
    server_id="TestServer",
    uri="test_server",
    port=4840
)

def test_opc_ua_client_factory_new_from_config():
    client: OpcUaClient | None = OpcUaClientFactory.new(test_config)
    assert client is not None

def test_opc_ua_client_factory_new_from_file():
    file_name = "test.json"

    def clean_up():
        if os.path.isfile(file_name):
            try:
                os.remove(file_name)
            except OSError as ose:
                print(f"Could not delete file: {ose}")

    clean_up()

    with open(file_name, "w") as f:
        try:
            json.dump(test_config.__dict__, f)
        except OSError as ose:
            print(f"Could not write config: {ose}.")

    client: OpcUaClient | None = OpcUaClientFactory.new(file_name)
    clean_up()

    assert client is not None


