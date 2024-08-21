from typing import List

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
                f"UserRepository::_get_collection::Error when trying to get collection"
            )
            Gladsheim.error(error=ex, message=message)
            raise ex

    @classmethod
    async def insert_all_products_in_watch_list(
        cls, products: List[WatchListProductModel]
    ):
        client = cls.infra.get_client()
        collection = await cls.__get_collection()

        try:
            async with await client.start_session() as session:
                async with session.start_transaction():
                    for product in products:
                        product_filter = {"_id": product.get_id()}
                        watch_list_product_dict = product.to_dict()
                        Sindri.dict_to_primitive_types(watch_list_product_dict)

                        await collection.update_one(
                            filter=product_filter,
                            update={"$set": watch_list_product_dict},
                            upsert=True,
                            session=session,
                        )

        except Exception as ex:
            message = f"UserRepository::insert_all_products_in_watch_list"
            Gladsheim.error(error=ex, message=message)
            raise ex
