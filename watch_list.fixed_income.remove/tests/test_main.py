from unittest.mock import patch

from etria_logger import Gladsheim
from flask import Flask
from heimdall_client.bifrost import Heimdall
from heimdall_client.bifrost import HeimdallStatusResponses
from pytest import mark
from werkzeug.test import Headers

from func.main import remove_products
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

request_ok = "?product_id=12&region=BR"
requests_with_invalid_parameters = [
    "?smbol=PETR4&region=BR",
    "?product=PETR4&regon=BR",
    "?product=&region=BR",
    "?product=PETR4&region=PR",
    "",
]


@mark.asyncio
@patch.object(WatchListService, "delete_products")
@patch.object(Heimdall, "decode_payload")
async def test_remove_products_when_request_is_ok(
    decode_payload_mock, register_products_mock
):
    decode_payload_mock.return_value = (decoded_jwt_ok, HeimdallStatusResponses.SUCCESS)
    register_products_mock.return_value = True

    app = Flask(__name__)
    with app.test_request_context(
        request_ok,
        headers=Headers({"x-thebes-answer": "test"}),
    ).request as request:

        remove_products_result = await remove_products(request)

        assert (
            remove_products_result.data
            == b'{"result": null, "message": "Products successfully deleted", "success": true, "code": 0}'
        )
        assert register_products_mock.called
        decode_payload_mock.assert_called_with(jwt="test")


@mark.asyncio
@patch.object(Gladsheim, "error")
@patch.object(WatchListService, "delete_products")
@patch.object(Heimdall, "decode_payload")
async def test_remove_products_when_jwt_is_invalid(
    decode_payload_mock, register_products_mock, etria_mock
):
    decode_payload_mock.return_value = (
        decoded_jwt_invalid,
        HeimdallStatusResponses.INVALID_TOKEN,
    )
    register_products_mock.return_value = True

    app = Flask(__name__)
    with app.test_request_context(
        request_ok,
        headers=Headers({"x-thebes-answer": "test_error"}),
    ).request as request:

        remove_products_result = await remove_products(request)

        assert (
            remove_products_result.data
            == b'{"result": null, "message": "JWT invalid or not supplied", "success": false, "code": 30}'
        )
        assert not register_products_mock.called
        decode_payload_mock.assert_called_with(jwt="test_error")
        etria_mock.assert_called()


@mark.asyncio
@mark.parametrize("request_json", requests_with_invalid_parameters)
@patch.object(Gladsheim, "error")
@patch.object(WatchListService, "delete_products")
@patch.object(Heimdall, "decode_payload")
async def test_remove_products_when_parameters_are_invalid(
    decode_payload_mock, register_products_mock, etria_mock, request_json
):
    decode_payload_mock.return_value = (decoded_jwt_ok, HeimdallStatusResponses.SUCCESS)
    register_products_mock.return_value = True

    app = Flask(__name__)
    with app.test_request_context(
        request_json,
        headers=Headers({"x-thebes-answer": "test"}),
    ).request as request:

        remove_products_result = await remove_products(request)

        assert (
            remove_products_result.data
            == b'{"result": null, "message": "Invalid parameters", "success": false, "code": 10}'
        )
        assert not register_products_mock.called
        decode_payload_mock.assert_called_with(jwt="test")
        etria_mock.assert_called()


@mark.asyncio
@patch.object(Gladsheim, "error")
@patch.object(WatchListService, "delete_products")
@patch.object(Heimdall, "decode_payload")
async def test_remove_products_when_generic_exception_happens(
    decode_payload_mock, register_products_mock, etria_mock
):
    decode_payload_mock.return_value = (decoded_jwt_ok, HeimdallStatusResponses.SUCCESS)
    register_products_mock.side_effect = Exception("erro")

    app = Flask(__name__)
    with app.test_request_context(
        request_ok,
        headers=Headers({"x-thebes-answer": "test"}),
    ).request as request:

        remove_products_result = await remove_products(request)

        assert (
            remove_products_result.data
            == b'{"result": null, "message": "Unexpected error occurred", "success": false, "code": 100}'
        )
        assert register_products_mock.called
        decode_payload_mock.assert_called_with(jwt="test")
        etria_mock.assert_called()
