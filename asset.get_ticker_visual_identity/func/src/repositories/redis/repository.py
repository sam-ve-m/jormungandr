# Jormungandr
from ...infrastructures.redis.infrastructure import RedisInfrastructure

# Third party
from decouple import config
from etria_logger import Gladsheim


class RedisRepository:
    @classmethod
    async def get(cls, key: str) -> bytes:
        redis = await RedisInfrastructure.get_client()
        ticket_custom_fields = await redis.get(key)
        return ticket_custom_fields

    @classmethod
    async def set(cls, key: str, value: str):
        redis = await RedisInfrastructure.get_client()
        try:
            await redis.set(
                key,
                value,
                ex=int(config("REDIS_DATA_EXPIRATION_IN_SECONDS")),
            )
        except Exception as ex:
            message = f"RedisRepository::set::error to set data"
            Gladsheim.error(error=ex, message=message)
            raise ex
