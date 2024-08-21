# STANDARD IMPORTS
from typing import List

# PROJECT IMPORTS
from func.src.domain.models.employ_type.model import EmployTypeModel, EmployTypeResponse


class EmployTypeToResponse:

    @staticmethod
    def employ_type_response(
            employ_type: List[EmployTypeResponse]
    ):

        employ_type_response = [
            EmployTypeModel(**employ_position.__repr__()).dict()
            for employ_position in employ_type
        ]

        return employ_type_response
