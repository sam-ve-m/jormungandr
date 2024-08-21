# Standards
from enum import IntEnum


class CodeResponse(IntEnum):
    SUCCESS = 0
    INVALID_ZENDESK_API_URL = 20
    ERROR_TO_REQUEST_ZENDESK_API = 21
    INTERNAL_SERVER_ERROR = 100
