# STANDARD IMPORTS
from decouple import config

# PROJECT IMPORTS
from func.src.domain.exceptions.exceptions import UserWasNotFound
from func.src.infrastructure.mongo_db.infrastructure import MongoDBInfrastructure

# THIRD PART IMPORTS
from etria_logger import Gladsheim


class UserRepository:
    infra = MongoDBInfrastructure
    database = config("MONGODB_DATABASE_NAME")
    collection = config("MONGODB_USER_COLLECTION")

    @classmethod
    async def __get_collection(cls):
        mongo_client = cls.infra.get_client()
        try:
            database = mongo_client[cls.database]
            collection = database[cls.collection]
            return collection
        except Exception as ex:
            message = (
                f"UserRepository::__get_collection::Error when trying to get collection"
            )
            Gladsheim.error(
                error=ex,
                message=message,
                database=cls.database,
                collection=cls.collection,
            )
            raise ex

    @classmethod
    async def update_user_and_time_experience(
        cls, unique_id: str, time_experience_request: str
    ):
        user_filter = {"unique_id": unique_id}
        time_experience = {
            "$set": {
                "external_exchange_requirements.us.time_experience": time_experience_request
            }
        }
        try:
            collection = await cls.__get_collection()
            was_updated = await collection.update_one(user_filter, time_experience)

            if not was_updated.matched_count == 1:
                raise UserWasNotFound()
            return bool(was_updated)

        except Exception as error:
            Gladsheim.error(error=error)
            return False
