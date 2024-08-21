# Jormungandr - Notifications
from ..base_repository.base import MongoDbBaseRepository

# Standards
from datetime import datetime
from typing import List

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
    async def get_all_user_notifications(cls, unique_id: str) -> List:
        collection = await cls._get_collection()
        try:
            cursor = collection.find({"unique_id": unique_id})
            notifications = [
                notification
                for notification in await cursor.to_list(
                    length=int(config("QUANTITY_OF_NOTIFICATIONS"))
                )
            ]
            return notifications
        except Exception as ex:
            Gladsheim.error(error=ex)
            raise ex

    @classmethod
    async def update_all_to_listed(
        cls, datetime_now: datetime, unique_id: str
    ) -> UpdateResult:
        collection = await cls._get_collection()
        try:
            result = await collection.update_many(
                {"unique_id": unique_id},
                {"$set": {"listed": True, "listed_at": datetime_now}},
            )
            return result
        except Exception as ex:
            Gladsheim.error(error=ex)
            raise ex
