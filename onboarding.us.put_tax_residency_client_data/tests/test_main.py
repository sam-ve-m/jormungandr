import logging.config
from flask import Flask
from pytest import mark
from unittest.mock import patch
from werkzeug.test import Headers
from decouple import RepositoryEnv, Config

from func.src.transport.device_info.transport import DeviceSecurity

with patch.object(RepositoryEnv, "__init__", return_value=None):
    with patch.object(Config, "__init__", return_value=None):
        with patch.object(Config, "__call__"):
            with patch.object(logging.config, "dictConfig"):
                from etria_logger import Gladsheim
                from heimdall_client.bifrost import Heimdall, HeimdallStatusResponses
                from func.main import update_external_fiscal_tax
                from func.src.domain.exceptions.model import (
                    InvalidStepError,
                    InternalServerError,
                    DeviceInfoRequestFailed,
                    DeviceInfoNotSupplied,
                )
                from func.src.repositories.sinacor_types.repository import SinacorTypesRepository
                from func.src.services.fiscal_tax.service import FiscalTaxService

request_ok = {"tax_residences": [{"country": "USA", "tax_number": "1292-06"}]}
requests_invalid = [
    {"tax_residencs": [{"country": "USA", "tax_number": "1292-06"}]},
    {"tax_residences": [{"country": "", "tax_number": "1292-06"}]},
    {"tax_residences": [{"country": "USA", "tax_number": None}]},
]

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
@patch.object(SinacorTypesRepository, "validate_country", return_value=True)
@patch.object(Heimdall, "decode_payload")
@patch.object(FiscalTaxService, "update_external_fiscal_tax_residence")
@patch.object(DeviceSecurity, "get_device_info")
async def test_update_external_fiscal_tax_when_request_is_ok(
    device_info,
    update_external_fiscal_tax_residence_mock,
    decode_payload_mock,
    validate_country_mock,
):
    update_external_fiscal_tax_residence_mock.return_value = None
    decode_payload_mock.return_value = (decoded_jwt_ok, HeimdallStatusResponses.SUCCESS)

    app = Flask(__name__)
    with app.test_request_context(
        json=request_ok,
        headers=Headers({"x-thebes-answer": "test"}),
    ).request as request:

        result = await update_external_fiscal_tax(request)

        assert (
            result.data
            == b'{"result": null, "message": "Register Updated.", "success": true, "code": 0}'
        )
        assert update_external_fiscal_tax_residence_mock.called


@mark.asyncio
@patch.object(SinacorTypesRepository, "validate_country", return_value=True)
@patch.object(Gladsheim, "error")
@patch.object(Heimdall, "decode_payload")
@patch.object(FiscalTaxService, "update_external_fiscal_tax_residence")
@patch.object(DeviceSecurity, "get_device_info")
async def test_update_external_fiscal_tax_when_jwt_is_invalid(
    device_info,
    update_external_fiscal_tax_residence_mock,
    decode_payload_mock,
    etria_mock,
    validate_country_mock,
):
    update_external_fiscal_tax_residence_mock.return_value = None
    decode_payload_mock.return_value = (
        decoded_jwt_invalid,
        HeimdallStatusResponses.INVALID_TOKEN,
    )

    app = Flask(__name__)
    with app.test_request_context(
        json=request_ok,
        headers=Headers({"x-thebes-answer": "test"}),
    ).request as request:

        result = await update_external_fiscal_tax(request)

        assert (
            result.data
            == b'{"result": null, "message": "JWT invalid or not supplied", "success": false, "code": 30}'
        )
        assert not update_external_fiscal_tax_residence_mock.called
        assert etria_mock.called


@mark.asyncio
@mark.parametrize("requests", requests_invalid)
@patch.object(SinacorTypesRepository, "validate_country", return_value=True)
@patch.object(Heimdall, "decode_payload")
@patch.object(Gladsheim, "error")
@patch.object(FiscalTaxService, "update_external_fiscal_tax_residence")
@patch.object(DeviceSecurity, "get_device_info")
async def test_update_external_fiscal_tax_when_request_is_invalid(
    device_info,
    update_external_fiscal_tax_residence_mock,
    etria_mock,
    decode_payload_mock,
    validate_country_mock,
    requests,
):
    update_external_fiscal_tax_residence_mock.return_value = None
    decode_payload_mock.return_value = (decoded_jwt_ok, HeimdallStatusResponses.SUCCESS)

    app = Flask(__name__)
    with app.test_request_context(
        json=requests,
        headers=Headers({"x-thebes-answer": "test"}),
    ).request as request:

        result = await update_external_fiscal_tax(request)

        assert (
            result.data
            == b'{"result": null, "message": "Invalid parameters", "success": false, "code": 10}'
        )
        assert not update_external_fiscal_tax_residence_mock.called
        etria_mock.assert_called()


