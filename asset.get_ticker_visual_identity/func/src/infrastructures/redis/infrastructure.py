# Third party
from aioredis import from_url
from decouple import config
from etria_logger import Gladsheim


class RedisInfrastructure:
    redis = None

    @classmethod
    async def get_client(cls):
        if cls.redis is None:
            try:
                url = config("REDIS_HOST")
                cls.redis = await from_url(url, max_connections=10)
            except Exception as ex:
                Gladsheim.error(
                    error=ex,
                    message=f"RedisInfrastructure::get_client::Error on client connection for the given url",
                )
                raise ex
        return cls.redis
