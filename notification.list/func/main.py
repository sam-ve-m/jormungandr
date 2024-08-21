# Jormungandr - Notifications
from func.src.domain.response.model import ResponseModel
from func.src.domain.enums.response.code import InternalCode
from func.src.services.jwt.service import JwtService
from func.src.services.notifications.service import NotificationService
from func.src.domain.exceptions.base.base_exceptions import (
    ServiceException,
    DomainException,
    RepositoryException,
)

# Standards
from http import HTTPStatus

# Third party
from etria_logger import Gladsheim
from flask import Response, request


async def get_all_notifications() -> Response:
    try:
        jwt = request.headers.get("x-thebes-answer")
        unique_id = await JwtService.decode_jwt_and_get_unique_id(jwt=jwt)
        result = await NotificationService.get_all(unique_id=unique_id)
        response = ResponseModel(
            success=True, result=result, code=InternalCode.SUCCESS
        ).build_http_response(status_code=HTTPStatus.OK)
        return response

    except ServiceException as err:
        Gladsheim.error(error=err, message=err.msg)
        response = ResponseModel(
            success=err.success, message=err.msg, code=err.code
        ).build_http_response(status_code=err.status_code)
        return response

    except DomainException as err:
        Gladsheim.error(error=err, message=err.msg)
        response = ResponseModel(
            success=err.success, message=err.msg, code=err.code
        ).build_http_response(status_code=err.status_code)
        return response

    except RepositoryException as err:
        Gladsheim.error(error=err, message=err.msg)
        response = ResponseModel(
            success=err.success, message=err.msg, code=err.code
        ).build_http_response(status_code=err.status_code)
        return response

    except Exception as ex:
        Gladsheim.error(error=ex)
        response = ResponseModel(
            success=False,
            message="Unexpected error has occurred",
            code=InternalCode.INTERNAL_SERVER_ERROR,
        ).build_http_response(status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response
