from typing import List, Tuple

from func.src.core.interfaces.repository.nationality_enum.interface import INationalityEnumRepository
from func.src.repository.enum_nationality_cache.repository import EnumNationalityCacheRepository
from func.src.repository.base_repository.oracle.repository import OracleBaseRepository


class NationalityEnumRepository(INationalityEnumRepository):

    enum_query = """
            SELECT CODE as code, DESCRIPTION as description
            FROM USPIXDB001.SINCAD_EXTERNAL_NATIONALITY
        """

    @classmethod
    def get_nationality_enum(cls) -> List[Tuple]:
        sql = cls.enum_query
        result = cls._get_nationality_cached_enum(sql)
        return result

    @classmethod
    def _get_nationality_cached_enum(cls, query: str) -> List[Tuple]:
        if cached_enum := EnumNationalityCacheRepository.get_enum_nationality():
            return cached_enum

        enum_values = OracleBaseRepository.query(sql=query)
        EnumNationalityCacheRepository.save_enum_nationality(enum_values)
        return enum_values
