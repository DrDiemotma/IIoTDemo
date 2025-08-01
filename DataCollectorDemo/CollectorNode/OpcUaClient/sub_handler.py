from asyncua import Node, ua
from asyncua.common.subscription import DataChangeNotif


class SubHandler:
    async def datachange_notification(self, node: Node, val, data: DataChangeNotif):
        source_timestamp: ua.datetime.timestamp = data.monitored_item.Value.SourceTimestamp
        server_timestamp: ua.datetime.timestamp = data.monitored_item.Value.ServerTimestamp

    async def event_notification(self, status: ua.EventNotificationList):
        pass

    async def status_changed_notification(self, status: ua.StatusChangeNotification):
        pass