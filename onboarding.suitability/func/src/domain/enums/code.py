# Standards
from enum import IntEnum


class InternalCode(IntEnum):
    SUCCESS = 0
    INVALID_PARAMS = 10
    ONBOARDING_STEP_INCORRECT = 70
    ONBOARDING_STEP_REQUEST_FAILURE = 71
    JWT_INVALID = 30
    ERROR_IN_KHONSHU = 96
    ERROR_SENDING_TO_PERSEPHONE = 97
    DATA_ALREADY_EXISTS = 98
    DATA_NOT_FOUND = 99
    INTERNAL_SERVER_ERROR = 100
    API_ERROR = 101
