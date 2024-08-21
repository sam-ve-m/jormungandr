from unittest.mock import patch

from etria_logger import Gladsheim
from flask import Flask
from heimdall_client.bifrost import Heimdall, HeimdallStatusResponses
from pytest import mark
from werkzeug.test import Headers

from main import get_term
from src.domain.exceptions.exceptions import FileNotFound
from src.services.terms.service import TermService

request_ok = "?file_type=term_refusal"
requests_invalid = ["?file_typ=term_refusal", "?file_type=term_reusal"]

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


@mark.asyncio
@patch.object(Heimdall, "decode_payload")
@patch.object(TermService, "get_term_url")
async def test_save_symbols_when_request_is_ok(get_term_mock, decode_payload_mock):
    get_term_mock.return_value = "https://www.term_link_here.com"
    decode_payload_mock.return_value = (decoded_jwt_ok, HeimdallStatusResponses.SUCCESS)

    app = Flask(__name__)
    with app.test_request_context(
        request_ok,
        headers=Headers({"x-thebes-answer": "test"}),
    ).request as request:

        save_symbols_result = await get_term(request)

        assert (
            save_symbols_result.data
            == b'{"result": "https://www.term_link_here.com", "message": "Success", "success": true, "code": 0}'
        )
        assert get_term_mock.called


@mark.asyncio
@patch.object(Heimdall, "decode_payload")
@patch.object(Gladsheim, "error")
@patch.object(TermService, "get_term_url")
async def test_save_symbols_when_image_is_not_found(
    get_term_mock, etria_mock, decode_payload_mock
):
    get_term_mock.side_effect = FileNotFound()
    decode_payload_mock.return_value = (decoded_jwt_ok, HeimdallStatusResponses.SUCCESS)

    app = Flask(__name__)
    with app.test_request_context(
        request_ok,
        headers=Headers({"x-thebes-answer": "test"}),
    ).request as request:

        save_symbols_result = await get_term(request)

        assert (
            save_symbols_result.data
            == b'{"result": null, "message": "Term file not found", "success": true, "code": 0}'
        )
        assert get_term_mock.called
        etria_mock.assert_called()


@mark.asyncio
@patch.object(Gladsheim, "error")
@patch.object(Heimdall, "decode_payload")
@patch.object(TermService, "get_term_url")
async def test_save_symbols_when_jwt_is_invalid(
    get_term_mock, decode_payload_mock, etria_mock
):
    get_term_mock.return_value = "https://www.term_link_here.com"
    decode_payload_mock.return_value = (
        decoded_jwt_invalid,
        HeimdallStatusResponses.INVALID_TOKEN,
    )

    app = Flask(__name__)
    with app.test_request_context(
        request_ok,
        headers=Headers({"x-thebes-answer": "test"}),
    ).request as request:

        save_symbols_result = await get_term(request)

        assert (
            save_symbols_result.data
            == b'{"result": null, "message": "JWT invalid or not supplied", "success": false, "code": 30}'
        )
        assert not get_term_mock.called
        assert etria_mock.called


@mark.asyncio
@mark.parametrize("requests", requests_invalid)
@patch.object(Heimdall, "decode_payload")
@patch.object(Gladsheim, "error")
@patch.object(TermService, "get_term_url")
async def test_save_symbols_when_request_is_invalid(
    get_term_mock, etria_mock, decode_payload_mock, requests
):
    get_term_mock.return_value = True
    decode_payload_mock.return_value = (decoded_jwt_ok, HeimdallStatusResponses.SUCCESS)

    app = Flask(__name__)
    with app.test_request_context(
        requests,
        headers=Headers({"x-thebes-answer": "test"}),
    ).request as request:

        save_symbols_result = await get_term(request)

        assert (
            save_symbols_result.data
            == b'{"result": null, "message": "Invalid parameters", "success": false, "code": 10}'
        )
        assert not get_term_mock.called
        etria_mock.assert_called()


@mark.asyncio
@patch.object(Heimdall, "decode_payload")
@patch.object(Gladsheim, "error")
@patch.object(TermService, "get_term_url")
async def test_save_symbols_when_generic_exception_happens(
    get_term_mock, etria_mock, decode_payload_mock
):
    get_term_mock.side_effect = Exception("erro")
    decode_payload_mock.return_value = (decoded_jwt_ok, HeimdallStatusResponses.SUCCESS)

    app = Flask(__name__)
    with app.test_request_context(
        request_ok,
        headers=Headers({"x-thebes-answer": "test"}),
    ).request as request:

        save_symbols_result = await get_term(request)

        assert (
            save_symbols_result.data
            == b'{"result": null, "message": "Unexpected error occurred", "success": false, "code": 100}'
        )
        assert get_term_mock.called
        etria_mock.assert_called()
