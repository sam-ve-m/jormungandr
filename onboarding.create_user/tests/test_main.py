import logging.config
from http import HTTPStatus
from unittest.mock import patch, MagicMock

import flask
import pytest
from decouple import RepositoryEnv, Config

from func.src.transports.device_info.transport import DeviceSecurity

with patch.object(RepositoryEnv, "__init__", return_value=None):
    with patch.object(Config, "__init__", return_value=None):
        with patch.object(Config, "__call__"):
            with patch.object(logging.config, "dictConfig"):
                from etria_logger import Gladsheim
                from func.main import (
                    create_user,
                    InvalidEmail,
                    EmailAlreadyExists,
                    ErrorOnSendAuditLog,
                    ErrorOnSendIaraMessage,
                    DeviceInfoRequestFailed,
                    DeviceInfoNotSupplied,
                )
                from func.src.domain.enums.response.code import InternalCode
                from func.src.domain.response.model import ResponseModel
                from func.src.domain.validators.validator import UserParams
                from func.src.services.user_register import UserService


invalid_email_case = (
    InvalidEmail(),
    "Validator::validate_email::Invalid email format",
    InternalCode.INVALID_PARAMS,
    InvalidEmail.msg,
    HTTPStatus.BAD_REQUEST,
)
duplicated_email_case = (
    EmailAlreadyExists(),
    "UserService::verify_email_already_exists:: Email already exists",
    InternalCode.DATA_ALREADY_EXISTS,
    EmailAlreadyExists.msg,
    HTTPStatus.BAD_REQUEST,
)
persephone_case = (
    ErrorOnSendAuditLog(),
    "Audit::register_user_log::Error on trying to register log",
    InternalCode.PARTNERS_ERROR,
    "Audit::register_user_log::Error on trying to register log",
    HTTPStatus.INTERNAL_SERVER_ERROR,
)
iara_case = (
    ErrorOnSendIaraMessage(),
    "Audit::register_user_log::Error on trying to register log",
    InternalCode.PARTNERS_ERROR,
    "Audit::register_user_log::Error on trying to register log",
    HTTPStatus.INTERNAL_SERVER_ERROR,
)
device_info_request_case = (
    DeviceInfoRequestFailed(),
    "Error trying to get device info",
    InternalCode.INTERNAL_SERVER_ERROR,
    "Error trying to get device info",
    HTTPStatus.INTERNAL_SERVER_ERROR,
)
no_device_info_case = (
    DeviceInfoNotSupplied(),
    "Device info not supplied",
    InternalCode.INVALID_PARAMS,
    "Device info not supplied",
    HTTPStatus.BAD_REQUEST,
)
value_exception_case = (
    ValueError("dummy"),
    "dummy",
    InternalCode.INVALID_PARAMS,
    "Invalid params",
    HTTPStatus.BAD_REQUEST,
)
exception_case = (
    Exception("dummy"),
    "dummy",
    InternalCode.INTERNAL_SERVER_ERROR,
    "Unexpected error occurred",
    HTTPStatus.INTERNAL_SERVER_ERROR,
)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "exception,error_message,internal_status_code,response_message,response_status_code",
    [
        invalid_email_case,
        duplicated_email_case,
        persephone_case,
        iara_case,
        value_exception_case,
        exception_case,
        device_info_request_case,
        no_device_info_case,
    ],
)
@patch.object(UserParams, "__init__", return_value=None)
@patch.object(UserService, "__init__", return_value=None)
@patch.object(UserService, "verify_email_already_exists")
@patch.object(UserService, "register")
@patch.object(Gladsheim, "error")
@patch.object(ResponseModel, "__init__", return_value=None)
@patch.object(ResponseModel, "build_http_response")
@patch.object(DeviceSecurity, "get_device_info")
async def test_create_user_raising_errors(
    device_info,
    mocked_build_response,
    mocked_response_instance,
    mocked_logger,
    mocked_register,
    mocked_validation,
    mocked_service,
    mocked_model,
    monkeypatch,
    exception,
    error_message,
    internal_status_code,
    response_message,
    response_status_code,
):
    monkeypatch.setattr(flask, "request", MagicMock())
    mocked_service.side_effect = exception
    await create_user()
    mocked_register.assert_not_called()
    mocked_validation.assert_not_called()
    mocked_logger.assert_called_once_with(error=exception, message=error_message)
    mocked_response_instance.assert_called_once_with(
        success=False, code=internal_status_code.value, message=response_message
    )
    mocked_build_response.assert_called_once_with(status=response_status_code)


dummy_response = "response"


@pytest.mark.asyncio
@patch.object(UserParams, "__init__", return_value=None)
@patch.object(UserService, "__init__", return_value=None)
@patch.object(UserService, "verify_email_already_exists")
@patch.object(UserService, "register", return_value=dummy_response)
@patch.object(Gladsheim, "error")
@patch.object(ResponseModel, "__init__", return_value=None)
@patch.object(ResponseModel, "build_http_response", return_value=dummy_response)
@patch.object(DeviceSecurity, "get_device_info")
async def test_create_user(
    device_info,
    mocked_build_response,
    mocked_response_instance,
    mocked_logger,
    mocked_register,
    mocked_validation,
    mocked_service,
    mocked_model,
    monkeypatch,
):
    monkeypatch.setattr(flask, "request", MagicMock())
    response = await create_user()
    mocked_service.assert_called()
    mocked_register.assert_called()
    mocked_validation.assert_called()
    mocked_logger.assert_not_called()
    mocked_response_instance.assert_called_once_with(
        success=dummy_response,
        code=InternalCode.SUCCESS.value,
        message="User successfully created",
    )
    mocked_build_response.assert_called_once_with(status=HTTPStatus.OK)
    assert dummy_response == response
