from decouple import config
from etria_logger import Gladsheim
from motor import motor_asyncio
from motor.motor_asyncio import AsyncIOMotorCollection

from func.src.domain.exceptions.exceptions import InitializeError


class MongoDBInfrastructure:

    client = None

    @classmethod
    def _get_client(cls):
        if cls.client is None:
            url = config("MONGO_CONNECTION_URL")
            cls.client = motor_asyncio.AsyncIOMotorClient(url)
        return cls.client

    @classmethod
    def _instance_collection(
        cls, database: str, collection: str
    ) -> AsyncIOMotorCollection:
        try:
            connection = cls._get_client()
            database = connection[database]
            collection = database[collection]
            return collection
        except Exception as e:
            Gladsheim.error(
                message=f"{cls.__name__}::get_collection",
                error=e,
                database=database,
                collection=collection,
            )
            raise InitializeError
