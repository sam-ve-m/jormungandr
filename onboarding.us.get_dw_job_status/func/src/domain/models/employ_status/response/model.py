# STANDARD IMPORTS
from typing import List

# PROJECT IMPORTS
from func.src.domain.models.employ_status.model import EmployStatusModel, EmployStatusResponse


class EmployStatusToResponse:

    @staticmethod
    def employ_status_response(
            employ_status: List[EmployStatusResponse]
    ):

        employ_status_response = [
            EmployStatusModel(**employ_position.__repr__()).dict()
            for employ_position in employ_status
        ]

        return employ_status_response
