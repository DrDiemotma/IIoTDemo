import os.path

from CollectorNode.OpcUaClient import load_config, save_config, OpcUaConfig, NodeConfig

test_config: OpcUaConfig = OpcUaConfig(
    ip="127.0.0.1",
    server_id="TestServer",
    uri="test_server",
    port=4840,
    subscriptions=[
        NodeConfig(namespace="http://test.org",
                   object_name="TestObject",
                   value_name="TestVariable")
    ]
)

def list_deviations(c1: OpcUaConfig, c2: OpcUaConfig) -> list[tuple[str, str | int, str | int]]:
    deviations = []

    if c1.ip != c2.ip:
        deviations.append(("ip", c1.ip, c2.ip))

    if c1.server_id != c2.server_id:
        deviations.append(("server_id", c1.server_id, c2.server_id))

    if c1.uri != c2.uri:
        deviations.append(("uri", c1.uri, c2.uri))

    if c1.port != c2.port:
        deviations.append(("port", c1.port, c2.port))

    if len(c1.subscriptions) != len(c2.subscriptions):
        deviations.append(("subscriptions_count", len(c1.subscriptions), len(c2.subscriptions)))

    for index, (s1, s2) in enumerate(zip(c1.subscriptions, c2.subscriptions)):
        if s1.namespace != s2.namespace:
            deviations.append((f"namespace {index}", s1.namespace, s2.namespace))

        if s1.object_name != s2.object_name:
            deviations.append((f"object_name {index}", s1.object_name, s2.object_name))

        if s1.value_name != s2.value_name:
            deviations.append((f"value_name {index}", s1.value_name, s2.value_name))

    return deviations


def test_list_deviations():
    assert len(list_deviations(test_config, test_config)) == 0
    my_config: OpcUaConfig = OpcUaConfig(
        ip="127.0.0.1",
        server_id="TestServer",
        uri="test_server",
        port=4840,
        subscriptions=[
            NodeConfig(namespace="http://test.org",
                       object_name="TestObject",
                       value_name="TestVariable")
        ]
    )
    assert len(list_deviations(my_config, test_config)) == 0

    my_false_config: OpcUaConfig = OpcUaConfig(
        ip="127.0.0.2",
        server_id="TestServer",
        uri="test_server",
        port=4840,
        subscriptions=[
            NodeConfig(namespace="http://test.org",
                       object_name="TestObject",
                       value_name="TestVariable")
        ]
    )

    assert len(list_deviations(my_false_config, test_config)) == 1

def test_save_config():
    test_file: str = "test_file.json"
    if os.path.isfile(test_file):
        try:
            os.remove(test_file)
        except:
            raise

    save_config(test_config, test_file)
    assert os.path.isfile(test_file)
    try:
        os.remove(test_file)
    except:
        raise

def test_load_config():
    test_file: str = "test_file.json"
    if os.path.isfile(test_file):
        try:
            os.remove(test_file)
        except:
            raise

    save_config(test_config, test_file)
    assert os.path.isfile(test_file)

    new_config: OpcUaConfig = load_config(test_file)
    assert len(list_deviations(test_config, new_config)) == 0
