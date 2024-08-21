# PROJECT IMPORTS
from http import HTTPStatus

import flask
import pytest
from unittest.mock import patch, MagicMock

from decouple import RepositoryEnv, Config
import logging.config

from src.domain.validator.webhook.validator import WebHookMessage

with patch.object(RepositoryEnv, "__init__", return_value=None):
    with patch.object(Config, "__init__", return_value=None):
        with patch.object(Config, "__call__"):
            with patch.object(logging.config, "dictConfig"):
                from etria_logger import Gladsheim
                from main import onboarding_ouroinvest
                from src.domain.enums.status_code.enum import InternalCode
                from src.domain.models.response.model import ResponseModel
                from src.domain.exceptions.exceptions import UserWasNotFound, StatusSentIsNotValid, UserWasNotUpdated, \
                    NotSentToIara
                from src.services.web_hook.service import ExchangeAccountService


user_was_not_found_case = (
    UserWasNotFound(),
    UserWasNotFound.msg,
    InternalCode.USER_WAS_NOT_FOUND,
    "ERROR - USER WAS NOT FOUND",
    HTTPStatus.INTERNAL_SERVER_ERROR
)
user_was_not_updated_case = (
    UserWasNotUpdated(),
    UserWasNotUpdated.msg,
    InternalCode.USER_WAS_NOT_FOUND,
    "ERROR - USER WAS NOT UPDATED",
    HTTPStatus.INTERNAL_SERVER_ERROR
)
status_sent_is_not_valid_case = (
    StatusSentIsNotValid(),
    StatusSentIsNotValid.msg,
    InternalCode.STATUS_SENT_IS_NOT_A_VALID_ENUM,
    "ERROR - STATUS SENT IS NOT A VALID ENUM",
    HTTPStatus.BAD_REQUEST
)
status_unable_to_redirect_message = (
    NotSentToIara(),
    NotSentToIara.msg,
    InternalCode.INTERNAL_TRANSPORT_ERROR,
    "ERROR ON FETCHING DATA FROM INTERN TRANSPORT:: Unable to redirect message",
    HTTPStatus.INTERNAL_SERVER_ERROR
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
    user_was_not_found_case,
    user_was_not_updated_case,
    status_sent_is_not_valid_case,
    status_unable_to_redirect_message,
    exception_case,
])
@patch.object(WebHookMessage, "from_request")
@patch.object(ExchangeAccountService, "save_exchange_account")
@patch.object(Gladsheim, "error")
@patch.object(ResponseModel, "__init__", return_value=None)
@patch.object(ResponseModel, "build_http_response")
async def test_onboarding_ouroinvest_raising_errors(
            mocked_build_response, mocked_response_instance,
            mocked_logger, mocked_service, mocked_model, monkeypatch,
            exception, error_message, internal_status_code, response_message, response_status_code,
):
    monkeypatch.setattr(flask, "request", MagicMock())
    mocked_model.side_effect = exception
    await onboarding_ouroinvest()
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
@patch.object(ExchangeAccountService, "save_exchange_account", return_value=dummy_response)
@patch.object(Gladsheim, "error")
@patch.object(ResponseModel, "__init__", return_value=None)
@patch.object(ResponseModel, "build_http_response", return_value=dummy_response)
async def test_onboarding_ouroinvest(
            mocked_build_response, mocked_response_instance, mocked_logger, mocked_service, mocked_model, monkeypatch,
):
    monkeypatch.setattr(flask, "request", MagicMock())
    response = await onboarding_ouroinvest()
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
