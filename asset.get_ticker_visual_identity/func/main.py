# Jormungandr
from src.domain.exceptions.exception import TickerNotFound
from src.services.ticker import TickerVisualIdentityService
from src.domain.enums.response import InternalCode
from src.domain.validators.validator import Ticker
from src.domain.response.model import ResponseModel

# Standards
from http import HTTPStatus

# Third party
from etria_logger import Gladsheim
from flask import request, Response


async def get_ticker_visual_identity() -> Response:
    try:
        raw_payload = request.args.to_dict()
        payload_validated = Ticker(**raw_payload)
        result = await TickerVisualIdentityService.get_ticker_url(
            payload_validated=payload_validated
        )
        response = ResponseModel(
            result=result, success=True, code=InternalCode.SUCCESS
        ).build_http_response(status=HTTPStatus.OK)
        return response

    except TickerNotFound as ex:
        result = {"url": None, "type": None}
        response = ResponseModel(
            result=result,
            success=True,
            message=ex.msg,
            code=InternalCode.DATA_NOT_FOUND,
        ).build_http_response(status=HTTPStatus.OK)
        return response

    except ValueError as ex:
        Gladsheim.error(
            ex=ex,
            message=f"Jormungandr::validator::There are invalid format"
            "or extra/missing parameters",
        )
        response = ResponseModel(
            success=False,
            code=InternalCode.INVALID_PARAMS,
            message="There are invalid format or extra/missing parameters",
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except Exception as ex:
        Gladsheim.error(
            error=ex, message=f"Jormungandr::get_ticker_visual_identity::{str(ex)}"
        )
        response = ResponseModel(
            success=False,
            code=InternalCode.INTERNAL_SERVER_ERROR,
            message="Unexpected error occurred",
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response
