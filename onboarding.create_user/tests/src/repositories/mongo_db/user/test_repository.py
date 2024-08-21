import pytest
from unittest.mock import patch, call
from func.src.repositories.user.repository import UserRepository

dummy_email = "email"


@pytest.mark.asyncio
@patch.object(UserRepository, "_UserRepository__get_collection")
async def test_find_one_by_email(mocked_collection):
    result = await UserRepository.find_one_by_email(
        dummy_email,
    )
    mocked_collection.return_value.find_one.assert_called_once_with(
        {"email": dummy_email}, {"_id": True}
    )
    assert mocked_collection.return_value.find_one.return_value == result
