from typing import Union

from etria_logger import Gladsheim
from mnemosine import SyncCache

from func.src.core.interfaces.repository.enum_state_cache.interface import (
    IEnumStateCacheRepository,
)


class EnumStateCacheRepository(IEnumStateCacheRepository):
    enum_key = "jormungandr:EnumState:{}"

    @classmethod
    def save_enum_state(cls, enum_state: list, country: str, time: int = 3600) -> bool:
        try:
            SyncCache.save(cls.enum_key.format(country), list(enum_state), int(time))
            return True
        except ValueError as error:
            Gladsheim.error(error=error, message="Error saving enum in cache.")
            return False
        except TypeError as error:
            Gladsheim.error(error=error, message="Error saving enum in cache.")
            return False
        except Exception as error:
            Gladsheim.error(error=error, message="Error saving enum in cache.")
            return False

    @classmethod
    def get_enum_state(cls, country: str) -> Union[list, None]:
        result = SyncCache.get(cls.enum_key.format(country))
        return result
