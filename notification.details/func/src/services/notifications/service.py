# Jormungandr - Notification
from ...domain.exceptions.services.exception import NotificationNotFound
from ...domain.validators.notification.validator import NotificationValidator
from ...domain.exceptions.repositories.exception import ErrorOnUpdateUserNotifications
from ...repositories.mongo_db.notification.repository import NotificationRepository


# Standards
from typing import Union


class NotificationService:
    @classmethod
    async def get_details(
        cls, notification: NotificationValidator
    ) -> Union[dict, None]:
        notification_details = await NotificationRepository.get_details(
            notification=notification
        )

        if not notification_details:
            raise NotificationNotFound
        await cls.update_notification_to_viewed(notification=notification)
        return {"notification": notification_details}

    @staticmethod
    async def update_notification_to_viewed(
        notification: NotificationValidator,
    ) -> bool:
        result = await NotificationRepository.update_seen_and_seen_at(
            notification=notification
        )
        if not result.matched_count:
            raise ErrorOnUpdateUserNotifications()
        return True
