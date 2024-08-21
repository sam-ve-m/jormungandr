# Jormungandr - Notifications
from ....domain.validators.notification.validator import NotificationValidator
from ..base_repository.base import MongoDbBaseRepository

# Standards
from datetime import datetime

# Third party
from decouple import config
from etria_logger import Gladsheim
from pymongo.results import UpdateResult


class NotificationRepository(MongoDbBaseRepository):
    @classmethod
    async def _get_collection(cls):
        mongo_client = cls.infra.get_client()
        try:
            database = mongo_client[config("MONGODB_DATABASE_NAME")]
            collection = database[config("MONGODB_NOTIFICATION_COLLECTION")]
            return collection
        except Exception as ex:
            Gladsheim.error(
                error=ex, message="Error when trying to get mongodb collection"
            )
            raise ex

    @classmethod
    async def get_details(cls, notification: NotificationValidator) -> dict:
        collection = await cls._get_collection()
        try:
            notification_details = await collection.find_one(
                {"_id": notification.id}, {"unique_id": 0, "_id": 0}
            )
            return notification_details
        except Exception as ex:
            Gladsheim.error(error=ex)
            raise ex

    @classmethod
    async def update_seen_and_seen_at(
        cls, notification: NotificationValidator
    ) -> UpdateResult:
        collection = await cls._get_collection()
        try:
            datetime_now = datetime.utcnow()
            result = await collection.update_one(
                {"_id": notification.id},
                {"$set": {"seen": True, "seen_at": datetime_now}},
            )
            return result
        except Exception as ex:
            Gladsheim.error(error=ex)
            raise ex
