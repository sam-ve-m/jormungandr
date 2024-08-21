from etria_logger import Gladsheim

from func.src.core.interfaces.service.country_enum.interface import ICountryEnumService
from func.src.domain.response.model import ResponseModel
from func.src.domain.response.status_code.enums import StatusCode
from func.src.repository.country_enum.repository import CountryEnumRepository


class CountryEnumService(ICountryEnumService):
    @classmethod
    def get_response(cls):
        service_response = []

        enums = CountryEnumRepository.get_country_enum()
        for code, value in enums:
            service_response.append({"code": code, "value": value})

        service_response = ResponseModel.build_response(
            success=True, code=StatusCode.SUCCESS, message=None, result=service_response
        )
        return service_response
