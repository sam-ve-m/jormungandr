from typing import List, Optional
from etria_logger import Gladsheim
from mnemosine import SyncCache

from func.src.domain.exceptions.exceptions import FailToFetchData


class EmployTypeCacheRepository:
    enum_key = "jormungandr:EnumEmployType"

    @classmethod
    def save_employ_type_enum(cls, employ_type: list, time: int = 3600) -> bool:
        try:
            SyncCache.save(cls.enum_key, list(employ_type), time)
            return True
        except Exception as error:
            Gladsheim.error(error=error, message="Error saving enum in cache.")
            raise FailToFetchData()

    @classmethod
    def get_employ_type_enum(cls) -> Optional[List[tuple]]:
        try:
            result = SyncCache.get(cls.enum_key)
            return result
        except Exception as error:
            Gladsheim.error(error=error, message="Error saving enum in cache.")
            raise FailToFetchData()
