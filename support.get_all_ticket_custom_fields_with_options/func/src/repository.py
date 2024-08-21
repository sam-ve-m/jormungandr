# Jormungandr
from .infrastructure import RedisInfrastructure

# Third party
from decouple import config
from etria_logger import Gladsheim


class RedisRepository:
    redis = RedisInfrastructure.get_client()

    @classmethod
    def get(cls) -> bytes:
        ticket_custom_fields = cls.redis.get(config("REDIS_KEY_CUSTOM_FIELDS"))
        return ticket_custom_fields

    @classmethod
    def set(cls, ticket_custom_fields: dict):
        try:
            cls.redis.set(
                config("REDIS_KEY_CUSTOM_FIELDS"),
                str(ticket_custom_fields),
                ex=int(config("REDIS_DATA_EXPIRATION_IN_SECONDS")),
            )
        except Exception as ex:
            message = f"RedisRepository::set::error to set data"
            Gladsheim.error(error=ex, message=message)
            raise ex
