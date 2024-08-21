from http import HTTPStatus

from etria_logger import Gladsheim
from flask import request, Response
from khonshu import CustomerAnswers
from pydantic import ValidationError

from func.src.transports.device_info.transport import DeviceSecurity
from func.src.domain.exceptions.base.base_exceptions import (
    ServiceException,
    RepositoryException,
    TransportException,
    DomainException,
    InternalCode,
)
from func.src.domain.response.model import ResponseModel
from func.src.services.jwt import JwtService
from func.src.services.suitability import SuitabilityService


async def update_suitability_profile() -> Response:
    try:
        jwt = request.headers.get("x-thebes-answer")
        encoded_device_info = request.headers.get("x-device-info")
        raw_customer_answers = request.json

        customer_answers_validated = CustomerAnswers(**raw_customer_answers)
        unique_id = await JwtService.decode_jwt_and_get_unique_id(jwt=jwt)
        device_info = await DeviceSecurity.get_device_info(encoded_device_info)
        await SuitabilityService.check_if_able_to_update(jwt=jwt)

        success = await SuitabilityService.set_in_customer(
            unique_id=unique_id,
            customer_answers=customer_answers_validated,
            device_info=device_info,
        )

        response = ResponseModel(
            success=success,
            message="Suitability score and profile created successfully",
            code=InternalCode.SUCCESS,
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

    except TransportException as err:
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

    except ValidationError as err:
        Gladsheim.error(error=err)
        response = ResponseModel(
            success=False,
            message="Invalid customer answers format",
            code=InternalCode.INVALID_PARAMS,
        ).build_http_response(status_code=HTTPStatus.BAD_REQUEST)
        return response

    except Exception as ex:
        Gladsheim.error(error=ex)
        response = ResponseModel(
            success=False,
            code=InternalCode.INTERNAL_SERVER_ERROR,
            message="Unexpected error has occurred",
        ).build_http_response(status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response
