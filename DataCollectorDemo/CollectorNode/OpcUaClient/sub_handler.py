from typing import Callable, Any

from asyncua import Node, ua
from asyncua.common.subscription import DataChangeNotif
from datetime import datetime


class SubHandler:
    def __init__(self):
        self.__subscribers: list[Callable[[Any], None]] = []

    def __on_data_received(self, data: Any):
        for sub in self.__subscribers:
            sub(data)

    def subscribe(self, callback: Callable[[Any], None]):
        """
        Subscribe to the data received event message.
        :param callback: Callback for the data.
        :return: None
        """
        self.__subscribers.append(callback)

    def unsubscribe(self, callback: Callable[[Any], None]):
        if callback in self.__subscribers:
            self.__subscribers.remove(callback)

    def datachange_notification(self, node: Node, val, data: DataChangeNotif):
        print("DEBUG")
        source_timestamp: datetime = data.monitored_item.Value.SourceTimestamp
        server_timestamp: datetime = data.monitored_item.Value.ServerTimestamp
        self.__on_data_received({"val": val, "source_timestamp": source_timestamp, "server_timestamp": server_timestamp})

    def event_notification(self, status: ua.EventNotificationList):
        pass

    def status_changed_notification(self, status: ua.StatusChangeNotification):
        pass