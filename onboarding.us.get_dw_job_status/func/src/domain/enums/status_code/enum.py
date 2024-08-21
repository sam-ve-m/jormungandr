# STANDARD IMPORTS
from enum import IntEnum


class InternalCode(IntEnum):
    SUCCESS = 0
    INVALID_PARAMS = 10
    JWT_INVALID = 30
    INTERNAL_SERVER_ERROR = 100
    DATA_NOT_FOUND = 99

    def __repr__(self):
        return str(self.value)
