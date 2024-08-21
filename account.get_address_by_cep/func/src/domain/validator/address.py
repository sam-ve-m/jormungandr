from typing import Optional, Union

from decouple import config
from pydantic import BaseModel


class AddressEnum(BaseModel):
    code: Union[int, str]
    value: str


class AddressEnums(BaseModel):
    state: AddressEnum
    city: AddressEnum


class Address(BaseModel):
    bairro: str
    cep: str
    cidade: str
    logradouro: str
    uf: str
    complemento: Optional[str]


    def liga_template(self, address_enum: AddressEnums) -> dict:
        address = {
            "country": {"code": config("DEFAULT_BR_COUNTRY_CODE"), "value": config("DEFAULT_BR_COUNTRY_VALUE")},
            "state": {"code": self.uf, "value": address_enum.state.value},
            "city": {"code": address_enum.city.code,"value": self.cidade},
            "neighborhood": {"value": self.bairro},
            "street_name": {"value": self.logradouro},
            "zip_code": {"value": self.cep},
            "complement": {"value": self.complemento}
        }
        return address
