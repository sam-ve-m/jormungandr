# Jormungandr
from func.src.services.suitability.service import SuitabilityService
from tests.src.services.suitability.stubs import stub_suitability_mongo_db

# Standards
from unittest.mock import patch

# Third party
import pytest


@pytest.mark.asyncio
@patch(
    "func.src.services.suitability.service.SuitabilityRepository.get_latest_suitability",
    return_value=stub_suitability_mongo_db,
)
@patch("func.src.services.suitability.service.AsyncCache.get", return_value=None)
@patch(
    "func.src.services.suitability.service.config",
    side_effect=["suitability_key", "suitability_key", "86400"],
)
async def test_when_not_have_suitability_data_in_redis_then_get_in_mongo_and_set_in_redis_to_return_model(
    mock_decouple, mock_redis, mock_repository
):
    suitability = await SuitabilityService.get_latest_questions_with_answer_options()

    assert isinstance(suitability, dict)
    assert suitability.get("version") == 12


@pytest.mark.asyncio
@patch('func.src.services.suitability.service.AsyncCache.get', return_value=stub_suitability_mongo_db)
@patch(
    "func.src.services.suitability.service.config",
    side_effect=["suitability_key", "suitability_key", "86400"],
)
async def test_when_have_suitability_in_redis_then_return_suitability_data(mock_params, mock_redis):
    suitability = await SuitabilityService.get_latest_questions_with_answer_options()

    assert isinstance(suitability, dict)
    assert suitability.get("version") == 12
