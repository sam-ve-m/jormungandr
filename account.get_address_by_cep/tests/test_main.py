import logging.config
from http import HTTPStatus
from unittest.mock import patch, MagicMock

import flask
import pytest
from decouple import RepositoryEnv, Config


with patch.object(RepositoryEnv, "__init__", return_value=None):
    with patch.object(Config, "__init__", return_value=None):
        with patch.object(Config, "__call__"):
            with patch.object(logging.config, "dictConfig"):
                from func.src.domain.validator.cep import Cep
                from func.src.services.address import AddressService
                from etria_logger import Gladsheim
                from func.main import get_address
                from func.src.domain.enums.code import InternalCode
                from func.src.domain.response.model import ResponseModel
                from func.src.domain.exceptions.exceptions import (
                    ErrorRequestingEnum,
                    CityEnumNotFound,
                    StateEnumNotFound,
                )


state_enum_not_found_case = (
    StateEnumNotFound(),
    StateEnumNotFound.msg,
    InternalCode.INVALID_PARAMS,
    "Unable to find state enum",
    HTTPStatus.BAD_REQUEST,
)
city_enum_not_found_case = (
    CityEnumNotFound(),
    CityEnumNotFound.msg,
    InternalCode.INVALID_PARAMS,
    "Unable to find city enum",
    HTTPStatus.BAD_REQUEST,
)
error_requesting_enum_case = (
    ErrorRequestingEnum(),
    ErrorRequestingEnum.msg,
    InternalCode.INTERNAL_SERVER_ERROR,
    "Unable to get enums",
    HTTPStatus.INTERNAL_SERVER_ERROR,
)

value_error_case = (
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
        state_enum_not_found_case,
        city_enum_not_found_case,
        error_requesting_enum_case,
        value_error_case,
        exception_case
    ],
)
@patch.object(AddressService, "get_address")
@patch.object(Gladsheim, "error")
@patch.object(ResponseModel, "__init__", return_value=None)
@patch.object(Cep, "__init__", return_value=None)
@patch.object(ResponseModel, "build_http_response")
async def test_get_address_raising_errors(
    mocked_build_response,
    mocked_model,
    mocked_response_instance,
    mocked_logger,
    mocked_service,
    monkeypatch,
    exception,
    error_message,
    internal_status_code,
    response_message,
    response_status_code,
):
    monkeypatch.setattr(flask, "request", MagicMock())
    mocked_service.side_effect = exception
    await get_address()
    mocked_logger.assert_called_once_with(error=exception, message=error_message)
    mocked_response_instance.assert_called_once_with(
        success=False, code=internal_status_code, message=response_message
    )
    mocked_build_response.assert_called_once_with(status=response_status_code)


dummy_response = "response"


@pytest.mark.asyncio
@patch.object(Gladsheim, "error")
@patch.object(AddressService, "get_address")
@patch.object(Cep, "__init__", return_value=None)
@patch.object(ResponseModel, "__init__", return_value=None)
@patch.object(ResponseModel, "build_http_response", return_value=dummy_response)
async def test_get_address(
    mocked_build_response,
    mocked_response_instance,
    mocked_model,
    mocked_server,
    mocked_logger,
    monkeypatch,
):
    monkeypatch.setattr(flask, "request", MagicMock())
    response = await get_address()
    mocked_logger.assert_not_called()
    mocked_response_instance.assert_called_once_with(
        result=mocked_server.return_value,
        success=True,
        code=InternalCode.SUCCESS,
        message="Address find successfully",
    )
    mocked_build_response.assert_called_once_with(status=HTTPStatus.OK)
    assert dummy_response == response
