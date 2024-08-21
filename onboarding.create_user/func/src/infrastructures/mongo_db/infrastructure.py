# Third party
from decouple import config
from etria_logger import Gladsheim
from motor import motor_asyncio


class MongoDBInfrastructure:

    client = None

    @classmethod
    def get_client(cls):
        if cls.client is None:
            try:
                url = config("MONGO_CONNECTION_URL")
                cls.client = motor_asyncio.AsyncIOMotorClient(url)
            except Exception as ex:
                Gladsheim.error(error=ex)
                raise ex
        return cls.client
