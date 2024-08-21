from func.src.core.interfaces.service.advisor_enum.interface import IAdvisorEnumService
from func.src.domain.response.model import ResponseModel
from func.src.domain.response.status_code.enums import StatusCode
from func.src.repository.advisor_enum.repository import AdvisorEnumRepository


class AdvisorEnumService(IAdvisorEnumService):
    @classmethod
    def get_response(cls):
        service_response = []

        enums = AdvisorEnumRepository.get_advisor_enum()
        for code, value in enums:
            service_response.append({"code": code, "value": value})

        service_response = ResponseModel.build_response(
            success=True, code=StatusCode.SUCCESS, message=None, result=service_response
        )
        return service_response