@mark.asyncio
@patch.object(SinacorTypesRepository, "validate_country", return_value=True)
@patch.object(Gladsheim, "error")
@patch.object(Heimdall, "decode_payload")
@patch.object(FiscalTaxService, "update_external_fiscal_tax_residence")
@patch.object(DeviceSecurity, "get_device_info")
async def test_update_external_fiscal_tax_when_user_is_in_invalid_oboarding_step(
    device_info,
    update_external_fiscal_tax_residence_mock,
    decode_payload_mock,
    etria_mock,
    validate_country_mock,
):
    update_external_fiscal_tax_residence_mock.side_effect = InvalidStepError("errooou")
    decode_payload_mock.return_value = (
        decoded_jwt_ok,
        HeimdallStatusResponses.SUCCESS,
    )

    app = Flask(__name__)
    with app.test_request_context(
        json=request_ok,
        headers=Headers({"x-thebes-answer": "test"}),
    ).request as request:

        result = await update_external_fiscal_tax(request)

        assert (
            result.data
            == b'{"result": null, "message": "User in invalid onboarding step", "success": false, "code": 10}'
        )
        assert update_external_fiscal_tax_residence_mock.called
        assert etria_mock.called


@mark.asyncio
@patch.object(SinacorTypesRepository, "validate_country", return_value=True)
@patch.object(Gladsheim, "error")
@patch.object(Heimdall, "decode_payload")
@patch.object(FiscalTaxService, "update_external_fiscal_tax_residence")
@patch.object(DeviceSecurity, "get_device_info")
async def test_update_external_fiscal_tax_when_internal_server_error_occurs(
    device_info,
    update_external_fiscal_tax_residence_mock,
    decode_payload_mock,
    etria_mock,
    validate_country_mock,
):
    update_external_fiscal_tax_residence_mock.side_effect = InternalServerError(
        "errooou"
    )
    decode_payload_mock.return_value = (
        decoded_jwt_ok,
        HeimdallStatusResponses.SUCCESS,
    )

    app = Flask(__name__)
    with app.test_request_context(
        json=request_ok,
        headers=Headers({"x-thebes-answer": "test"}),
    ).request as request:

        result = await update_external_fiscal_tax(request)

        assert (
            result.data
            == b'{"result": null, "message": "Failed to update register", "success": false, "code": 100}'
        )
        assert update_external_fiscal_tax_residence_mock.called
        assert etria_mock.called


@mark.asyncio
@patch.object(SinacorTypesRepository, "validate_country", return_value=True)
@patch.object(Heimdall, "decode_payload")
@patch.object(Gladsheim, "error")
@patch.object(FiscalTaxService, "update_external_fiscal_tax_residence")
@patch.object(DeviceSecurity, "get_device_info")
async def test_update_external_fiscal_tax_when_generic_exception_happens(
    device_info,
    update_external_fiscal_tax_residence_mock,
    etria_mock,
    decode_payload_mock,
    validate_country_mock,
):
    update_external_fiscal_tax_residence_mock.side_effect = Exception("erro")
    decode_payload_mock.return_value = (decoded_jwt_ok, HeimdallStatusResponses.SUCCESS)

    app = Flask(__name__)
    with app.test_request_context(
        json=request_ok,
        headers=Headers({"x-thebes-answer": "test"}),
    ).request as request:

        result = await update_external_fiscal_tax(request)

        assert (
            result.data
            == b'{"result": null, "message": "Unexpected error occurred", "success": false, "code": 100}'
        )
        assert update_external_fiscal_tax_residence_mock.called
        etria_mock.assert_called()


@mark.asyncio
@patch.object(SinacorTypesRepository, "validate_country", return_value=True)
@patch.object(Heimdall, "decode_payload")
@patch.object(Gladsheim, "error")
@patch.object(FiscalTaxService, "update_external_fiscal_tax_residence")
@patch.object(DeviceSecurity, "get_device_info")
async def test_update_external_fiscal_tax_when_fail_to_get_device_info(
    device_info,
    update_external_fiscal_tax_residence_mock,
    etria_mock,
    decode_payload_mock,
    validate_country_mock,
):
    update_external_fiscal_tax_residence_mock.side_effect = DeviceInfoRequestFailed(
        "erro"
    )
    decode_payload_mock.return_value = (decoded_jwt_ok, HeimdallStatusResponses.SUCCESS)

    app = Flask(__name__)
    with app.test_request_context(
        json=request_ok,
        headers=Headers({"x-thebes-answer": "test"}),
    ).request as request:

        result = await update_external_fiscal_tax(request)

        assert (
            result.data
            == b'{"result": null, "message": "Error trying to get device info", "success": false, "code": 100}'
        )
        assert update_external_fiscal_tax_residence_mock.called
        etria_mock.assert_called()


@mark.asyncio
@patch.object(SinacorTypesRepository, "validate_country", return_value=True)
@patch.object(Heimdall, "decode_payload")
@patch.object(Gladsheim, "error")
@patch.object(FiscalTaxService, "update_external_fiscal_tax_residence")
@patch.object(DeviceSecurity, "get_device_info")
async def test_update_external_fiscal_tax_when_device_info_is_not_supplied(
    device_info,
    update_external_fiscal_tax_residence_mock,
    etria_mock,
    decode_payload_mock,
    validate_country_mock,
):
    update_external_fiscal_tax_residence_mock.side_effect = DeviceInfoNotSupplied(
        "erro"
    )
    decode_payload_mock.return_value = (decoded_jwt_ok, HeimdallStatusResponses.SUCCESS)

    app = Flask(__name__)
    with app.test_request_context(
        json=request_ok,
        headers=Headers({"x-thebes-answer": "test"}),
    ).request as request:

        result = await update_external_fiscal_tax(request)

        assert (
            result.data
            == b'{"result": null, "message": "Device info not supplied", "success": false, "code": 10}'
        )
        assert update_external_fiscal_tax_residence_mock.called
        etria_mock.assert_called()
