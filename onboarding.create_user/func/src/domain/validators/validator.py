# Jormungandr
from ...domain.exceptions.exceptions import InvalidEmail

# Standards
import re
from typing import Optional

# Third party
from pydantic import BaseModel, validator


class UserParams(BaseModel):
    email: str
    nick_name: str

    @validator("email")
    def validate_email(cls, email: str):
        regex = r"^([\w-]+(?:\.[\w-]+)*)@((?:[\w-]+\.)*\w[\w-]{1,66})\.([a-z]{2,3}(?:\.[a-z]{2})?)$"
        if not re.search(regex, email):
            raise InvalidEmail
        return email
