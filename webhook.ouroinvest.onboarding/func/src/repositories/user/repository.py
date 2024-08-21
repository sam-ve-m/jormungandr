from decouple import config
from etria_logger import Gladsheim

from src.domain.validator.webhook.validator import WebHookMessage
from src.infrastructure.mongo_db.infrastructure import MongoDBInfrastructure


class UserRepository:
    infra = MongoDBInfrastructure

    @classmethod
    async def __get_collection(cls):
        mongo_client = cls.infra.get_client()
        try:
            database = mongo_client[config("MONGODB_DATABASE_NAME")]
            collection = database[config("MONGODB_USER_COLLECTION")]
            return collection
        except Exception as ex:
            message = (
                f"UserRepository::__get_collection::Error when trying to get collection"
            )
            Gladsheim.error(
                error=ex,
                message=message,
                database=config("MONGODB_DATABASE_NAME"),
                collection=config("MONGODB_USER_COLLECTION"),
            )
            raise ex

    @classmethod
    async def find_client_unique_id(cls, cpf: str) -> str:
        user_filter = {"identifier_document.cpf": cpf}
        collection = await cls.__get_collection()
        user = await collection.find_one(user_filter) or {}
        unique_id = user.get("unique_id")
        return unique_id

    @classmethod
    async def update_exchange_account_status(cls, webhook_message: WebHookMessage) -> bool:
        user_filter = {"identifier_document.cpf": webhook_message.cpf}
        webhook_message_information = {
            "$set": {"ouro_invest.status": webhook_message.status.value}
        }

        collection = await cls.__get_collection()
        was_updated = await collection.update_one(
            user_filter, webhook_message_information
        )
        return was_updated.matched_count == 1
