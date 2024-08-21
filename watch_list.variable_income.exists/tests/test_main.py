from unittest.mock import patch

from etria_logger import Gladsheim
from flask import Flask
from heimdall_client.bifrost import Heimdall
from heimdall_client.bifrost import HeimdallStatusResponses
from pytest import mark
from werkzeug.test import Headers

from func.main import symbol_exists
from func.src.services.watch_list import WatchListService

decoded_jwt_ok = {
    "is_payload_decoded": True,
    "decoded_jwt": {"user": {"unique_id": "test"}},
    "message": "Jwt decoded",
}
decoded_jwt_invalid = {
    "is_payload_decoded": False,
    "decoded_jwt": {"user": {"unique_id": "test_error"}},
    "message": "Jwt decoded",
}

request_ok = "?symbol=PETR4&region=BR"
requests_with_invalid_parameters = [
    "?smbol=PETR4&region=BR",
    "?symbol=PETR4&regon=BR",
    "?symbol=&region=BR",
    "?symbol=PETR4&region=PR",
    "",
]


@mark.asyncio
@patch.object(WatchListService, "symbol_exists")
@patch.object(Heimdall, "decode_payload")
async def test_symbol_exists_when_request_is_ok(
    decode_payload_mock, symbol_exists_mock
):
    decode_payload_mock.return_value = (decoded_jwt_ok, HeimdallStatusResponses.SUCCESS)
    symbol_exists_mock.return_value = {"is_symbol_in_watchlist": True}

    app = Flask(__name__)
    with app.test_request_context(
        request_ok,
        headers=Headers({"x-thebes-answer": "test"}),
    ).request as request:

        symbol_exists_result = await symbol_exists(request)

        assert (
            symbol_exists_result.data
            == b'{"result": {"is_symbol_in_watchlist": true}, "message": "Success", "success": true, "code": 0}'
        )
        assert symbol_exists_mock.called
        decode_payload_mock.assert_called_with(jwt="test")


@mark.asyncio
@patch.object(Gladsheim, "error")
@patch.object(WatchListService, "symbol_exists")
@patch.object(Heimdall, "decode_payload")
async def test_symbol_exists_when_jwt_is_invalid(
    decode_payload_mock, symbol_exists_mock, etria_mock
):
    decode_payload_mock.return_value = (
        decoded_jwt_invalid,
        HeimdallStatusResponses.INVALID_TOKEN,
    )
    symbol_exists_mock.return_value = {"is_symbol_in_watchlist": True}

    app = Flask(__name__)
    with app.test_request_context(
        request_ok,
        headers=Headers({"x-thebes-answer": "test_error"}),
    ).request as request:

        symbol_exists_result = await symbol_exists(request)

        assert (
            symbol_exists_result.data
            == b'{"result": null, "message": "JWT invalid or not supplied", "success": false, "code": 30}'
        )
        assert not symbol_exists_mock.called
        decode_payload_mock.assert_called_with(jwt="test_error")
        etria_mock.assert_called()


@mark.asyncio
@mark.parametrize("request_json", requests_with_invalid_parameters)
@patch.object(Gladsheim, "error")
@patch.object(WatchListService, "symbol_exists")
@patch.object(Heimdall, "decode_payload")
async def test_symbol_exists_when_parameters_are_invalid(
    decode_payload_mock, symbol_exists_mock, etria_mock, request_json
):
    decode_payload_mock.return_value = (decoded_jwt_ok, HeimdallStatusResponses.SUCCESS)
    symbol_exists_mock.return_value = {"is_symbol_in_watchlist": True}

    app = Flask(__name__)
    with app.test_request_context(
        request_json,
        headers=Headers({"x-thebes-answer": "test"}),
    ).request as request:

        symbol_exists_result = await symbol_exists(request)

        assert (
            symbol_exists_result.data
            == b'{"result": null, "message": "Invalid parameters", "success": false, "code": 10}'
        )
        assert not symbol_exists_mock.called
        decode_payload_mock.assert_called_with(jwt="test")
        etria_mock.assert_called()


@mark.asyncio
@patch.object(Gladsheim, "error")
@patch.object(WatchListService, "symbol_exists")
@patch.object(Heimdall, "decode_payload")
async def test_symbol_exists_when_generic_exception_happens(
    decode_payload_mock, symbol_exists_mock, etria_mock
):
    decode_payload_mock.return_value = (decoded_jwt_ok, HeimdallStatusResponses.SUCCESS)
    symbol_exists_mock.side_effect = Exception("erro")

    app = Flask(__name__)
    with app.test_request_context(
        request_ok,
        headers=Headers({"x-thebes-answer": "test"}),
    ).request as request:

        symbol_exists_result = await symbol_exists(request)

        assert (
            symbol_exists_result.data
            == b'{"result": null, "message": "Unexpected error occurred", "success": false, "code": 100}'
        )
        assert symbol_exists_mock.called
        decode_payload_mock.assert_called_with(jwt="test")
        etria_mock.assert_called()
