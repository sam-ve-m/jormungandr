# STANDARD IMPORTS
from typing import List, Tuple

# PROJECT IMPORTS
from func.src.repositories.base_repository.oracle.base import OracleBaseRepository
from func.src.repositories.enum_experience_cache.repository import (
    EnumExperienceTimeCacheRepository,
)


class ExperienceTimeEnumRepository:

    enum_query = "SELECT CODE as code, DESCRIPTION as description FROM USPIXDB001.SIGAME_TIME_EXPERIENCE"

    @classmethod
    def get_experience_time_enum(cls) -> List[Tuple]:
        sql = cls.enum_query
        result = cls._get_experience_time_cached_enum(sql)
        return result

    @classmethod
    def _get_experience_time_cached_enum(cls, query: str) -> List[Tuple]:
        if cached_enum := EnumExperienceTimeCacheRepository.get_enum_experience_time():
            return cached_enum

        enum_values = OracleBaseRepository.query(sql=query)
        EnumExperienceTimeCacheRepository.save_enum_experience_time(enum_values)
        return enum_values
