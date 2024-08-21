# STANDARD IMPORTS
from enum import IntEnum


class InternalCode(IntEnum):
    SUCCESS = 0
    INTERNAL_SERVER_ERROR = 100
    TRANSPORT_LAYER_ERROR = 69
    USER_WAS_NOT_FOUND = 99
    CARONTE_TRANSPORT_ERROR = 59
    STATUS_SENT_IS_NOT_A_VALID_ENUM = 89

    def __repr__(self):
        return self.value
