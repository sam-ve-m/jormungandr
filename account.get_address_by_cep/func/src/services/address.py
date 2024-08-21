import asyncio
import unidecode

from ..domain.validator.address import Address, AddressEnums
from ..domain.validator.cep import Cep
import pycep_correios

from ..transport.enums import JormungandrEnums


class AddressService:
    @classmethod
    async def get_address(cls, cep: Cep) -> dict:
        raw_address = pycep_correios.get_address_from_cep(cep.cep, webservice=pycep_correios.WebService.CORREIOS)
        address = Address(**raw_address)
        address_enums = await cls._request_address_enums(address)
        template = address.liga_template(address_enums)
        return template

    @staticmethod
    async def _request_address_enums(address: Address) -> AddressEnums:
        state, city = await asyncio.gather(*(
            JormungandrEnums.find_state_enum_code(address.uf),
            JormungandrEnums.find_city_enum_code(unidecode.unidecode(address.cidade), address.uf),
        ))
        return AddressEnums(
            state=state,
            city=city,
        )
