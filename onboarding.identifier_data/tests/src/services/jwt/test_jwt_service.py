import logging.config
from unittest.mock import patch

import pytest
from decouple import Config, RepositoryEnv
from heimdall_client import Heimdall

with patch.object(logging.config, "dictConfig"):
    with patch.object(Config, "__call__"):
        with patch.object(Config, "__init__", return_value=None):
            with patch.object(RepositoryEnv, "__init__", return_value=None):
                from func.src.domain.exceptions.exceptions import (
                    ErrorOnDecodeJwt,
                    ErrorOnGetUniqueId,
                )
                from func.src.services.jwt import JwtService
                from tests.src.services.jwt.stubs import (
                    stub_heimdall_response,
                    stub_heimdall_response_failure,
                    stub_heimdall_with_no_content,
                )


@pytest.mark.asyncio
@patch.object(Heimdall, "decode_payload", return_value=stub_heimdall_response)
async def test_when_valid_jwt_then_return_user_unique_id(mock_heimdall):
    unique_id = await JwtService.decode_jwt_and_get_unique_id(jwt="123")

    assert isinstance(unique_id, str)
    assert unique_id == "451baf5a-9cd5-4037-aa17-fbd0fcef66c8"


@pytest.mark.asyncio
@patch.object(Heimdall, "decode_payload", return_value=stub_heimdall_response_failure)
async def test_when_invalid_jwt_then_raises(mock_heimdall):
    with pytest.raises(ErrorOnDecodeJwt):
        await JwtService.decode_jwt_and_get_unique_id(jwt="123")


@pytest.mark.asyncio
@patch.object(Heimdall, "decode_payload", return_value=stub_heimdall_with_no_content)
async def test_when_no_content_in_jwt_then_raises(mock_heimdall):
    with pytest.raises(ErrorOnGetUniqueId):
        await JwtService.decode_jwt_and_get_unique_id(jwt="123")
