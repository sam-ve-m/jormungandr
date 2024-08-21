# Jormungandr - Notifications
from ...repositories.mongo_db.notification.repository import NotificationRepository
from ...domain.models.notification.model import NotificationsModel
from ...domain.exceptions.repositories.exception import ErrorOnUpdateUserNotifications


class NotificationService:
    @classmethod
    async def get_all(cls, unique_id: str) -> dict:
        notifications = await NotificationRepository.get_all_user_notifications(
            unique_id=unique_id
        )

        if not notifications:
            return {"notifications": notifications}

        notifications_model = NotificationsModel(notifications=notifications)
        notifications_response = notifications_model.get_notifications_template()
        await cls.update_to_listed_all_notifications(
            unique_id=unique_id, notifications_model=notifications_model
        )
        return notifications_response

    @staticmethod
    async def update_to_listed_all_notifications(
        unique_id: str, notifications_model: NotificationsModel
    ) -> bool:

        result = await NotificationRepository.update_all_to_listed(
            unique_id=unique_id, datetime_now=notifications_model.datetime_now
        )
        if not result.matched_count:
            raise ErrorOnUpdateUserNotifications()
        return True
