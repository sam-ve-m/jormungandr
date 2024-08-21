from decouple import config
from etria_logger import Gladsheim

from func.src.domain.exceptions.model import UserDataNotFound
from func.src.infrastructures.mongo_db.infrastructure import MongoDBInfrastructure


class UserRepository:
    infra = MongoDBInfrastructure
    database = config("MONGODB_DATABASE_NAME")
    collection = config("MONGODB_USER_COLLECTION")

    @classmethod
    async def __get_collection(cls):
        try:
            mongo_client = cls.infra.get_client()
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
    async def find_user(cls, query: dict) -> dict:
        try:
            collection = await cls.__get_collection()
            user_document = await collection.find_one(query)
            if user_document is None:
                user_document = {}
                Gladsheim.error(
                    error=UserDataNotFound("common.register_not_exists"),
                    message="User not found",
                    query=query,
                )
            return user_document

        except Exception as ex:
            Gladsheim.error(error=ex, query=query)
            raise ex
