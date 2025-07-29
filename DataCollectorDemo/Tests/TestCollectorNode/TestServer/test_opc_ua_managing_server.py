from CollectorNode.OpcUaClient import OpcUaManagingServer, OpcUaConfig
from Common.Communication import CommandModel, ResponseModel, MessageCategory

def test_get_outline():
    sut = OpcUaManagingServer()
    outline = sut.get_outline()
    assert len(outline.name) > 0
    assert outline.port > 1000
    assert outline.sensor_data_receiver == False
    assert outline.sensor_data_sender == True
    
