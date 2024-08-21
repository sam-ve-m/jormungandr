class InvalidJwtToken(Exception):
    msg = "Failed to validate user credentials"


class UserNotFound(Exception):
    msg = "Failed to get user data"


