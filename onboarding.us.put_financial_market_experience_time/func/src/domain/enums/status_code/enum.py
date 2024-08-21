from enum import IntEnum


class InternalCode(IntEnum):
    SUCCESS = 0
    JWT_INVALID = 30
    INTERNAL_SERVER_ERROR = 100
    NOT_SENT_TO_PERSEPHONE = 60
    INVALID_PARAMS = 10
    UNIQUE_ID_WAS_NOT_UPDATED = 69
    TRANSPORT_ON_BOARDING_ERROR = 88
    USER_WAS_NOT_FOUND = 66
    NOT_A_VALID_ENUM = 77
    ERROR_LOGGIN_ON_IARA = 59

    def __repr__(self):
        return self.value
