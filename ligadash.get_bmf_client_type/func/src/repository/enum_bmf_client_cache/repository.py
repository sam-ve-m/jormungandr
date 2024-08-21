from typing import Union

from etria_logger import Gladsheim
from mnemosine import SyncCache

from func.src.core.interfaces.repository.enum_bmf_client_cache.interface import (
    IEnumBmfClientCacheRepository,
)


class EnumBmfClientCacheRepository(IEnumBmfClientCacheRepository):
    enum_key = "jormungandr:EnumBmfClient"

    @classmethod
    def save_enum_bmf_client(cls, enum_bmf_client: list, time: int = 3600) -> bool:
        try:
            SyncCache.save(cls.enum_key, list(enum_bmf_client), int(time))
            return True
        except Exception as error:
            Gladsheim.error(error=error, message="Error saving enum in cache.")
            return False

    @classmethod
    def get_enum_bmf_client(cls) -> Union[list, None]:
        result = SyncCache.get(cls.enum_key)
        return result
