# Standards
from enum import IntEnum


class InternalCode(IntEnum):
    SUCCESS = 0
    INVALID_PARAMS = 10
    JWT_INVALID = 30
    DATA_VALIDATION_ERROR = 97
    DATA_ALREADY_EXISTS = 98
    DATA_NOT_FOUND = 99
    INTERNAL_SERVER_ERROR = 100
