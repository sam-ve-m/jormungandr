# Third party
from decouple import config
from etria_logger import Gladsheim
from redis import from_url


class RedisInfrastructure:
    redis = None

    @classmethod
    def get_client(cls):
        if cls.redis is None:
            url = config("REDIS_HOST")
            try:
                cls.redis = from_url(url, max_connections=10)
            except Exception as ex:
                Gladsheim.error(
                    error=ex,
                    message=f"RedisInfrastructure::get_client::Error on client connection for the giving url {url}",
                )
                raise ex
        return cls.redis
