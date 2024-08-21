# Jormungandr - Notifications
from ..base.base_exceptions import DomainException
from ...enums.response.code import InternalCode

# Standards
from http import HTTPStatus


class InconsistentNotification(DomainException):
    def __init__(self, *args, **kwargs):
        self.msg = "Inconsistent notification, missing or incorrect data"
        self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        self.internal_code = InternalCode.DATA_VALIDATION_ERROR
        self.success = False
        super().__init__(
            self.msg,
            self.status_code,
            self.internal_code,
            self.success,
            *args,
            **kwargs
        )
