# Jormungandr - Onboarding
from ....infrastructures.mongo_db.infrastructure import MongoDBInfrastructure

# Standards
from abc import abstractmethod


class MongoDbBaseRepository:
    infra = MongoDBInfrastructure

    @classmethod
    @abstractmethod
    async def _get_collection(cls):
        pass
