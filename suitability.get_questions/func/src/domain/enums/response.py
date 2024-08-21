# Standards
from enum import IntEnum


class InternalCode(IntEnum):
    SUCCESS = 0
    JWT_INVALID = 30
    DATA_NOT_FOUND = 99
    INTERNAL_SERVER_ERROR = 100
    VALIDATION_ERROR = 110
