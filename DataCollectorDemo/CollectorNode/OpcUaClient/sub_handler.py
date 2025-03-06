from asyncua import Node, ua


class SubHandler:
    def datachange_notification(self, node: Node, val, data):
        pass

    def event_notification(self, status: ua.EventNotificationList):
        pass

    def status_changed_notification(self, status: ua.StatusChangeNotification):
        pass