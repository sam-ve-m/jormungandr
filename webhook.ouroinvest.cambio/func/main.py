# STANDARD IMPORTS
from http import HTTPStatus
from flask import request, Response, Request

# THIRD PART IMPORTS
from etria_logger import Gladsheim

from func.src.domain.enums.status_code.enum import InternalCode
from func.src.domain.models.response.model import ResponseModel


async def exchange_ouroinvest(
        request_body: Request = request
) -> Response:

    # hook_request = request_body.json

    try:
        response = 0

        response = ResponseModel(
            success=True,
            code=InternalCode.SUCCESS,
            message="SUCCESS - DATA WAS UPDATED SUCCESSFULLY",
            result=response
        ).build_http_response(status=HTTPStatus.OK)
        return response

    except Exception as error:
        Gladsheim.error(error=error)
        response = ResponseModel(
            result=False,
            success=False,
            code=InternalCode.INTERNAL_SERVER_ERROR,
            message="ERROR - AN UNEXPECTED ERROR HAS OCCURRED"
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response
