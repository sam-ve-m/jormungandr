from json import dumps

from flask import Response

from func.src.domain.response.status_code.enums import StatusCode


class ResponseModel:
    @staticmethod
    def build_response(
        success: bool, code: StatusCode, message: str = None, result: any = None
    ) -> str:
        response_model = dumps(
            {
                "result": result,
                "message": message,
                "success": success,
                "code": code.value,
            }
        )
        return response_model

    @staticmethod
    def build_http_response(
        response_model: str, status: int, mimetype: str = "application/json"
    ) -> Response:
        response = Response(
            response_model,
            mimetype=mimetype,
            status=status,
        )
        return response
