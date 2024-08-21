from typing import Union

from etria_logger import Gladsheim
from mnemosine import SyncCache

from func.src.core.interfaces.repository.enum_activity_type_cache.interface import (
    IEnumActivityTypeCacheRepository,
)


class EnumActivityTypeCacheRepository(IEnumActivityTypeCacheRepository):
    enum_key = "jormungandr:EnumActivityType"

    @classmethod
    def save_enum_activity_type(cls, enum_activity_type: list, time: int = 3600) -> bool:
        try:
            SyncCache.save(cls.enum_key, list(enum_activity_type), int(time))
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
    def get_enum_activity_type(cls) -> Union[list, None]:
        result = SyncCache.get(cls.enum_key)
        return result
