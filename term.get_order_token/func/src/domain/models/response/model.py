# Jormungandr
from ...enums.code import InternalCode

# Standards
from json import dumps

# Third party
from flask import Response


class ResponseModel:
    def __init__(
        self, success: bool, code: InternalCode, message: str = None, result: any = None
    ):
        self.success = success
        self.code = code
        self.message = message
        self.result = result
        self.response = self.to_dumps()

    def to_dumps(self) -> str:
        response_model = dumps(
            {
                "result": self.result,
                "message": self.message,
                "success": self.success,
                "code": self.code,
            }
        )
        self.response = response_model
        return response_model

    def build_http_response(
        self, status_code: int, mimetype: str = "application/json"
    ) -> Response:
        http_response = Response(
            self.response,
            mimetype=mimetype,
            status=status_code,
        )
        return http_response
