# PROJECT IMPORTS
from http import HTTPStatus

import flask
import pytest
from unittest.mock import patch, MagicMock

from decouple import RepositoryEnv, Config
import logging.config


with patch.object(RepositoryEnv, "__init__", return_value=None):
    with patch.object(Config, "__init__", return_value=None):
        with patch.object(Config, "__call__"):
            with patch.object(logging.config, "dictConfig"):
                from etria_logger import Gladsheim
                from func.main import caf_transaction
                from func.src.domain.enums.status_code.enum import InternalCode
                from func.src.domain.models.response.model import ResponseModel
                from func.src.domain.exceptions.exceptions import UserWasNotUpdated, TransactionNotFound, \
    ErrorSendingToIaraDatailCpfValidation, InvalidStatusReceived
                from func.src.services.web_hook.service import BureauValidationService
                from func.src.domain.validator.webhook.validator import WebHookMessage

user_was_not_updated_case = (
    UserWasNotUpdated(),
    UserWasNotUpdated.msg,
    InternalCode.UNABLE_TO_UPDATE_IN_MONGO,
    "UNABLE TO UPDATE IN MONGO",
    HTTPStatus.INTERNAL_SERVER_ERROR
)
transaction_not_found_case = (
    TransactionNotFound(),
    TransactionNotFound.msg,
    InternalCode.UNABLE_TO_UPDATE_IN_MONGO,
    "UNABLE TO FIND TRANSACTION REGISTERS",
    HTTPStatus.INTERNAL_SERVER_ERROR
)
error_sending_to_iara_datail_cpf_validation_case = (
    ErrorSendingToIaraDatailCpfValidation(),
    ErrorSendingToIaraDatailCpfValidation.msg.format(""),
    InternalCode.INTERNAL_TRANSPORT_ERROR,
    "UNABLE TO INTERNALLY REDIRECT MESSAGE",
    HTTPStatus.INTERNAL_SERVER_ERROR
)
invalid_status_received_case = (
    InvalidStatusReceived(),
    InvalidStatusReceived.msg.format(""),
    InternalCode.FIELD_RECEIVED_IS_NOT_A_VALID_ENUM,
    "ERROR - FIELD RECEIVED IS NOT A VALID ENUM",
    HTTPStatus.BAD_REQUEST
)
exception_case = (
    Exception("dummy"),
    "dummy",
    InternalCode.INTERNAL_SERVER_ERROR,
    "ERROR - AN UNEXPECTED ERROR HAS OCCURRED",
    HTTPStatus.INTERNAL_SERVER_ERROR
)


@pytest.mark.asyncio
@pytest.mark.parametrize("exception,error_message,internal_status_code,response_message,response_status_code", [
    error_sending_to_iara_datail_cpf_validation_case,
    invalid_status_received_case,
    transaction_not_found_case,
    user_was_not_updated_case,
    exception_case,
])
@patch.object(WebHookMessage, "from_request")
@patch.object(BureauValidationService, "save_bureau_validation")
@patch.object(Gladsheim, "error")
@patch.object(ResponseModel, "__init__", return_value=None)
@patch.object(ResponseModel, "build_http_response")
async def test_caf_transaction_raising_errors(
            mocked_build_response, mocked_response_instance,
            mocked_logger, mocked_service, mocked_model, monkeypatch,
            exception, error_message, internal_status_code, response_message, response_status_code,
):
    monkeypatch.setattr(flask, "request", MagicMock())
    mocked_model.side_effect = exception
    await caf_transaction()
    mocked_service.assert_not_called()
    mocked_logger.assert_called_once_with(error=exception, message=error_message)
    mocked_response_instance.assert_called_once_with(
        success=False,
        code=internal_status_code,
        message=response_message
    )
    mocked_build_response.assert_called_once_with(status=response_status_code)


dummy_response = "response"


@pytest.mark.asyncio
@patch.object(WebHookMessage, "from_request")
@patch.object(BureauValidationService, "save_bureau_validation", return_value=dummy_response)
@patch.object(Gladsheim, "error")
@patch.object(ResponseModel, "__init__", return_value=None)
@patch.object(ResponseModel, "build_http_response", return_value=dummy_response)
async def test_caf_transaction(
            mocked_build_response, mocked_response_instance, mocked_logger, mocked_service, mocked_model, monkeypatch,
):
    monkeypatch.setattr(flask, "request", MagicMock())
    response = await caf_transaction()
    mocked_service.assert_called()
    mocked_logger.assert_not_called()
    mocked_response_instance.assert_called_once_with(
        success=True,
        code=InternalCode.SUCCESS,
        message="SUCCESS - DATA WAS UPDATED SUCCESSFULLY",
        result=dummy_response
    )
    mocked_build_response.assert_called_once_with(status=HTTPStatus.OK)
    assert dummy_response == response
