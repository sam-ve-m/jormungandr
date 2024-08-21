from etria_logger import Gladsheim

from func.src.core.interfaces.service.experience_time_enum.interface import (
    IExperienceTimeEnumService,
)
from func.src.domain.response.model import ResponseModel
from func.src.domain.response.status_code.enums import StatusCode
from func.src.repository.experience_time_enum.repository import ExperienceTimeEnumRepository


class ExperienceTimeEnumService(IExperienceTimeEnumService):
    @classmethod
    def get_response(cls):
        service_response = []

        enums = ExperienceTimeEnumRepository.get_experience_time_enum()
        for code, value in enums:
            service_response.append({"code": code, "value": value})

        service_response = ResponseModel.build_response(
            success=True, code=StatusCode.SUCCESS, message=None, result=service_response
        )
        return service_response
