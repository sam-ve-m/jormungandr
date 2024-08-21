from typing import Union

from etria_logger import Gladsheim
from mnemosine import SyncCache

from func.src.core.interfaces.repository.enum_advisor_cache.interface import (
    IEnumAdvisorCacheRepository,
)


class EnumAdvisorCacheRepository(IEnumAdvisorCacheRepository):
    enum_key = "jormungandr:EnumAdvisor"

    @classmethod
    def save_enum_advisor(cls, enum_advisor: list, time: int = 3600) -> bool:
        try:
            SyncCache.save(cls.enum_key, list(enum_advisor), int(time))
            return True
        except Exception as error:
            Gladsheim.error(error=error, message="Error saving enum in cache.")
            return False

    @classmethod
    def get_enum_advisor(cls) -> Union[list, None]:
        result = SyncCache.get(cls.enum_key)
        return result
