# STANDARD IMPORTS
from http import HTTPStatus
import flask

# THIRD PART IMPORTS
from etria_logger import Gladsheim

# PROJECT IMPORTS
from src.domain.enums.status_code.enum import InternalCode
from src.domain.exceptions.exceptions import UserWasNotFound, NotSentToIara, NotSentToPersephone, StatusSentIsNotValid, \
    UserWasNotUpdated
from src.domain.models.response.model import ResponseModel
from src.domain.validator.webhook.validator import WebHookMessage
from src.services.web_hook.service import ExchangeAccountService


async def onboarding_ouroinvest() -> flask.Response:
    hook_request = flask.request.json
    try:
        webhook_message = WebHookMessage.from_request(request_body=hook_request)
        service_response = await ExchangeAccountService.save_exchange_account(
            webhook_message=webhook_message
        )

        response = ResponseModel(
            success=True,
            code=InternalCode.SUCCESS,
            message="SUCCESS - DATA WAS UPDATED SUCCESSFULLY",
            result=service_response
        ).build_http_response(status=HTTPStatus.OK)
        return response

    except UserWasNotFound as error:
        Gladsheim.error(error=error, message=error.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.USER_WAS_NOT_FOUND,
            message="ERROR - USER WAS NOT FOUND"
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)

        return response

    except UserWasNotUpdated as error:
        Gladsheim.error(error=error, message=error.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.USER_WAS_NOT_FOUND,
            message="ERROR - USER WAS NOT UPDATED"
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)

        return response

    except (NotSentToIara, NotSentToPersephone) as error:
        Gladsheim.error(error=error, message=error.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.INTERNAL_TRANSPORT_ERROR,
            message="ERROR ON FETCHING DATA FROM INTERN TRANSPORT:: Unable to redirect message"
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response

    except StatusSentIsNotValid as error:
        Gladsheim.error(error=error, message=error.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.STATUS_SENT_IS_NOT_A_VALID_ENUM,
            message="ERROR - STATUS SENT IS NOT A VALID ENUM"
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)
        return response

    except Exception as error:
        Gladsheim.error(error=error, message=str(error))
        response = ResponseModel(
            success=False,
            code=InternalCode.INTERNAL_SERVER_ERROR,
            message="ERROR - AN UNEXPECTED ERROR HAS OCCURRED"
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
        return response
