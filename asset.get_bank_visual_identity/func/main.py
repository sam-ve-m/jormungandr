from http import HTTPStatus

from etria_logger import Gladsheim
from flask import request, Request, Response

from func.src.domain.enums.response.code import InternalCode
from func.src.domain.exceptions.model import ImageNotFound
from func.src.domain.models.request.model import BankVisualIdentityModel
from func.src.domain.models.response.model import ResponseModel
from func.src.services.bank_visual_identity.service import BankVisualIdentityService


async def get_bank_logo(request: Request = request) -> Response:
    raw_params = request.args.to_dict()

    try:
        bank_code = BankVisualIdentityModel(**raw_params)
        bank_logo_link = await BankVisualIdentityService.get_bank_logo(
            bank_code=bank_code
        )

        response = ResponseModel(
            result=bank_logo_link,
            success=True,
            code=InternalCode.SUCCESS,
            message="Success",
        ).build_http_response(status=HTTPStatus.OK)
        return response

    except ImageNotFound as ex:
        message = "Bank image not found"
        Gladsheim.error(error=ex, message=message)
        response = ResponseModel(
            result=None, success=True, code=InternalCode.SUCCESS, message=message
        ).build_http_response(status=HTTPStatus.OK)
        return response

    except ValueError as ex:
        message = "Invalid parameters"
        Gladsheim.error(error=ex, message=message)
        response = ResponseModel(
            success=False, code=InternalCode.INVALID_PARAMS, message=message
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except Exception as ex:
        message = "Unexpected error occurred"
        Gladsheim.error(error=ex, message=message)
        response = ResponseModel(
            success=False, code=InternalCode.INTERNAL_SERVER_ERROR, message=message
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response
