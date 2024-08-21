# Jormungandr - Notification
from ...repositories.mongo_db.notification.repository import NotificationRepository


class NotificationCountService:
    @classmethod
    async def get_number_of_unlisted(cls, unique_id: str) -> dict:
        number_of_not_listed = (
            await NotificationRepository.count_unlisted_notifications(
                unique_id=unique_id
            )
        )
        return {"notifications_unlisted": number_of_not_listed}
