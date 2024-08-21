from decouple import config
from etria_logger import Gladsheim
from mnemosine import SyncCache

from func.src.core.interfaces.repositories.cache.interface import (
    ICacheRepository,
)


class CacheRepository(ICacheRepository):
    enum_key = "jormungandr:BankLogo:{}"
    cache_time = int(config("CACHE_EXPIRATION_TIME_IN_SECONDS"))

    @classmethod
    def save_logo_in_cache(
        cls, logo_link: str, bank_code: str, time: int = cache_time
    ) -> bool:
        try:
            SyncCache.save(cls.enum_key.format(bank_code), str(logo_link), int(time))
            return True
        except ValueError as error:
            Gladsheim.error(error=error, message="Error saving logo in cache.")
            return False
        except TypeError as error:
            Gladsheim.error(error=error, message="Error saving logo in cache.")
            return False
        except Exception as error:
            Gladsheim.error(error=error, message="Error saving logo in cache.")
            return False

    @classmethod
    def get_cached_logo(cls, bank_code: str) -> str:
        result = None
        try:
            result = SyncCache.get(cls.enum_key.format(bank_code))
        except Exception as error:
            Gladsheim.error(error=error, message="Error getting logo in cache.")
        return result
