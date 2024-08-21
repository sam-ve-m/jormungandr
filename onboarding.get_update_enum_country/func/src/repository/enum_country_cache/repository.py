from typing import Union

from etria_logger import Gladsheim
from mnemosine import SyncCache

from func.src.core.interfaces.repository.enum_country_cache.interface import (
    IEnumCountryCacheRepository,
)


class EnumCountryCacheRepository(IEnumCountryCacheRepository):
    enum_key = "jormungandr:EnumCountry"

    @classmethod
    def save_enum_country(cls, enum_country: list, time: int = 3600) -> bool:
        try:
            SyncCache.save(cls.enum_key, list(enum_country), int(time))
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
    def get_enum_country(cls) -> Union[list, None]:
        result = SyncCache.get(cls.enum_key)
        return result
