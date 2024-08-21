from unittest.mock import patch
from etria_logger import Gladsheim
import pytest
from decouple import Config
from flask import Flask
from heimdall_client import HeimdallStatusResponses, Heimdall
from werkzeug.datastructures import Headers

from func.src.domain.exceptions.exceptions import (
    DeviceInfoRequestFailed,
    DeviceInfoNotSupplied,
)
from func.src.services.enum_experience_time.service import ExperienceTimeEnumService

with patch.object(Config, "__call__"):
    from func.main import update_experience_time
    from func.src.domain.models.jwt.models import Jwt
    from func.src.services.update_time_experience.service import (
        UpdateMarketTimeExperience,
    )
    from func.src.transport.device_info.transport import DeviceSecurity
    from tests.main_stub import request_body_stub, decoded_jwt_stub

jwt_response = "125458.hagfsdsa"


@pytest.mark.asyncio
@patch.object(
    Heimdall,
    "decode_payload",
    return_value=(decoded_jwt_stub, HeimdallStatusResponses.SUCCESS),
)
@patch(
    "func.src.services.enum_experience_time.service.ExperienceTimeEnumService.experience_time_enum_validation",
    return_value=True,
)
@patch(
    "func.src.services.update_time_experience.service.UpdateMarketTimeExperience.update_market_time_experience",
    return_value=True,
)
@patch.object(DeviceSecurity, "get_device_info")
@patch.object(Config, "__call__")
async def test_when_sending_right_params_to_update_market_experience_time_then_return_the_expected(
    config,
    device_info,
    mock_update_market_time_experience,
    mock_experience_time_enum_validation,
    mock_decode_and_validate_jwt,
):

    app = Flask(__name__)
    with app.test_request_context(
        json=request_body_stub,
        headers=Headers({"x-thebes-answer": "jwt_to_decode_stub"}),
    ).request as request:
        response = await update_experience_time(request)
        assert response.status_code == 200


enums_data_stub = [("LALA", "lala"), ("LILI", "lili")]


@pytest.mark.asyncio
@patch.object(
    Heimdall,
    "decode_payload",
    return_value=(None, HeimdallStatusResponses.INVALID_TOKEN),
)
@patch(
    "func.src.services.enum_experience_time.service.ExperienceTimeEnumService.experience_time_enum_validation",
    return_value=False,
)
@patch.object(Jwt, "get_unique_id_from_jwt_payload", return_value=jwt_response)
@patch.object(Jwt, "get_experience_time_from_jwt_payload", return_value=jwt_response)
@patch.object(
    UpdateMarketTimeExperience, "update_market_time_experience", return_value=Exception
)
@patch.object(DeviceSecurity, "get_device_info")
@patch.object(Config, "__call__")
async def test_when_sending_wrong_params_to_update_market_experience_time_then_return_the_expected_error(
    config,
    device_info,
    mock_update_market_time_experience,
    mock_get_experience_time_from_jwt_payload,
    mock_get_unique_id_from_jwt_payload,
    mock_experience_time_enum_validation,
    mock_decode_payload,
):
    app = Flask(__name__)
    with app.test_request_context(
        json=None,
        headers=Headers({"x-thebes-answer": "jwt_to_decode_stub"}),
    ).request as request:
        device_info.side_effect = Exception()
        response = await update_experience_time(request)
        assert response.status_code == 500


@pytest.mark.asyncio
@patch.object(Gladsheim, "error")
@patch.object(Heimdall, "decode_payload")
@patch.object(ExperienceTimeEnumService, "experience_time_enum_validation")
@patch.object(UpdateMarketTimeExperience, "update_market_time_experience")
@patch.object(DeviceSecurity, "get_device_info")
async def test_update_employ_for_us_when_fail_to_get_device_info(
    device_info,
    update_time_experience,
    validator,
    heimdall_mock,
    etria_mock,
):
    validator.side_effect = DeviceInfoRequestFailed("errooou")
    heimdall_mock.return_value = ({}, HeimdallStatusResponses.SUCCESS)
    app = Flask(__name__)
    with app.test_request_context(
        json=request_body_stub,
        headers=Headers({"x-thebes-answer": "test"}),
    ).request as request:

        result = await update_experience_time(request)

        assert (
            result.data
            == b'{"result": null, "message": "Error trying to get device info", "success": false, "code": 100}'
        )
        assert etria_mock.called


@pytest.mark.asyncio
@patch.object(Gladsheim, "error")
@patch.object(Heimdall, "decode_payload")
@patch.object(ExperienceTimeEnumService, "experience_time_enum_validation")
@patch.object(UpdateMarketTimeExperience, "update_market_time_experience")
@patch.object(DeviceSecurity, "get_device_info")
async def test_update_employ_for_us_when_device_info_is_not_supplied(
    device_info,
    update_time_experience,
    validator,
    heimdall_mock,
    etria_mock,
):
    validator.side_effect = DeviceInfoNotSupplied("errooou")
    heimdall_mock.return_value = ({}, HeimdallStatusResponses.SUCCESS)
    app = Flask(__name__)
    with app.test_request_context(
        json=request_body_stub,
        headers=Headers({"x-thebes-answer": "test"}),
    ).request as request:

        result = await update_experience_time(request)

        assert (
            result.data
            == b'{"result": null, "message": "Device info not supplied", "success": false, "code": 10}'
        )
        assert etria_mock.called
