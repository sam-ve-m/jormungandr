from decouple import config

from func.src.domain.exceptions.exceptions import TransactionNotFound, CpfNotFound, TransactionWasNotUpdated
from func.src.domain.validator.webhook.validator import WebHookMessage
from func.src.infrastructure.mongo_db.infrastructure import MongoDBInfrastructure


class BureauTransactionRepository(MongoDBInfrastructure):
    collection = None

    @classmethod
    def _get_collection(cls):
        if cls.collection is None:
            database = config("MONGO_DATABASE_LIONX")
            collection = config("MONGO_COLLECTION_BUREAU")
            cls.collection = cls._instance_collection(database, collection)
        return cls.collection

    @classmethod
    async def get_user_cpf_of_transaction(cls, bureau_validation: WebHookMessage) -> str:
        user_filter = {
            "transaction_id": bureau_validation.uuid
        }
        collection = cls._get_collection()
        transaction = await collection.find_one(user_filter)
        if not transaction:
            raise TransactionNotFound()
        if not (cpf := transaction.get("cpf")):
            raise CpfNotFound()
        return cpf

    @classmethod
    async def update_bureau_transaction(cls, bureau_validation: WebHookMessage) -> bool:
        user_filter = {
            "transaction_id": bureau_validation.uuid
        }
        bureau_transaction_information = {
            "$set": {
                "status": bureau_validation.status.value,
                "last_update_date": bureau_validation.date,
                "event_type": bureau_validation.event_type.value,
                "status_reasons": bureau_validation.status_reasons,
            }
        }

        collection = cls._get_collection()
        was_updated = await collection.update_one(
            user_filter, bureau_transaction_information
        )
        transaction_was_updated = was_updated.matched_count == 1
        if transaction_was_updated is False:
            raise TransactionWasNotUpdated
        return True
