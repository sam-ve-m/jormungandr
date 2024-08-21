# Jormungandr
from ...enums.types import TermType, VariableIncomeQuoteType, FixedIncomeRiskClassification

# Third party
from pydantic import BaseModel, constr

# Standards
from typing import Union


class VariableIncomeValidator(BaseModel):
    symbol: constr(min_length=3, to_upper=True)
    quote_type: VariableIncomeQuoteType
    quantity: int


class FixedIncomeValidator(BaseModel):
    product_id: int
    quantity: int
    risk: FixedIncomeRiskClassification


class TermWithOrder(BaseModel):
    order: Union[VariableIncomeValidator, FixedIncomeValidator]
    term_type: TermType
