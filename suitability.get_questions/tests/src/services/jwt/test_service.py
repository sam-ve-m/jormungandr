# Jormungandr
from func.src.services.jwt.service import JwtService
from func.src.domain.exceptions.service.exception import ErrorOnDecodeJwt

# Standards
from unittest.mock import patch

# Third party
import pytest
from heimdall_client import HeimdallStatusResponses


@pytest.mark.asyncio
@patch(
    "func.src.services.jwt.service.Heimdall.decode_payload",
    return_value=(None, HeimdallStatusResponses.SUCCESS),
)
async def test_when_valid_jwt_then_return_true(mock_heimdall):
    result = await JwtService.validate_jwt(jwt="jwt")

    assert isinstance(result, bool)
    assert result is True


@pytest.mark.asyncio
@patch(
    "func.src.services.jwt.service.Heimdall.decode_payload",
    return_value=(None, HeimdallStatusResponses.INTERNAL_HEIMDALL_ERROR),
)
async def test_when_invalid_jwt_then_raises(mock_heimdall):
    with pytest.raises(ErrorOnDecodeJwt):
        await JwtService.validate_jwt(jwt="jwt")
