from decouple import config
from etria_logger import Gladsheim
from mnemosine import SyncCache

from src.core.interfaces.repositories.cache.interface import (
    ICacheRepository,
)


class CacheRepository(ICacheRepository):
    enum_key = "jormungandr:TermFile:{}"
    cache_time = int(config("CACHE_EXPIRATION_TIME_IN_SECONDS"))

    @classmethod
    def save_term_in_cache(
        cls, term_link: str, term_file: str, time: int = cache_time
    ) -> bool:
        try:
            SyncCache.save(cls.enum_key.format(term_file), str(term_link), int(time))
            return True
        except Exception as error:
            Gladsheim.error(error=error, message="Error saving term link in cache.")
            return False

    @classmethod
    def get_cached_term(cls, term_file: str) -> str:
        result = None
        try:
            result = SyncCache.get(cls.enum_key.format(term_file))
        except Exception as error:
            Gladsheim.error(error=error, message="Error getting term link in cache.")
        return result
