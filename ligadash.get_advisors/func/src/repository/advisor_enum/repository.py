from typing import List, Tuple

from func.src.core.interfaces.repository.advisor_enum.interface import IAdvisorEnumRepository
from func.src.repository.enum_advisor_cache.repository import EnumAdvisorCacheRepository
from func.src.repository.base_repository.oracle.repository import OracleBaseRepository


class AdvisorEnumRepository(IAdvisorEnumRepository):
    enum_query = """
            SELECT CD_ASSESSOR, NM_ASSESSOR FROM tscasses
        """

    @classmethod
    def get_advisor_enum(cls) -> List[Tuple]:
        sql = cls.enum_query
        result = cls._get_advisor_cached_enum(sql)
        return result

    @classmethod
    def _get_advisor_cached_enum(cls, query: str) -> List[Tuple]:
        if cached_enum := EnumAdvisorCacheRepository.get_enum_advisor():
            return cached_enum

        enum_values = OracleBaseRepository.query(sql=query)
        EnumAdvisorCacheRepository.save_enum_advisor(enum_values)
        return enum_values
