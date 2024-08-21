# STANDARD IMPORTS
from typing import List

# PROJECT IMPORTS
from func.src.domain.models.employ_position.model import EmployPositionModel, EmployPositionResponse


class EmployPositionToResponse:

    @staticmethod
    def employ_position_response(
            employ_position: List[EmployPositionResponse]
    ):

        employ_position_response = [
            EmployPositionModel(**employ_position.__repr__()).dict()
            for employ_position in employ_position
        ]

        return employ_position_response
