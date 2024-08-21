from typing import List, Optional
from etria_logger import Gladsheim
from mnemosine import SyncCache

from func.src.domain.exceptions.exceptions import FailToFetchData


class EmployStatusCacheRepository:
    enum_key = "jormungandr:EnumEmployStatus"

    @classmethod
    def save_employ_status_enum(cls, employ_status: list, time: int = 3600) -> bool:
        try:
            SyncCache.save(cls.enum_key, list(employ_status), time)
            return True
        except Exception as error:
            Gladsheim.error(error=error, message="Error saving enum in cache.")
            raise FailToFetchData()

    @classmethod
    def get_employ_status_enum(cls) -> Optional[List[tuple]]:
        try:
            result = SyncCache.get(cls.enum_key)
            return result
        except Exception as error:
            Gladsheim.error(error=error, message="Error saving enum in cache.")
            raise FailToFetchData()
