from pydantic import BaseModel, validator
from func.src.domain.enums.file.file_type import ImageType


class BankVisualIdentityModel(BaseModel):
    bank_code: int
    type: ImageType

    @validator("bank_code")
    def validate_bank_code(cls, bank_code):
        if bank_code < 0:
            raise ValueError()
        return bank_code
