# Jormungandr - Notifications
from ..base_repository.base import MongoDbBaseRepository


# Third party
from decouple import config
from etria_logger import Gladsheim


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
    async def count_unlisted_notifications(cls, unique_id: str) -> int:
        collection = await cls._get_collection()
        try:
            result = await collection.count_documents(
                {"unique_id": unique_id, "listed": False}
            )
            return result
        except Exception as ex:
            Gladsheim.error(error=ex)
            raise ex
