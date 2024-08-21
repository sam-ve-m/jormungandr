from typing import List

from func.src.domain.models.employ_status.model import EmployStatusModel
from func.src.repositories.cache.repository import EmployStatusCacheRepository
from func.src.repositories.oracle.repository import EmployStatusOracleRepository


class EmployStatusService:

    @classmethod
    def get_employ_status_response(cls) -> List[dict]:
        enum_values = EmployStatusCacheRepository.get_employ_status_enum()
        if not enum_values:
            enum_values = EmployStatusOracleRepository.get_employ_status()
            EmployStatusCacheRepository.save_employ_status_enum(enum_values)
        response = list(map(
            EmployStatusModel.from_database, enum_values
        ))
        return response
