# PROJECT IMPORTS
import logging.config
from http import HTTPStatus
from unittest.mock import MagicMock
from unittest.mock import patch

import flask
import pytest
from decouple import RepositoryEnv, Config

with patch.object(RepositoryEnv, "__init__", return_value=None):
    with patch.object(Config, "__init__", return_value=None):
        with patch.object(Config, "__call__"):
            with patch.object(logging.config, "dictConfig"):
                from etria_logger import Gladsheim
                from func.main import get_employ_positions
                from func.src.domain.enums.status_code.enum import InternalCode
                from func.src.domain.models.response.model import ResponseModel
                from func.src.domain.exceptions.exceptions import FailToFetchData
                from func.src.services.employ_position.service import EmployPositionService


fail_to_fetch_data_case = (
    FailToFetchData(),
    FailToFetchData.msg,
    InternalCode.INTERNAL_SERVER_ERROR,
    "Not able to get or save data in database",
    HTTPStatus.INTERNAL_SERVER_ERROR
)
exception_case = (
    Exception("dummy"),
    "dummy",
    InternalCode.INTERNAL_SERVER_ERROR,
    "Something went wrong",
    HTTPStatus.INTERNAL_SERVER_ERROR
)


@pytest.mark.asyncio
@pytest.mark.parametrize("exception,error_message,internal_status_code,response_message,response_status_code", [
    fail_to_fetch_data_case,
    exception_case,
])
@patch.object(EmployPositionService, "get_employ_position_response")
@patch.object(Gladsheim, "error")
@patch.object(ResponseModel, "__init__", return_value=None)
@patch.object(ResponseModel, "build_http_response")
async def test_get_employ_position_raising_errors(
            mocked_build_response, mocked_response_instance,
            mocked_logger, mocked_service, monkeypatch,
            exception, error_message, internal_status_code, response_message, response_status_code,
):
    monkeypatch.setattr(flask, "request", MagicMock())
    mocked_service.side_effect = exception
    await get_employ_positions()
    mocked_logger.assert_called_once_with(error=exception, message=error_message)
    mocked_response_instance.assert_called_once_with(
        success=False,
        code=internal_status_code.value,
        message=response_message
    )
    mocked_build_response.assert_called_once_with(status=response_status_code)


dummy_response = "response"


@pytest.mark.asyncio
@patch.object(EmployPositionService, "get_employ_position_response", return_value=dummy_response)
@patch.object(Gladsheim, "error")
@patch.object(ResponseModel, "__init__", return_value=None)
@patch.object(ResponseModel, "build_http_response", return_value=dummy_response)
async def test_get_employ_position(
        mocked_build_response, mocked_response_instance,
        mocked_logger, mocked_service, monkeypatch,
):
    monkeypatch.setattr(flask, "request", MagicMock())
    response = await get_employ_positions()
    mocked_service.assert_called()
    mocked_logger.assert_not_called()
    mocked_response_instance.assert_called_once_with(
        result=dummy_response,
        success=True,
        code=InternalCode.SUCCESS.value,
        message='SUCCESS',
    )
    mocked_build_response.assert_called_once_with(status=HTTPStatus.OK)
    assert dummy_response == response
