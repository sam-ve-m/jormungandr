from etria_logger import Gladsheim
from decouple import config
from motor.motor_asyncio import AsyncIOMotorClient


class MongoInfrastructure:
    client = None

    @classmethod
    def get_connection(cls):
        if cls.client is None:
            try:
                url = config("MONGO_CLIENT_URL")
                cls.client = AsyncIOMotorClient(url)
            except Exception as ex:
                Gladsheim.error(
                    error=ex,
                    message=f"{__class__}::get_connection::Error trying to get Mongo Client",
                )
                raise ex
        return cls.client

