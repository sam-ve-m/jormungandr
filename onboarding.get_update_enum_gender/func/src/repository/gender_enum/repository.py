from typing import List, Tuple

from func.src.core.interfaces.repository.gender_enum.interface import IGenderEnumRepository
from func.src.repository.enum_gender_cache.repository import EnumGenderCacheRepository
from func.src.repository.base_repository.oracle.repository import OracleBaseRepository


class GenderEnumRepository(IGenderEnumRepository):

    enum_query = """
            SELECT CODE as code, DESCRIPTION as description
            FROM USPIXDB001.SIGAME_GENDER
        """

    @classmethod
    def get_gender_enum(cls) -> List[Tuple]:
        sql = cls.enum_query
        result = cls._get_gender_cached_enum(sql)
        return result

    @classmethod
    def _get_gender_cached_enum(cls, query: str) -> List[Tuple]:
        if cached_enum := EnumGenderCacheRepository.get_enum_gender():
            return cached_enum

        enum_values = OracleBaseRepository.query(sql=query)
        EnumGenderCacheRepository.save_enum_gender(enum_values)
        return enum_values
