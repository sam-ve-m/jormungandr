from http import HTTPStatus

from etria_logger import Gladsheim
from flask import request

from func.src.domain.enums.code import InternalCode
from func.src.domain.exceptions.exceptions import (
    ErrorOnSendAuditLog,
    ErrorOnUpdateUser,
    ErrorOnDecodeJwt,
    UserUniqueIdNotExists,
    TermVersionNotExists,
    DeviceInfoRequestFailed,
    DeviceInfoNotSupplied,
)
from func.src.domain.response.model import ResponseModel
from func.src.domain.validators.validator import TermFiles
from func.src.services.jwt import JwtService
from func.src.services.terms import TermSignService
from func.src.transports.device_info.transport import DeviceSecurity


async def terms_sign():
    msg_error = "Unexpected error occurred"
    try:
        raw_terms_type = request.json
        x_thebes_answer = request.headers.get("x-thebes-answer")
        x_device_info = request.headers.get("x-device-info")

        terms_type_validated = TermFiles(**raw_terms_type)
        unique_id = await JwtService.decode_jwt_and_get_unique_id(jwt=x_thebes_answer)
        device_info = await DeviceSecurity.get_device_info(x_device_info)

        terms_service = TermSignService(
            unique_id=unique_id,
            terms_type_validated=terms_type_validated,
            device_info=device_info,
        )
        success = await terms_service.user_terms_sign()
        response = ResponseModel(
            success=success,
            message="Terms signed successfully",
            code=InternalCode.SUCCESS,
        ).build_http_response(status=HTTPStatus.OK)
        return response

    except ErrorOnDecodeJwt as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False, code=InternalCode.JWT_INVALID, message="Unauthorized token"
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except UserUniqueIdNotExists as ex:
        Gladsheim.info(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False, code=InternalCode.DATA_NOT_FOUND, message=msg_error
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except ErrorOnUpdateUser as ex:
        Gladsheim.info(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False, code=InternalCode.INTERNAL_SERVER_ERROR, message=msg_error
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except TermVersionNotExists as ex:
        Gladsheim.info(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False, code=InternalCode.DATA_NOT_FOUND, message=msg_error
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except ErrorOnSendAuditLog as ex:
        Gladsheim.info(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False, code=InternalCode.INTERNAL_SERVER_ERROR, message=msg_error
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except DeviceInfoRequestFailed as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.INTERNAL_SERVER_ERROR,
            message="Error trying to get device info",
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except DeviceInfoNotSupplied as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.INVALID_PARAMS,
            message="Device info not supplied",
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except ValueError as ex:
        Gladsheim.info(error=ex)
        response = ResponseModel(
            success=False,
            code=InternalCode.INVALID_PARAMS,
            message="Invalid term type or format type",
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except Exception as ex:
        Gladsheim.error(error=ex)
        response = ResponseModel(
            success=False, code=InternalCode.INTERNAL_SERVER_ERROR, message=msg_error
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response
