class UnauthorizedError(Exception):
    pass


class InvalidStepError(Exception):
    pass


class SuitabilityRequiredError(Exception):
    pass


class InternalServerError(Exception):
    pass


class DeviceInfoRequestFailed(Exception):
    pass


class DeviceInfoNotSupplied(Exception):
    pass
