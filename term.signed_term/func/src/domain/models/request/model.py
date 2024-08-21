from pydantic import BaseModel

from func.src.domain.enums.terms import TermsFileType


class TermModel(BaseModel):
    file_type: TermsFileType
