from typing import List

from pydantic import BaseModel

from ..enums.types import TermsType


class TermFiles(BaseModel):
    terms_file: List[TermsType]
