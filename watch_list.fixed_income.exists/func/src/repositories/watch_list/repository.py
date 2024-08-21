from decouple import config
from etria_logger import Gladsheim

from func.src.domain.watch_list.model import WatchListProductModel
from func.src.infrastructures.mongo_db.infrastructure import MongoDBInfrastructure


class WatchListRepository:

    infra = MongoDBInfrastructure

    @classmethod
    async def __get_collection(cls):
        mongo_client = cls.infra.get_client()
        try:
            database = mongo_client[config("MONGODB_DATABASE_NAME")]
            collection = database[config("MONGODB_WATCH_LIST_COLLECTION")]
            return collection
        except Exception as ex:
            message = (
                f"UserRepository::_get_collection::Error when trying to get collection"
            )
            Gladsheim.error(error=ex, message=message)
            raise ex

    @classmethod
    async def exists(cls, product: WatchListProductModel):
        collection = await cls.__get_collection()
        id = product.get_id()
        query = {"_id": id}

        try:
            exists = bool(await collection.find_one(query))
            return exists

        except Exception as ex:
            message = f'UserRepository::exists::error when find watch list product'
            Gladsheim.error(
                error=ex,
                message=message,
                query=query
            )
            raise ex
