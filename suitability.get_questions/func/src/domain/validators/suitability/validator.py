# Standards
from datetime import datetime
from typing import List

# Third party
from pydantic import BaseModel


class AnswerValidator(BaseModel):
    option_id: int
    text: str
    weight: int


class QuestionValidator(BaseModel):
    order_id: int
    text: str
    answers: List[AnswerValidator]
    weight: int


class SuitabilityValidator(BaseModel):
    questions: List[QuestionValidator]
    date: datetime
    version: int
