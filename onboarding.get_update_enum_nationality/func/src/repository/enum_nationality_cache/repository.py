from typing import Union

from etria_logger import Gladsheim
from mnemosine import SyncCache

from func.src.core.interfaces.repository.enum_nationality_cache.interface import (
    IEnumNationalityCacheRepository,
)


class EnumNationalityCacheRepository(IEnumNationalityCacheRepository):
    enum_key = "jormungandr:EnumNationality"

    @classmethod
    def save_enum_nationality(cls, enum_nationality: list, time: int = 3600) -> bool:
        try:
            SyncCache.save(cls.enum_key, list(enum_nationality), int(time))
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
    def get_enum_nationality(cls) -> Union[list, None]:
        result = SyncCache.get(cls.enum_key)
        return result
