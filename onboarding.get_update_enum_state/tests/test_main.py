from unittest.mock import patch

from flask import Flask
import pytest
from func.main import get_enums
from func.src.repository.state_enum.repository import StateEnumRepository
from tests.test_doubles.doubles import (
    main_service_response_dummy,
    enum_service_get_enums_response_none,
    enum_service_response_none,
    enum_service_response_invalid,
    enum_service_get_enums_response_ok,
    enum_service_response_ok,
    enum_service_response_bad_request,
)

service_response_dummy = main_service_response_dummy


@pytest.mark.asyncio
@patch.object(StateEnumRepository, "get_state_enum")
async def test_response_when_is_all_ok(get_enums_mock):
    get_enums_mock.return_value = enum_service_get_enums_response_ok
    app = Flask(__name__)
    with app.test_request_context("?country=BRA").request as request:
        response = await get_enums(request_=request)
        assert response.data == enum_service_response_ok.encode()


@pytest.mark.asyncio
@patch.object(StateEnumRepository, "get_state_enum")
async def test_get_response_when_enums_are_none(get_enums_mock):
    get_enums_mock.return_value = enum_service_get_enums_response_none
    app = Flask(__name__)
    with app.test_request_context("?country=BRA").request as request:
        response = await get_enums(request_=request)
        assert response.data == enum_service_response_none.encode()


@pytest.mark.asyncio
@patch.object(StateEnumRepository, "get_state_enum")
async def test_get_response_when_enums_are_invalid(get_enums_mock):
    get_enums_mock.side_effect = Exception("Erroooooou!")
    app = Flask(__name__)
    with app.test_request_context("?country=BRA").request as request:
        response = await get_enums(request_=request)
        assert response.data == enum_service_response_invalid.encode()


@pytest.mark.asyncio
@patch.object(StateEnumRepository, "get_state_enum")
async def test_get_response_when_bad_parameters(get_enums_mock):
    get_enums_mock.side_effect = ValueError("Bad Parameters")
    app = Flask(__name__)
    with app.test_request_context("?country=BRA").request as request:
        response = await get_enums(request_=request)
        assert response.data == enum_service_response_bad_request.encode()
