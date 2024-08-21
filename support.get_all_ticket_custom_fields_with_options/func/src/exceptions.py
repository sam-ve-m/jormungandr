class ErrorToRequestZendeskApi(Exception):
    def __init__(self):
        self.msg = "Failed to request ticket custom fields."


class InvalidEndpointZendeskApi(Exception):
    def __init__(self):
        self.msg = "Failed to request ticket custom fields."
