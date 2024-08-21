from http import HTTPStatus

import flask
from etria_logger import Gladsheim

from func.src.domain.enums.status_code.enum import InternalCode
from func.src.domain.exceptions.exceptions import InvalidStatusReceived, UserWasNotUpdated, InvalidMessageTypeReceived, \
    TransactionWasNotUpdated, TransactionNotFound, UniqueIdNotFound, ErrorSendingToIaraDatailCpfValidation, \
    NotSentToPersephone
from func.src.domain.models.response.model import ResponseModel
from func.src.domain.validator.webhook.validator import WebHookMessage
from func.src.services.web_hook.service import BureauValidationService


async def caf_transaction() -> flask.Response:
    hook_request = flask.request.json
    try:
        webhook_message = WebHookMessage.from_request(request_body=hook_request)
        service_response = await BureauValidationService.save_bureau_validation(
            webhook_message=webhook_message
        )

        response = ResponseModel(
            success=True,
            code=InternalCode.SUCCESS,
            message="SUCCESS - DATA WAS UPDATED SUCCESSFULLY",
            result=service_response
        ).build_http_response(status=HTTPStatus.OK)

    except (TransactionNotFound, UniqueIdNotFound) as error:
        Gladsheim.error(error=error, message=error.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.UNABLE_TO_UPDATE_IN_MONGO,
            message="UNABLE TO FIND TRANSACTION REGISTERS"
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)

    except (ErrorSendingToIaraDatailCpfValidation, NotSentToPersephone) as error:
        Gladsheim.error(error=error, message=error.msg.format(str(error)))
        response = ResponseModel(
            success=False,
            code=InternalCode.INTERNAL_TRANSPORT_ERROR,
            message="UNABLE TO INTERNALLY REDIRECT MESSAGE"
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)

    except (UserWasNotUpdated, TransactionWasNotUpdated) as error:
        Gladsheim.error(error=error, message=error.msg)
        response = ResponseModel(
            success=False,
            code=InternalCode.UNABLE_TO_UPDATE_IN_MONGO,
            message="UNABLE TO UPDATE IN MONGO"
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)

    except (InvalidStatusReceived, InvalidMessageTypeReceived) as error:
        Gladsheim.error(error=error, message=error.msg.format(str(error)))
        response = ResponseModel(
            success=False,
            code=InternalCode.FIELD_RECEIVED_IS_NOT_A_VALID_ENUM,
            message="ERROR - FIELD RECEIVED IS NOT A VALID ENUM"
        ).build_http_response(status=HTTPStatus.BAD_REQUEST)

    except Exception as error:
        Gladsheim.error(error=error, message=str(error))
        response = ResponseModel(
            success=False,
            code=InternalCode.INTERNAL_SERVER_ERROR,
            message="ERROR - AN UNEXPECTED ERROR HAS OCCURRED"
        ).build_http_response(status=HTTPStatus.INTERNAL_SERVER_ERROR)

    return response
