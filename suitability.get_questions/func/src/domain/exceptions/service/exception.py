# Jormungandr
from ..base_exceptions.exception import ServiceException
from ...enums.response import InternalCode


# Standards
from http import HTTPStatus


class ErrorOnDecodeJwt(ServiceException):
    def __init__(self, *args, **kwargs):
        self.msg = "Invalid Jwt"
        self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        self.code = InternalCode.JWT_INVALID
        self.success = False
        super().__init__(
            self.msg, self.status_code, self.code, self.success, args, kwargs
        )
