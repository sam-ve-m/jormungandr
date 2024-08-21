# Suitability
from ....infrastructures.mongo_db.infrastructure import MongoDBInfrastructure


# Third party
from decouple import config
from etria_logger import Gladsheim


class SuitabilityRepository(MongoDBInfrastructure):
    @classmethod
    async def _get_collection(cls):
        mongo_client = cls.get_client()
        try:
            database = mongo_client[config("MONGODB_DATABASE_NAME")]
            collection = database[config("MONGODB_SUITABILITY_COLLECTION")]
            return collection
        except Exception as ex:
            Gladsheim.error(
                error=ex, message="Error when trying to get mongo collection"
            )
            raise ex

    @classmethod
    async def get_latest_suitability(cls) -> dict:
        collection = await cls._get_collection()
        suitability = await collection.find_one(
            {"$query": {}, "$orderby": {"version": -1}}
        )
        return suitability
