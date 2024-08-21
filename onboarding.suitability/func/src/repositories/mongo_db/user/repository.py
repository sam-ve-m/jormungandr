# Jormungandr - Onboarding
from ..base_repository.base import MongoDbBaseRepository

# Third party
from decouple import config
from etria_logger import Gladsheim
from pymongo.results import UpdateResult


class UserRepository(MongoDbBaseRepository):
    @classmethod
    async def _get_collection(cls):
        mongo_client = cls.infra.get_client()
        try:
            database = mongo_client[config("MONGODB_DATABASE_NAME")]
            collection = database[config("MONGODB_USER_COLLECTION")]
            return collection
        except Exception as ex:
            Gladsheim.error(
                error=ex, message="Error when trying to get mongo collection"
            )
            raise ex

    @classmethod
    async def update_customer_suitability_data(
        cls, unique_id: str, suitability
    ) -> UpdateResult:
        collection = await cls._get_collection()
        try:
            user_updated = await collection.update_one(
                {"unique_id": unique_id}, {"$set": suitability}
            )
            return user_updated
        except Exception as ex:
            message = f"UserRepository::update_one_with_suitability_data::error on update user with this {unique_id=}"
            Gladsheim.error(error=ex, message=message)
            raise ex
