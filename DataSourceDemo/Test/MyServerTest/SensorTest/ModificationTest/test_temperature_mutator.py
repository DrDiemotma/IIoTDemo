import asyncio

import pytest
from datetime import datetime

from MyServer.Sensor.Modification.TemperatureMutator import TemperatureMutator
from MyServer.Sensor import TemperatureSensor
from MyServer.MachineOperation import State, Mode

class TestSensorConsumer:
    temperature: float
    time_stamp: datetime
    def callback(self, time_stamp: datetime, value: float):
        self.time_stamp = time_stamp
        self.temperature = value


def test_measure():
    sensor: TemperatureSensor = TemperatureSensor(1)
    sut: TemperatureMutator = TemperatureMutator(sensor, start_value=20.0)
    value: float = sut.measure()
    assert 15.0 < value < 25.0  # should be around 20 degrees plus some noise.

@pytest.mark.asyncio
async def test_updates():
    sensor: TemperatureSensor = TemperatureSensor(1, updates_per_second=100)
    consumer = TestSensorConsumer()
    sensor.add_callback(consumer.callback)
    sut: TemperatureMutator = TemperatureMutator(sensor, start_value=20.0, value_running=200)
    sensor.start()
    await asyncio.sleep(2.0 / sensor.updates_per_second)  # make sure data is written
    start_temperature = consumer.temperature
    start_time = consumer.time_stamp
    assert start_temperature > 0
    assert start_time is not None
    sut.mode = Mode.RUNNING
    await asyncio.sleep(10.0 / sensor.updates_per_second)  # make sure value has time to increase
    sensor.stop()
    end_temperature = consumer.temperature
    end_time = consumer.time_stamp

    assert end_temperature > start_temperature
    assert end_time > start_time

@pytest.mark.asyncio
async def test_adaption():
    sensor: TemperatureSensor = TemperatureSensor(1, updates_per_second=100)
    consumer = TestSensorConsumer()
    sensor.add_callback(consumer.callback)
    # don't increase the st_dev value, this is here to have a very deterministic behaviour of temperature
    sut: TemperatureMutator = TemperatureMutator(sensor, start_value=20.0, value_running=200, st_dev=10e-8)
    sensor.start()
    await asyncio.sleep(2.0 / sensor.updates_per_second) # make sure data is written
    raw_data = [consumer.temperature] * 10
    sut.mode = Mode.RUNNING
    for i in range(1, 10):
        await asyncio.sleep(1.0 / sensor.updates_per_second)
        raw_data[i] = consumer.temperature
    sensor.stop()  # we don't need to have it running for the rest of the test, just see that the data increases
    for i in range(1, 10):
        assert raw_data[i] > raw_data[i - 1]





