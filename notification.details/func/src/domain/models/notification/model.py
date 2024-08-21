# Jormungandr - Notifications
from ...exceptions.domain.exception import InconsistentNotification


# Standards
from typing import List
from datetime import datetime


class Notification:
    def __init__(self, notification: dict, datetime_now: datetime):
        self.title = notification.get("title")
        self.description = notification.get("description")
        self.details = notification.get("details")
        self.sent_at = notification.get("sent_at")
        self.seen = notification.get("seen")
        self.unique_id = notification.get("unique_id")
        self.seen_at = notification.get("seen_at")
        self.listed = True
        self.listed_at = datetime_now
        self.notification_id = notification.get("notification_id")
        self.validate_notifications = self.check_if_no_empty_fields()

    def check_if_no_empty_fields(self):
        if not all(
            [
                self.title,
                self.description,
                self.unique_id,
                self.notification_id,
                self.sent_at,
            ]
        ):
            raise InconsistentNotification()


class NotificationsModel:
    def __init__(self, notifications: List):
        self.datetime_now = datetime.utcnow()
        self.notifications = [
            Notification(notification=notification, datetime_now=self.datetime_now)
            for notification in notifications
        ]

    def get_notifications_template(self) -> List[dict]:

        notifications_template = [
            {
                "title": notification.title,
                "description": notification.description,
                "details": notification.details,
                "sent_at": notification.sent_at,
                "seen": notification.seen,
                "seen_at": notification.seen_at,
                "listed": notification.listed,
                "listed_at": notification.listed_at,
                "notification_id": notification.notification_id,
            }
            for notification in self.notifications
        ]
        return notifications_template
