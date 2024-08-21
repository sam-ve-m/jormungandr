from unittest.mock import patch, call, AsyncMock, MagicMock

import pytest
from decouple import Config

from func.src.domain.exceptions.exceptions import TransactionNotFound, UniqueIdNotFound, TransactionWasNotUpdated
from func.src.repositories.bureau_transactions.repository import BureauTransactionRepository

dummy_env = "dummy env"
fake_collection = AsyncMock()
fake_bureau_validation = AsyncMock()


@patch.object(Config, "__call__", return_value=dummy_env)
@patch.object(BureauTransactionRepository, "_instance_collection", return_value=fake_collection)
def test_get_collection(mocked_repository, mocked_env):
    new_connection_created = BureauTransactionRepository._get_collection()
    assert new_connection_created == fake_collection
    mocked_repository.assert_called_once_with(dummy_env, dummy_env)
    mocked_env.assert_has_calls((call("MONGO_DATABASE_LIONX"), call("MONGO_COLLECTION_BUREAU")))

    reused_client = BureauTransactionRepository._get_collection()
    assert reused_client == new_connection_created
    mocked_repository.assert_called_once_with(dummy_env, dummy_env)
    mocked_env.assert_has_calls((call("MONGO_DATABASE_LIONX"), call("MONGO_COLLECTION_BUREAU")))
    BureauTransactionRepository.collection = None


@pytest.mark.asyncio
@patch.object(BureauTransactionRepository, "_get_collection", return_value=fake_collection)
async def test_update_bureau_transaction(mocked_repository):
    fake_collection.update_one.return_value.matched_count = 1
    response = await BureauTransactionRepository.update_bureau_transaction(
        fake_bureau_validation
    )
    mocked_repository.assert_called_once_with()
    fake_collection.update_one.assert_called_with(
        {"transaction_id": fake_bureau_validation.uuid},
        {"$set": {
            "status": fake_bureau_validation.status.value,
            "last_update_date": fake_bureau_validation.date,
            "event_type": fake_bureau_validation.event_type.value,
            "status_reasons": fake_bureau_validation.status_reasons,
        }}
    )
    assert response is True


@pytest.mark.asyncio
@patch.object(BureauTransactionRepository, "_get_collection", return_value=fake_collection)
async def test_update_bureau_transaction_user_not_found(mocked_repository):
    fake_collection.update_one.return_value.matched_count = 0
    with pytest.raises(TransactionWasNotUpdated):
        await BureauTransactionRepository.update_bureau_transaction(
            fake_bureau_validation
        )
    mocked_repository.assert_called_once_with()
    fake_collection.update_one.assert_called_with(
        {"transaction_id": fake_bureau_validation.uuid},
        {"$set": {
            "status": fake_bureau_validation.status.value,
            "last_update_date": fake_bureau_validation.date,
            "event_type": fake_bureau_validation.event_type.value,
            "status_reasons": fake_bureau_validation.status_reasons,
        }}
    )


fake_transaction = MagicMock()


@pytest.mark.asyncio
@patch.object(BureauTransactionRepository, "_get_collection", return_value=fake_collection)
async def test_get_user_unique_id_of_transaction_without_unique_id(mocked_repository):
    fake_collection.find_one.return_value = fake_transaction
    fake_transaction.get.return_value = False
    with pytest.raises(UniqueIdNotFound):
        await BureauTransactionRepository.get_user_unique_id_of_transaction(fake_bureau_validation)
    mocked_repository.assert_called_once_with()
    fake_collection.find_one.assert_called_with({
        "transaction_id": fake_bureau_validation.uuid
    })


@pytest.mark.asyncio
@patch.object(BureauTransactionRepository, "_get_collection", return_value=fake_collection)
async def test_get_user_unique_id_of_transaction(mocked_repository):
    fake_collection.find_one.return_value = fake_transaction
    fake_transaction.get.return_value = dummy_env
    result = await BureauTransactionRepository.get_user_unique_id_of_transaction(fake_bureau_validation)
    mocked_repository.assert_called_once_with()
    fake_collection.find_one.assert_called_with({
        "transaction_id": fake_bureau_validation.uuid
    })
    assert dummy_env == result


@pytest.mark.asyncio
@patch.object(BureauTransactionRepository, "_get_collection", return_value=fake_collection)
async def test_get_user_unique_id_of_transaction_without_transaction(mocked_repository):
    fake_collection.find_one.return_value = None
    with pytest.raises(TransactionNotFound):
        await BureauTransactionRepository.get_user_unique_id_of_transaction(fake_bureau_validation)
    mocked_repository.assert_called_once_with()
    fake_collection.find_one.assert_called_with({
        "transaction_id": fake_bureau_validation.uuid
    })
