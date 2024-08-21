# Jormungandr - Onboarding
from ..base.base_exceptions import RepositoryException
from ...enums.code import InternalCode

# Standards
from http import HTTPStatus


class ErrorOnUpdateUser(RepositoryException):
    def __init__(self, *args, **kwargs):
        self.msg = "Error on trying to update customer in database, or customer does not exist or invalid unique_id"
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
