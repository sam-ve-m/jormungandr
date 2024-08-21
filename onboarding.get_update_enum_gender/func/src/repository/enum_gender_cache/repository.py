from typing import Union

from etria_logger import Gladsheim
from mnemosine import SyncCache

from func.src.core.interfaces.repository.enum_gender_cache.interface import (
    IEnumGenderCacheRepository,
)


class EnumGenderCacheRepository(IEnumGenderCacheRepository):
    enum_key = "jormungandr:EnumGender"

    @classmethod
    def save_enum_gender(cls, enum_gender: list, time: int = 3600) -> bool:
        try:
            SyncCache.save(cls.enum_key, list(enum_gender), int(time))
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
    def get_enum_gender(cls) -> Union[list, None]:
        result = SyncCache.get(cls.enum_key)
        return result
