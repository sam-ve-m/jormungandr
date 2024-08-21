from typing import List, Tuple

from func.src.core.interfaces.repository.country_enum.interface import ICountryEnumRepository
from func.src.repository.enum_country_cache.repository import EnumCountryCacheRepository
from func.src.repository.base_repository.oracle.repository import OracleBaseRepository


class CountryEnumRepository(ICountryEnumRepository):

    enum_query = """
            SELECT SG_PAIS as initials, NM_PAIS as description
            FROM CORRWIN.TSCPAIS
        """

    @classmethod
    def get_country_enum(cls) -> List[Tuple]:
        sql = cls.enum_query
        result = cls._get_country_cached_enum(sql)
        return result

    @classmethod
    def _get_country_cached_enum(cls, query: str) -> List[Tuple]:
        if cached_enum := EnumCountryCacheRepository.get_enum_country():
            return cached_enum

        enum_values = OracleBaseRepository.query(sql=query)
        EnumCountryCacheRepository.save_enum_country(enum_values)
        return enum_values
