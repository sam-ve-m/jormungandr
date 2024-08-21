from http import HTTPStatus

from ..base.base_exceptions import TransportException
from ...enums.code import InternalCode


class ErrorOnSendAuditLog(TransportException):
    def __init__(self, *args, **kwargs):
        self.msg = "Error when trying to send audit log to Persephone"
        self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        self.internal_code = InternalCode.ERROR_SENDING_TO_PERSEPHONE
        self.success = False
        super().__init__(
            self.msg,
            self.status_code,
            self.internal_code,
            self.success,
            *args,
            **kwargs
        )


class OnboardingStepsStatusCodeNotOk(TransportException):
    def __init__(self, *args, **kwargs):
        self.msg = "Error when trying to get customer onboarding steps"
        self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        self.internal_code = InternalCode.ONBOARDING_STEP_REQUEST_FAILURE
        self.success = False
        super().__init__(
            self.msg,
            self.status_code,
            self.internal_code,
            self.success,
            *args,
            **kwargs
        )


class InvalidOnboardingCurrentStep(TransportException):
    def __init__(self, *args, **kwargs):
        self.msg = "Customer is not in the create suitability step"
        self.status_code = HTTPStatus.UNAUTHORIZED
        self.internal_code = InternalCode.ONBOARDING_STEP_INCORRECT
        self.success = False
        super().__init__(
            self.msg,
            self.status_code,
            self.internal_code,
            self.success,
            *args,
            **kwargs
        )


class NotAuthorizedToUpdate(TransportException):
    def __init__(self, *args, **kwargs):
        self.msg = "Customer is not able to update suitability profile"
        self.status_code = HTTPStatus.UNAUTHORIZED
        self.internal_code = InternalCode.ONBOARDING_NOT_FINISHED
        self.success = False
        super().__init__(
            self.msg,
            self.status_code,
            self.internal_code,
            self.success,
            *args,
            **kwargs
        )


class DeviceInfoRequestFailed(TransportException):
    def __init__(self, *args, **kwargs):
        self.msg = "Error trying to get device info"
        self.status_code = HTTPStatus.INTERNAL_SERVER_ERROR
        self.internal_code = InternalCode.API_ERROR
        self.success = False
        super().__init__(
            self.msg,
            self.status_code,
            self.internal_code,
            self.success,
            *args,
            **kwargs
        )


class DeviceInfoNotSupplied(TransportException):
    def __init__(self, *args, **kwargs):
        self.msg = "Device info not supplied"
        self.status_code = HTTPStatus.BAD_REQUEST
        self.internal_code = InternalCode.INVALID_PARAMS
        self.success = False
        super().__init__(
            self.msg,
            self.status_code,
            self.internal_code,
            self.success,
            *args,
            **kwargs
        )
