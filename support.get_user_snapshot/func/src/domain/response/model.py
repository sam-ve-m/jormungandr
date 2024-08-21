# Jormungandr
from ...domain.enums import CodeResponse

# Standards
import json

# Third party
from flask import Response
from nidavellir import Sindri


class ResponseModel:
    @staticmethod
    def build_response(result: dict, code: CodeResponse) -> str:
        response_model = json.dumps(
            {
                "result": result,
                "code": code.value,
            },
            default=Sindri.resolver,
        )
        return response_model

    @staticmethod
    def build_error_response(message: str, code: CodeResponse) -> str:
        response_model = json.dumps(
            {
                "message": message,
                "code": code.value,
            },
            default=Sindri.resolver,
        )
        return response_model

    @staticmethod
    def build_http_response(response_model: str, status: int, mimetype: str = "application/json") -> Response:
        response = Response(
            response_model,
            mimetype=mimetype,
            status=status.value,
        )
        return response
