from abc import ABC, abstractmethod
from typing import Callable
from datetime import datetime



class SensorBase[T](ABC):
    __namespace: str
    __name: str
    __updates_per_second: float
    __normal_set_value: T
    __normal_variation: T

    def __init__(self, name: str, namespace: str, normal_set_value: T, normal_variation: T):
        self.__name = name
        self.__namespace = namespace
        self.__normal_set_value = normal_set_value
        self.__normal_variation = normal_variation

    @property
    def namespace(self) -> str:
        return self.__namespace

    @property
    def name(self) -> str:
        return self.__name

    @property
    def updates_per_second(self):
        return self.__updates_per_second

    @property
    def normal_set_value(self) -> T:
        return self.__normal_set_value

    @property
    def normal_variation(self) -> T:
        return self.__normal_variation

    @abstractmethod
    def to_json(self):
        pass