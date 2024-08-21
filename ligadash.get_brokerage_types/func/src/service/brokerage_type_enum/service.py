from func.src.core.interfaces.service.brokerage_type_enum.interface import (
    IBrokerageTypeEnumService,
)
from func.src.domain.response.model import ResponseModel
from func.src.domain.response.status_code.enums import StatusCode
from func.src.repository.brokerage_type_enum.repository import BrokerageTypeEnumRepository


class BrokerageTypeEnumService(IBrokerageTypeEnumService):
    @classmethod
    def get_response(cls):
        service_response = []

        enums = BrokerageTypeEnumRepository.get_brokerage_type_enum()
        for code, value in enums:
            service_response.append({"code": code, "value": value})

        service_response = ResponseModel.build_response(
            success=True, code=StatusCode.SUCCESS, message=None, result=service_response
        )
        return service_response
