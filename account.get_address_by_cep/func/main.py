from func.src.domain.exceptions.exceptions import ErrorRequestingEnum, CityEnumNotFound, StateEnumNotFound
from func.src.domain.response.model import ResponseModel
from func.src.domain.enums.code import InternalCode
from func.src.domain.validator.cep import Cep

from http import HTTPStatus

from etria_logger import Gladsheim
import flask

from func.src.services.address import AddressService


async def get_address() -> flask.Response:
    try:
        body = flask.request.args.to_dict()
        cep = Cep(**body)
        result = await AddressService.get_address(cep)
        response = ResponseModel(
            result=result, success=True, code=InternalCode.SUCCESS, message="Address find successfully"
        ).build_http_response(status=HTTPStatus.OK)
        return response

    except StateEnumNotFound as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False, code=InternalCode.INVALID_PARAMS, message="Unable to find state enum"
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except CityEnumNotFound as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False, code=InternalCode.INVALID_PARAMS, message="Unable to find city enum"
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except ErrorRequestingEnum as ex:
        Gladsheim.error(error=ex, message=ex.msg)
        response = ResponseModel(
            success=False, code=InternalCode.INTERNAL_SERVER_ERROR, message="Unable to get enums"
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except ValueError as ex:
        Gladsheim.error(error=ex, message=str(ex))
        response = ResponseModel(
            success=False, code=InternalCode.INVALID_PARAMS, message="Invalid params"
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except Exception as ex:
        Gladsheim.error(error=ex, message=str(ex))
        response = ResponseModel(
            success=False,
            code=InternalCode.INTERNAL_SERVER_ERROR,
            message="Unexpected error occurred",
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response
