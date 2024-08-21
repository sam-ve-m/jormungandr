from typing import List

from func.src.domain.models.employ_type.model import EmployTypeModel
from func.src.repositories.cache.repository import EmployTypeCacheRepository
from func.src.repositories.oracle.repository import EmployTypeOracleRepository


class EmployTypeService:

    @classmethod
    def get_employ_type_response(cls) -> List[dict]:
        enum_values = EmployTypeCacheRepository.get_employ_type_enum()
        if not enum_values:
            enum_values = EmployTypeOracleRepository.get_employ_type()
            EmployTypeCacheRepository.save_employ_type_enum(enum_values)
        response = list(map(
            EmployTypeModel.from_database, enum_values
        ))
        return response
