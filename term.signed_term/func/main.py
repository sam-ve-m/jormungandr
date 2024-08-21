from http import HTTPStatus

from etria_logger import Gladsheim
from flask import request, Request, Response
from heimdall_client import Heimdall, HeimdallStatusResponses

from func.src.domain.enums.response.code import InternalCode
from func.src.domain.exceptions.model import UnauthorizedError, FileNotFound, TermNotSigned
from func.src.domain.models.request.model import TermModel
from func.src.domain.models.response.model import ResponseModel
from func.src.services.terms.service import TermService


async def get_signed_term(request: Request = request) -> Response:
    raw_params = request.args.to_dict()
    x_thebes_answer = request.headers.get("x-thebes-answer")

    try:
        jwt_content, heimdall_status = await Heimdall.decode_payload(
            jwt=x_thebes_answer
        )
        if heimdall_status != HeimdallStatusResponses.SUCCESS:
            raise UnauthorizedError()

        term_model = TermModel(**raw_params)
        unique_id = jwt_content["decoded_jwt"]["user"]["unique_id"]
        pdf_link = await TermService.get_user_signed_term_url(
            term=term_model, unique_id=unique_id
        )

        response = ResponseModel(
            result=pdf_link,
            success=True,
            code=InternalCode.SUCCESS,
            message="Success",
        ).build_http_response(status=HTTPStatus.OK)
        return response

    except ValueError as ex:
        message = "Invalid parameters"
        Gladsheim.error(error=ex, message=message)
        response = ResponseModel(
            success=False, code=InternalCode.INVALID_PARAMS, message=message
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except UnauthorizedError as ex:
        message = "JWT invalid or not supplied"
        Gladsheim.error(error=ex, message=message)
        response = ResponseModel(
            success=False,
            code=InternalCode.JWT_INVALID,
            message=message,
        ).build_http_response(status=HTTPStatus.UNAUTHORIZED)
        return response

    except FileNotFound as ex:
        message = "Term file not found"
        Gladsheim.error(error=ex, message=message)
        response = ResponseModel(
            success=True, code=InternalCode.SUCCESS, message=message
        ).build_http_response(status=HTTPStatus.OK)
        return response

    except TermNotSigned as ex:
        message = "Term not signed by the user"
        Gladsheim.error(error=ex, message=message)
        response = ResponseModel(
            success=True, code=InternalCode.SUCCESS, message=message
        ).build_http_response(status=HTTPStatus.OK)
        return response

    except Exception as ex:
        message = "Unexpected error occurred"
        Gladsheim.error(error=ex, message=message)
        response = ResponseModel(
            success=False, code=InternalCode.INTERNAL_SERVER_ERROR, message=message
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response
