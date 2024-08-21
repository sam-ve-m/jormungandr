from typing import Union

from etria_logger import Gladsheim
from mnemosine import SyncCache

from func.src.core.interfaces.repository.enum_brokerage_type_cache.interface import (
    IEnumBrokerageTypeCacheRepository,
)


class EnumBrokerageTypeCacheRepository(IEnumBrokerageTypeCacheRepository):
    enum_key = "jormungandr:EnumBrokerageType"

    @classmethod
    def save_enum_brokerage_type(
        cls, enum_brokerage_type: list, time: int = 3600
    ) -> bool:
        try:
            SyncCache.save(cls.enum_key, list(enum_brokerage_type), int(time))
            return True
        except Exception as error:
            Gladsheim.error(error=error, message="Error saving enum in cache.")
            return False

    @classmethod
    def get_enum_brokerage_type(cls) -> Union[list, None]:
        result = SyncCache.get(cls.enum_key)
        return result
