# Jormungandr
from func.src.domain.ticker.model import TickerModel
from tests.src.services.stubs import stub_payload_validated

# Standards
from unittest.mock import patch

# Third party
from pytest import fixture


@fixture(scope="function")
@patch(
    "func.src.domain.ticker.model.config",
    side_effect=[4, "companies", "png", "png", "png"],
)
def ticker_model(mock_config):
    instance_model = TickerModel(payload_validated=stub_payload_validated)
    return instance_model
