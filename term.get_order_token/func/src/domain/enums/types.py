# Third party
from strenum import StrEnum


class TermType(StrEnum):
    REFUSAL = "term_refusal"
    MISMATCH_PROFILE = "term_mismatch_profile"


class VariableIncomeQuoteType(StrEnum):
    STOCK = "stock"
    FII = "fii"
    OPTION = "option"
    FUTURE = "future"
    BOND = "bond"
    ETF = "etf"
    OTHERS = "others"


class FixedIncomeRiskClassification(StrEnum):
    VERY_LOW = "VERY_LOW"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
