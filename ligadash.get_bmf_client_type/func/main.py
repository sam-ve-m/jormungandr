from http import HTTPStatus

from etria_logger import Gladsheim
from flask import request, Response, Request

from func.src.domain.response.model import ResponseModel
from func.src.domain.response.status_code.enums import StatusCode
from func.src.service.bmf_client_enum.service import BmfClientEnumService


async def get_enums(request_: Request = request) -> Response:
    try:
        service_response = BmfClientEnumService.get_response()
        response = ResponseModel.build_http_response(
            response_model=service_response, status=HTTPStatus.OK
        )
        return response

    except TypeError as error:
        Gladsheim.error(error=error, message="Data not found or inconsistent.")
        response = ResponseModel.build_http_response(
            response_model=ResponseModel.build_response(
                success=False,
                code=StatusCode.DATA_NOT_FOUND,
                message="Data not found or inconsistent.",
                result=[],
            ),
            status=HTTPStatus.NOT_FOUND,
        )
        return response

    except Exception as error:
        Gladsheim.error(error=error, message="Error trying to get the enum.")
        response = ResponseModel.build_http_response(
            response_model=ResponseModel.build_response(
                success=False,
                code=StatusCode.DATA_NOT_FOUND,
                message="Error trying to get the enum.",
                result=[],
            ),
            status=HTTPStatus.INTERNAL_SERVER_ERROR,
        )
        return response
