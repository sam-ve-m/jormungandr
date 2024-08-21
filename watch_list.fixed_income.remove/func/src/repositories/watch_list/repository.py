from decouple import config
from etria_logger import Gladsheim
from nidavellir import Sindri

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
                f"UserRepository::_get_collection::Error trying to get collection"
            )
            Gladsheim.error(error=ex, message=message)
            raise ex

    @classmethod
    async def remove_product_from_watch_list(cls, product: WatchListProductModel):
        client = cls.infra.get_client()
        collection = await cls.__get_collection()
        product_filter = {"_id": product.get_id()}

        try:
            async with await client.start_session() as session:
                async with session.start_transaction():
                    await collection.delete_one(product_filter, session=session)

        except Exception as ex:
            message = f"UserRepository::remove_product_from_watch_list"
            Gladsheim.error(
                error=ex,
                query=product_filter,
                message=message
            )
            raise ex
