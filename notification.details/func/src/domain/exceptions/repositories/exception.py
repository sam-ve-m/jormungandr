# Jormungandr - Notifications
from ..base.base_exceptions import RepositoryException
from ...enums.response.code import InternalCode

# Standards
from http import HTTPStatus


class ErrorOnUpdateUserNotifications(RepositoryException):
    def __init__(self, *args, **kwargs):
        self.msg = "Error on trying to update user notifications"
        self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        self.internal_code = InternalCode.DATA_NOT_FOUND
        self.success = False
        super().__init__(
            self.msg,
            self.status_code,
            self.internal_code,
            self.success,
            *args,
            **kwargs
        )
