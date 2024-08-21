from typing import List, Tuple

from func.src.core.interfaces.repository.state_enum.interface import IStateEnumRepository
from func.src.repository.enum_state_cache.repository import EnumStateCacheRepository
from func.src.repository.base_repository.oracle.repository import OracleBaseRepository


class StateEnumRepository(IStateEnumRepository):

    enum_query = """
            SELECT SG_ESTADO as initials, NM_ESTADO as description
            FROM CORRWIN.TSCESTADO
            WHERE SG_PAIS='{}'
        """

    @classmethod
    def get_state_enum(cls, country: str) -> List[Tuple]:
        sql = cls.enum_query
        result = cls._get_state_cached_enum(sql, country)
        return result

    @classmethod
    def _get_state_cached_enum(cls, query: str, country: str) -> List[Tuple]:
        if cached_enum := EnumStateCacheRepository.get_enum_state(country):
            return cached_enum
        query = query.format(country)
        enum_values = OracleBaseRepository.query(sql=query)
        EnumStateCacheRepository.save_enum_state(enum_values, country)
        return enum_values
