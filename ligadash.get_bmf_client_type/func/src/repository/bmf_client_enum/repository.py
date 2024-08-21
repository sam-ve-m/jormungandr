from typing import List, Tuple

from func.src.core.interfaces.repository.bmf_client_enum.interface import (
    IBmfClientEnumRepository,
)
from func.src.repository.enum_bmf_client_cache.repository import (
    EnumBmfClientCacheRepository,
)
from func.src.repository.base_repository.oracle.repository import OracleBaseRepository


class BmfClientEnumRepository(IBmfClientEnumRepository):
    enum_query = """
            select TP_CLIENTE_BMF, DS_TIPO_CLIENTE from tsctipclibmf
        """

    @classmethod
    def get_bmf_client_enum(cls) -> List[Tuple]:
        sql = cls.enum_query
        result = cls._get_bmf_client_cached_enum(sql)
        return result

    @classmethod
    def _get_bmf_client_cached_enum(cls, query: str) -> List[Tuple]:
        if cached_enum := EnumBmfClientCacheRepository.get_enum_bmf_client():
            return cached_enum

        enum_values = OracleBaseRepository.query(sql=query)
        EnumBmfClientCacheRepository.save_enum_bmf_client(enum_values)
        return enum_values
