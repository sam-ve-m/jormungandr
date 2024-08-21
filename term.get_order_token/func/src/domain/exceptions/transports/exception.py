# Jormungandr
from ..base.base_exceptions import TransportException
from ...enums.code import InternalCode

# Standards
from http import HTTPStatus


class SignTermStatusCodeNotOk(TransportException):
    def __init__(self, *args, **kwargs):
        self.msg = "Error when trying to sign a term"
        self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        self.internal_code = InternalCode.TERM_SIGN_REQUEST_FAILURE
        self.success = False
        super().__init__(
            self.msg,
            self.status_code,
            self.internal_code,
            self.success,
            *args,
            **kwargs
        )
