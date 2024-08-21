from http import HTTPStatus

from etria_logger import Gladsheim

from func.src.domain.enums.status_code.enum import InternalCode
from func.src.domain.exceptions.exceptions import FailToFetchData
from func.src.domain.models.response.model import ResponseModel
from func.src.services.employ_position.service import EmployPositionService
import flask


async def get_employ_positions() -> flask.Response:
    try:
        service_response = EmployPositionService.get_employ_position_response()
        response = ResponseModel(
            success=True,
            code=InternalCode.SUCCESS,
            message="SUCCESS",
            result=service_response
        ).build_http_response(status=HTTPStatus.OK)
        return response

    except FailToFetchData as error:
        Gladsheim.error(error=error, message=error.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.INTERNAL_SERVER_ERROR,
            message="Not able to get or save data in database"
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except Exception as error:
        Gladsheim.error(error=error, message=str(error))
        response = ResponseModel(
            success=False,
            code=InternalCode.INTERNAL_SERVER_ERROR,
            message="Something went wrong"
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response
