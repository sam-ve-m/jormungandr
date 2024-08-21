# Jormungandr
from func.src.domain.enums.response import InternalCode
from func.src.domain.exceptions.base_exceptions.exception import ServiceException
from func.src.domain.models.response.model import ResponseModel
from func.src.services.jwt.service import JwtService
from func.src.services.suitability.service import SuitabilityService

# Standards
from http import HTTPStatus

# Third party
from etria_logger import Gladsheim
from flask import request, Response
from pydantic import ValidationError


async def get_suitability_questions() -> Response:
    try:
        jwt = request.headers.get("x-thebes-answer")
        await JwtService.validate_jwt(jwt=jwt)
        result = await SuitabilityService.get_latest_questions_with_answer_options()
        response = ResponseModel(
            result=result,
            success=True,
            code=InternalCode.SUCCESS,
        ).build_http_response(status_code=HTTPStatus.OK)
        return response

    except ServiceException as err:
        Gladsheim.error(error=err, message=err.msg)
        response = ResponseModel(
            success=err.success, message=err.msg, code=err.code
        ).build_http_response(status_code=err.status_code)
        return response

    except ValidationError as err:
        Gladsheim.info(error=err)
        response = ResponseModel(
            success=False,
            message="Error trying to validate suitability data",
            code=InternalCode.VALIDATION_ERROR,
        ).build_http_response(status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except Exception as err:
        Gladsheim.error(error=err)
        response = ResponseModel(
            success=False,
            message="Unexpected error has occurred",
            code=InternalCode.INTERNAL_SERVER_ERROR,
        ).build_http_response(status_code=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response
