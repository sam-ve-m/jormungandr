from etria_logger import Gladsheim

from func.src.core.interfaces.service.activity_type_enum.interface import IActivityTypeEnumService
from func.src.domain.response.model import ResponseModel
from func.src.domain.response.status_code.enums import StatusCode
from func.src.repository.activity_type_enum.repository import ActivityTypeEnumRepository


class ActivityTypeEnumService(IActivityTypeEnumService):
    @classmethod
    def get_response(cls):
        enums = ActivityTypeEnumRepository.get_activity_type_enum()
        service_response = sorted((
            {"code": code, "value": value}
            for code, value in enums
        ), key=lambda activity: activity["value"])

        service_response = ResponseModel.build_response(
            success=True, code=StatusCode.SUCCESS, message=None, result=service_response
        )
        return service_response
