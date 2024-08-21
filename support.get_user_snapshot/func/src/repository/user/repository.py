from etria_logger import Gladsheim
from typing import Optional
from decouple import config

from ...infrastructure.mongo.infrastructure import MongoInfrastructure


class UserRepository:
    mongo_infra = MongoInfrastructure

    @classmethod
    def _get_collection(cls):
        mongo_client = cls.mongo_infra.get_connection()
        user_mongodb_database = mongo_client[config("USER_MONGODB_DATABASE")]
        user_mongodb_collection = user_mongodb_database[config("USER_MONGODB_COLLECTION")]
        return user_mongodb_collection

    @classmethod
    async def find_user_by_unique_id(cls, unique_id: str, projection=None) -> dict:
        collection = cls._get_collection()
        try:
            user = await collection.find_one({"unique_id": unique_id}, projection=projection)
            return user
        except Exception as ex:
            Gladsheim.error(
                error=ex,
                message=f"Repository::find_user_by_unique_id::No record found with this unique_id::{unique_id}")
            raise ex
