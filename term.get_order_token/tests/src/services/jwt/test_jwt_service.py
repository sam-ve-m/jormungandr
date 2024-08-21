# Jormungandr - Onboarding
from func.src.domain.exceptions.services.exception import (
    ErrorOnDecodeJwt,
    ErrorOnGetUniqueId,
)
from func.src.services.jwt.service import JwtService
from tests.src.services.jwt.stubs import (
    stub_heimdall_response,
    stub_heimdall_response_failure,
    stub_heimdall_with_no_content,
)

# Standards
from unittest.mock import patch

# Third party
import pytest


@pytest.mark.asyncio
@patch(
    "func.src.services.jwt.service.Heimdall.decode_payload", return_value=stub_heimdall_response
)
async def test_when_valid_jwt_then_return_user_unique_id(mock_heimdall):
    unique_id = await JwtService.decode_jwt_and_get_unique_id(jwt="123")

    assert isinstance(unique_id, str)
    assert unique_id == "451baf5a-9cd5-4037-aa17-fbd0fcef66c8"


@pytest.mark.asyncio
@patch(
    "func.src.services.jwt.service.Heimdall.decode_payload",
    return_value=stub_heimdall_response_failure,
)
async def test_when_invalid_jwt_then_raises(mock_heimdall):
    with pytest.raises(ErrorOnDecodeJwt):
        await JwtService.decode_jwt_and_get_unique_id(jwt="123")


@pytest.mark.asyncio
@patch(
    "func.src.services.jwt.service.Heimdall.decode_payload",
    return_value=stub_heimdall_with_no_content,
)
async def test_when_no_content_in_jwt_then_raises(mock_heimdall):
    with pytest.raises(ErrorOnGetUniqueId):
        await JwtService.decode_jwt_and_get_unique_id(jwt="123")
