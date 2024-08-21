from typing import List, Tuple

from func.src.core.interfaces.repository.brokerage_type_enum.interface import (
    IBrokerageTypeEnumRepository,
)
from func.src.repository.enum_brokerage_type_cache.repository import (
    EnumBrokerageTypeCacheRepository,
)
from func.src.repository.base_repository.oracle.repository import OracleBaseRepository


class BrokerageTypeEnumRepository(IBrokerageTypeEnumRepository):
    enum_query = """
            SELECT CD_POLITICA, DS_POLITICA from tbocorr_poli
        """

    @classmethod
    def get_brokerage_type_enum(cls) -> List[Tuple]:
        sql = cls.enum_query
        result = cls._get_brokerage_type_cached_enum(sql)
        return result

    @classmethod
    def _get_brokerage_type_cached_enum(cls, query: str) -> List[Tuple]:
        if cached_enum := EnumBrokerageTypeCacheRepository.get_enum_brokerage_type():
            return cached_enum

        enum_values = OracleBaseRepository.query(sql=query)
        EnumBrokerageTypeCacheRepository.save_enum_brokerage_type(enum_values)
        return enum_values
