# Jormungandr
from func.src.services.ticker import TickerVisualIdentityService
from func.src.domain.exceptions.exception import TickerNotFound

from tests.src.services.stubs import (
    stub_payload_validated,
    stub_ticker_path,
    stub_url_access,
    stub_ticker_url_encoded,
)

# Standards
from unittest.mock import patch

# Third party
import pytest


@pytest.mark.asyncio
@patch(
    "func.src.domain.ticker.model.config",
    side_effect=[4, "companies", "png", "png", "png"],
)
@patch(
    "func.src.services.ticker.TickerVisualIdentityService._get_or_set_ticker_url_access",
    return_value=stub_url_access,
)
async def test_when_get_ticker_url_success_then_return_expected_result(
    mock_function, mock_config
):
    result = await TickerVisualIdentityService.get_ticker_url(
        payload_validated=stub_payload_validated
    )

    assert isinstance(result, dict)
    assert (
        result.get("url")
        == "https://dtvm-visual-identity-files.s3.amazonaws.com/companies/BR/PETR/logo.png"
    )
    assert result.get("type") == "logo"


@pytest.mark.asyncio
@patch(
    "func.src.services.ticker.RedisRepository.get", return_value=stub_ticker_url_encoded
)
async def test_when_get_on_redis_then_return_expected_values(mock_redis_get):
    result = await TickerVisualIdentityService._get_or_set_ticker_url_access(
        ticker_path=stub_ticker_path
    )

    assert isinstance(result, str)
    assert (
        result
        == "https://dtvm-visual-identity-files.s3.amazonaws.com/companies/BR/PETR/logo.png"
    )


@pytest.mark.asyncio
@patch("func.src.services.ticker.S3Repository.get_ticker", return_value=False)
@patch("func.src.services.ticker.RedisRepository.get", return_value=False)
async def test_when_ticker_not_found_then_raises(mock_redis_get, mock_s3_get):
    with pytest.raises(TickerNotFound):
        await TickerVisualIdentityService._get_or_set_ticker_url_access(
            ticker_path=stub_ticker_path
        )


@pytest.mark.asyncio
@patch("func.src.services.ticker.RedisRepository.set")
@patch(
    "func.src.services.ticker.S3Repository.generate_ticker_url",
    return_value=stub_url_access,
)
@patch("func.src.services.ticker.S3Repository.get_ticker", return_value=True)
@patch("func.src.services.ticker.RedisRepository.get", return_value=False)
async def test_when_found_ticker_in_s3_then_return_expected_values(
    mock_redis_get, mock_s3_get, mock_generate_url_access, mock_redis_set
):
    result = await TickerVisualIdentityService._get_or_set_ticker_url_access(
        ticker_path=stub_ticker_path
    )

    assert isinstance(result, str)
    assert (
        result
        == "https://dtvm-visual-identity-files.s3.amazonaws.com/companies/BR/PETR/logo.png"
    )
