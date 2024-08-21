from pydantic import BaseModel

from src.domain.enums.terms.enum import TermsFileType


class TermModel(BaseModel):
    file_type: TermsFileType
