# Standards
from enum import IntEnum

# Third party
from strenum import StrEnum


class QueueTypes(IntEnum):
    SUITABILITY = 2


class UserOnboardingStep(StrEnum):
    SUITABILITY = "suitability"
