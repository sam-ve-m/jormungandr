# Jormungandr - Onboarding
from ..base.base_exceptions import ServiceException
from ...enums.code import InternalCode

# Standards
from http import HTTPStatus


class ErrorOnDecodeJwt(ServiceException):
    def __init__(self, *args, **kwargs):
        self.msg = "Fail trying to decode jwt"
        self.status_code = HTTPStatus.BAD_REQUEST
        self.internal_code = InternalCode.JWT_INVALID
        self.success = False
        super().__init__(
            self.msg,
            self.status_code,
            self.internal_code,
            self.success,
            *args,
            **kwargs
        )


class ErrorOnGetUniqueId(ServiceException):
    def __init__(self, *args, **kwargs):
        self.msg = "Fail when trying to get customer unique_id from jwt"
        self.status_code = HTTPStatus.UNAUTHORIZED
        self.internal_code = InternalCode.JWT_INVALID
        self.success = False
        super().__init__(
            self.msg,
            self.status_code,
            self.internal_code,
            self.success,
            *args,
            **kwargs
        )


class ErrorCalculatingCustomerSuitability(ServiceException):
    def __init__(self, *args, **kwargs):
        self.msg = (
            "Fail when trying to calculating customer score and profile suitability"
        )
        self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        self.internal_code = InternalCode.ERROR_IN_KHONSHU
        self.success = False
        super().__init__(
            self.msg,
            self.status_code,
            self.internal_code,
            self.success,
            *args,
            **kwargs
        )
