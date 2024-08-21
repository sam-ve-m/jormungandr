# Standards
from unittest.mock import patch

# Third party
import pytest


@pytest.mark.asyncio
@patch(
    "func.src.domain.ticker.model.config",
    side_effect=[4, "companies", "png", "png", "png"],
)
async def test_when_region_br_then_return_treatment_symbol(mock_config, ticker_model):
    symbol = ticker_model._treatment_ticker_symbol(symbol="PETRAAA", region="BR")

    assert symbol == "PETR"


@pytest.mark.asyncio
async def test_when_region_us_then_return_same_symbol(ticker_model):
    symbol = ticker_model._treatment_ticker_symbol(symbol="AAPL123", region="US")

    assert symbol == "AAPL123"
