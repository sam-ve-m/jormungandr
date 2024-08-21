from pydantic import BaseModel
from pydantic.types import constr


class Cep(BaseModel):
    cep: constr(regex="\d\d\d\d\d-\d\d\d")