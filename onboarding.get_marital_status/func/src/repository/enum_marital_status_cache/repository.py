from typing import Union

from etria_logger import Gladsheim
from mnemosine import SyncCache

from func.src.core.interfaces.repository.enum_marital_status_cache.interface import (
    IEnumMaritalStatusCacheRepository,
)


class EnumMaritalStatusCacheRepository(IEnumMaritalStatusCacheRepository):
    enum_key = "jormungandr:onboarding:EnumMaritalStatus"

    @classmethod
    def save_enum_marital_status(
        cls, enum_marital_status: list, time: int = 3600
    ) -> bool:
        try:
            SyncCache.save(cls.enum_key, list(enum_marital_status), int(time))
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
    def get_enum_marital_status(cls) -> Union[list, None]:
        result = SyncCache.get(cls.enum_key)
        return result
