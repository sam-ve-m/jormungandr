from unittest.mock import patch

from etria_logger import Gladsheim
from flask import Flask
from pytest import mark
from werkzeug.test import Headers
from decouple import RepositoryEnv, Config
import logging.config


with patch.object(RepositoryEnv, "__init__", return_value=None):
    with patch.object(Config, "__init__", return_value=None):
        with patch.object(Config, "__call__"):
            with patch.object(logging.config, "dictConfig"):
                from func.main import get_bank_logo
                from func.src.domain.exceptions.model import ImageNotFound
                from func.src.services.bank_visual_identity.service import BankVisualIdentityService

request_ok = "?bank_code=79&type=logo"
requests_invalid = [
    "?bank_cod=79&type=logo",
    "?bank_code=a&type=logo",
    "?bank_code=-1&type=logo",
    "?bank_code=79&type=log",
]


@mark.asyncio
@patch.object(BankVisualIdentityService, "get_bank_logo")
async def test_save_symbols_when_request_is_ok(get_bank_logo_mock):
    get_bank_logo_mock.return_value = "https://www.image_link_here.com"

    app = Flask(__name__)
    with app.test_request_context(
        request_ok,
        headers=Headers({"x-thebes-answer": "test"}),
    ).request as request:

        save_symbols_result = await get_bank_logo(request)

        assert (
            save_symbols_result.data
            == b'{"result": "https://www.image_link_here.com", "message": "Success", "success": true, "code": 0}'
        )
        assert get_bank_logo_mock.called


@mark.asyncio
@patch.object(Gladsheim, "error")
@patch.object(BankVisualIdentityService, "get_bank_logo")
async def test_save_symbols_when_image_is_not_found(get_bank_logo_mock, etria_mock):
    get_bank_logo_mock.side_effect = ImageNotFound()

    app = Flask(__name__)
    with app.test_request_context(
        request_ok,
        headers=Headers({"x-thebes-answer": "test"}),
    ).request as request:

        save_symbols_result = await get_bank_logo(request)

        assert (
            save_symbols_result.data
            == b'{"result": null, "message": "Bank image not found", "success": true, "code": 0}'
        )
        assert get_bank_logo_mock.called
        etria_mock.assert_called()


@mark.asyncio
@mark.parametrize("request_json", requests_invalid)
@patch.object(Gladsheim, "error")
@patch.object(BankVisualIdentityService, "get_bank_logo")
async def test_save_symbols_when_request_is_invalid(
    get_bank_logo_mock, etria_mock, request_json
):
    get_bank_logo_mock.return_value = True

    app = Flask(__name__)
    with app.test_request_context(
        request_json,
        headers=Headers({"x-thebes-answer": "test"}),
    ).request as request:

        save_symbols_result = await get_bank_logo(request)

        assert (
            save_symbols_result.data
            == b'{"result": null, "message": "Invalid parameters", "success": false, "code": 10}'
        )
        assert not get_bank_logo_mock.called
        etria_mock.assert_called()


@mark.asyncio
@patch.object(Gladsheim, "error")
@patch.object(BankVisualIdentityService, "get_bank_logo")
async def test_save_symbols_when_generic_exception_happens(
    get_bank_logo_mock, etria_mock
):
    get_bank_logo_mock.side_effect = Exception("erro")

    app = Flask(__name__)
    with app.test_request_context(
        request_ok,
        headers=Headers({"x-thebes-answer": "test"}),
    ).request as request:

        save_symbols_result = await get_bank_logo(request)

        assert (
            save_symbols_result.data
            == b'{"result": null, "message": "Unexpected error occurred", "success": false, "code": 100}'
        )
        assert get_bank_logo_mock.called
        etria_mock.assert_called()
