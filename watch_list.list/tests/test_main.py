from unittest.mock import patch

import decouple
from etria_logger import Gladsheim
from flask import Flask
from heimdall_client import HeimdallStatusResponses
from heimdall_client.bifrost import Heimdall
from pytest import mark
from werkzeug.test import Headers

with patch.object(decouple, "config", return_value="CONFIG"):
    from func.main import list_assets
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

requests_with_invalid_parameters = [
    "?limit=&offset=12",
    "?limit1=&offset=",
    "?limit=-1&offset=-1",
]


@mark.asyncio
@patch.object(WatchListService, "list_assets_in_watch_list")
@patch.object(Heimdall, "decode_payload")
async def test_list_assets_when_request_is_ok(
    decode_payload_mock, list_assets_in_watch_list_mock
):
    decode_payload_mock.return_value = (decoded_jwt_ok, HeimdallStatusResponses.SUCCESS)
    service_result = {
        "assets": {"symbol": "symbol", "region": "region"},
        "pages": 1,
        "current_page": 1,
    }
    list_assets_in_watch_list_mock.return_value = service_result

    app = Flask(__name__)
    with app.test_request_context(
        "?limit=3&offset=12",
        headers=Headers({"x-thebes-answer": "test"}),
    ).request as request:

        list_assets_result = await list_assets(request)

        assert (
            list_assets_result.data
            == b'{"result": {"assets": {"symbol": "symbol", "region": "region"}, "pages": 1, "current_page": 1}, "message": "Success", "success": true, "code": 0}'
        )
        assert list_assets_in_watch_list_mock.called
        decode_payload_mock.assert_called_with(jwt="test")


@mark.asyncio
@patch.object(Gladsheim, "error")
@patch.object(WatchListService, "list_assets_in_watch_list")
@patch.object(Heimdall, "decode_payload")
async def test_list_assets_when_jwt_is_invalid(
    decode_payload_mock, list_assets_in_watch_list_mock, etria_mock
):
    decode_payload_mock.return_value = (
        decoded_jwt_invalid,
        HeimdallStatusResponses.INVALID_TOKEN,
    )
    service_result = {
        "assets": {"symbol": "symbol", "region": "region"},
        "pages": 1,
        "current_page": 1,
    }
    list_assets_in_watch_list_mock.return_value = service_result

    app = Flask(__name__)
    with app.test_request_context(
        "?limit=3&offset=12",
        headers=Headers({"x-thebes-answer": "test_error"}),
    ).request as request:

        list_assets_result = await list_assets(request)

        assert (
            list_assets_result.data
            == b'{"result": null, "message": "JWT invalid or not supplied", "success": false, "code": 30}'
        )
        assert not list_assets_in_watch_list_mock.called
        decode_payload_mock.assert_called_with(jwt="test_error")
        etria_mock.assert_called()


@mark.asyncio
@patch.object(Gladsheim, "error")
@patch.object(WatchListService, "list_assets_in_watch_list")
@patch.object(Heimdall, "decode_payload")
async def test_list_assets_when_generic_exception_happens(
    decode_payload_mock, list_assets_in_watch_list_mock, etria_mock
):
    decode_payload_mock.return_value = (decoded_jwt_ok, HeimdallStatusResponses.SUCCESS)
    list_assets_in_watch_list_mock.side_effect = Exception("erro")

    app = Flask(__name__)
    with app.test_request_context(
        "?limit=3&offset=12",
        headers=Headers({"x-thebes-answer": "test"}),
    ).request as request:

        list_assets_result = await list_assets(request)

        assert (
            list_assets_result.data
            == b'{"result": null, "message": "Unexpected error occurred", "success": false, "code": 100}'
        )
        assert list_assets_in_watch_list_mock.called
        decode_payload_mock.assert_called_with(jwt="test")
        etria_mock.assert_called()
