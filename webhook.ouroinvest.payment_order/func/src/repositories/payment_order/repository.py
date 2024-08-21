from decouple import config
from etria_logger import Gladsheim

from src.infrastructure.mongo_db.infrastructure import MongoDBInfrastructure
from src.domain.validator.webhook.validator import WebHookMessage
from src.domain.exceptions.exceptions import ErrorOnSave


class PaymentOrderRepository:
    infra = MongoDBInfrastructure
    database = config("MONGODB_DATABASE_NAME")
    collection = config("MONGODB_PAYMENT_ORDER_COLLECTION")

    @classmethod
    async def __get_collection(cls):
        mongo_client = cls.infra.get_client()
        try:
            database = mongo_client[cls.database]
            collection = database[cls.collection]
            return collection
        except Exception as ex:
            message = (
                f"PaymentOrderRepository::_get_collection::Error when trying to get collection"
            )
            Gladsheim.error(
                error=ex,
                message=message,
                database=cls.database,
                collection=cls.collection,
            )
            raise ex

    @classmethod
    async def save_payment_order(cls,  webhook_message: WebHookMessage):
        try:
            collection = await cls.__get_collection()
            document_payload = webhook_message.dict()
            await collection.insert_one(document_payload)
        except Exception as error:
            Gladsheim.error(error=error)
            raise ErrorOnSave()
