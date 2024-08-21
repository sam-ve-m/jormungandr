from typing import List, Tuple

from func.src.core.interfaces.repository.activity_type_enum.interface import IActivityTypeEnumRepository
from func.src.repository.enum_activity_type_cache.repository import EnumActivityTypeCacheRepository
from func.src.repository.base_repository.oracle.repository import OracleBaseRepository


class ActivityTypeEnumRepository(IActivityTypeEnumRepository):

    enum_query = """
            SELECT CODE as code, DESCRIPTION as description
            FROM USPIXDB001.SINCAD_EXTERNAL_PROFESSIONAL
        """

    @classmethod
    def get_activity_type_enum(cls) -> List[Tuple]:
        sql = cls.enum_query
        result = cls._get_activity_type_cached_enum(sql)
        return result

    @classmethod
    def _get_activity_type_cached_enum(cls, query: str) -> List[Tuple]:
        if cached_enum := EnumActivityTypeCacheRepository.get_enum_activity_type():
            return cached_enum

        enum_values = OracleBaseRepository.query(sql=query)
        EnumActivityTypeCacheRepository.save_enum_activity_type(enum_values)
        return enum_values
