from decouple import config

from func.src.domain.exceptions.exceptions import UserWasNotUpdated
from func.src.domain.validator.webhook.validator import WebHookMessage
from func.src.infrastructure.mongo_db.infrastructure import MongoDBInfrastructure


class UserRepository(MongoDBInfrastructure):
    collection = None

    @classmethod
    def _get_collection(cls):
        if cls.collection is None:
            database = config("MONGO_DATABASE_LIONX")
            collection = config("MONGODB_COLLECTION_USERS")
            cls.collection = cls._instance_collection(database, collection)
        return cls.collection

    @classmethod
    async def update_bureau_validation(cls, cpf: str, bureau_validation: WebHookMessage):
        user_filter = {"identifier_document.cpf": cpf}
        bureau_validation_information = {
            "$set": {
                "bureau_validations.cpf": bureau_validation.status.value,
            }
        }

        collection = cls._get_collection()
        was_updated = await collection.update_one(
            user_filter, bureau_validation_information
        )
        user_was_updated = was_updated.matched_count == 1
        if user_was_updated is False:
            raise UserWasNotUpdated()
        return True
