import http

import orjson
from decouple import config
from etria_logger import Gladsheim

from func.src.domain.exceptions.exceptions import CityEnumNotFound, StateEnumNotFound, ErrorRequestingEnum
from func.src.infrastructure.http.infrastructure import HttpInfrastructure
from func.src.domain.validator.address import AddressEnum


class JormungandrEnums:
    @staticmethod
    async def _request(url: str, params: dict) -> list:
        session = HttpInfrastructure.get_session()
        response = await session.get(url, params=params)
        response_content = await response.text()
        if response.status != http.HTTPStatus.OK:
            Gladsheim.error(message="Unable to get enum", content=response_content)
            raise ErrorRequestingEnum()
        response_json = orjson.loads(response_content)
        return response_json.get("result")

    @classmethod
    async def find_city_enum_code(cls, city: str, state: str) -> AddressEnum:
        url = config("JORMUNGANDR_URL_ENUM_CITY")
        cities = await cls._request(url, {
            "country": config("DEFAULT_BR_COUNTRY_CODE"),
            "state": state,
        })
        for response_city in cities:
            if city.upper() == response_city["value"]:
                return AddressEnum(value=city, code=response_city["code"])
        Gladsheim.error(message="Unable to find city", city=city)
        raise CityEnumNotFound()

    @classmethod
    async def find_state_enum_code(cls, state: str) -> AddressEnum:
        url = config("JORMUNGANDR_URL_ENUM_STATE")
        states = await cls._request(url, {"country": config("DEFAULT_BR_COUNTRY_CODE")})
        for response_state in states:
            if state == response_state["code"]:
                return AddressEnum(code=state, value=response_state["value"])
        Gladsheim.error(message="Unable to find state", state=state)
        raise StateEnumNotFound()
