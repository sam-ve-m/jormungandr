from etria_logger import Gladsheim

from func.src.core.interfaces.service.state_enum.interface import IStateEnumService
from func.src.domain.response.model import ResponseModel
from func.src.domain.response.status_code.enums import StatusCode
from func.src.domain.validators.state.validator import StateParams
from func.src.repository.state_enum.repository import StateEnumRepository


class StateEnumService(IStateEnumService):
    @classmethod
    def get_response(cls, request: StateParams):
        service_response = []
        country = request.country.value

        enums = StateEnumRepository.get_state_enum(country)
        for code, value in enums:
            service_response.append({"code": code, "value": value})

        service_response = ResponseModel.build_response(
            success=True, code=StatusCode.SUCCESS, message=None, result=service_response
        )
        return service_response
