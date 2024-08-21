from unittest.mock import patch, call, AsyncMock

import pytest
from decouple import Config

from func.src.domain.exceptions.exceptions import UserWasNotUpdated
from func.src.repositories.user.repository import UserRepository

dummy_env = "dummy env"
fake_collection = AsyncMock()
fake_bureau_validation = AsyncMock()


@patch.object(Config, "__call__", return_value=dummy_env)
@patch.object(UserRepository, "_instance_collection", return_value=fake_collection)
def test_get_collection(mocked_repository, mocked_env):
    new_connection_created = UserRepository._get_collection()
    assert new_connection_created == fake_collection
    mocked_repository.assert_called_once_with(dummy_env, dummy_env)
    mocked_env.assert_has_calls((call("MONGO_DATABASE_LIONX"), call("MONGODB_COLLECTION_USERS")))

    reused_client = UserRepository._get_collection()
    assert reused_client == new_connection_created
    mocked_repository.assert_called_once_with(dummy_env, dummy_env)
    mocked_env.assert_has_calls((call("MONGO_DATABASE_LIONX"), call("MONGODB_COLLECTION_USERS")))
    UserRepository.collection = None


@pytest.mark.asyncio
@patch.object(Config, "__call__", return_value=dummy_env)
@patch.object(UserRepository, "_get_collection", return_value=fake_collection)
async def test_update_bureau_validation(mocked_repository, mocked_env):
    fake_collection.update_one.return_value.matched_count = 1
    response = await UserRepository.update_bureau_validation(
        dummy_env, fake_bureau_validation
    )
    mocked_repository.assert_called_once_with()
    fake_collection.update_one.assert_called_with(
        {"identifier_document.cpf": dummy_env},
        {"$set": {
            "bureau_validations.cpf": fake_bureau_validation.status.value,
        }}
    )
    assert response is True


@pytest.mark.asyncio
@patch.object(Config, "__call__", return_value=dummy_env)
@patch.object(UserRepository, "_get_collection", return_value=fake_collection)
async def test_update_bureau_validation_user_not_found(mocked_repository, mocked_env):
    fake_collection.update_one.return_value.matched_count = 0
    with pytest.raises(UserWasNotUpdated):
        await UserRepository.update_bureau_validation(
            dummy_env, fake_bureau_validation
        )
    mocked_repository.assert_called_once_with()
    fake_collection.update_one.assert_called_with(
        {"identifier_document.cpf": dummy_env},
        {"$set": {
            "bureau_validations.cpf": fake_bureau_validation.status.value,
        }}
    )
