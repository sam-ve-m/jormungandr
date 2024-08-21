class InvalidEmail(Exception):
    msg = "Invalid email address"


class EmailAlreadyExists(Exception):
    msg = "Email already exists"


class ErrorOnSendAuditLog(Exception):
    msg = "Error when trying to send log audit on Persephone"


class ErrorOnSendIaraMessage(Exception):
    msg = "Jormungandr-Onboarding::send_to_email_verification_queue::Error when trying send message to Iara"


class DeviceInfoRequestFailed(Exception):
    msg = "Error trying to get device info"


class DeviceInfoNotSupplied(Exception):
    msg = "Device info not supplied"
