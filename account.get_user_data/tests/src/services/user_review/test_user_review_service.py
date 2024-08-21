# Jormungandr - Onboarding
from func.src.services.user_review import UserDataService
from func.src.domain.exceptions.exceptions import UserUniqueIdNotExists
from .stubs import stub_unique_id, stub_user

# Third party
from unittest.mock import patch
import pytest


@pytest.mark.asyncio
@patch(
    "func.src.services.user_review.UserRepository.find_one_by_unique_id",
    return_value=None,
)
async def test_when_unique_id_not_exists_then_raises(mock_find_one):
    with pytest.raises(UserUniqueIdNotExists):
        await UserDataService.get_registration_data(unique_id=stub_unique_id)


@pytest.mark.asyncio
@patch(
    "func.src.services.user_review.UserRepository.find_one_by_unique_id",
    return_value=stub_user,
)
async def test_when_unique_id_valid_then_return_customer_registration_built(
    mock_find_one,
):
    result = await UserDataService.get_registration_data(unique_id=stub_unique_id)

    assert isinstance(result, dict)
