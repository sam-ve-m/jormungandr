import pytest
from decouple import AutoConfig
from etria_logger import Gladsheim
from unittest.mock import patch, MagicMock, AsyncMock
from src.repositories.user.repository import UserRepository

dummy_env = "dummy env"
fake_infra = MagicMock()
fake_collection = AsyncMock()
dummy_cpf = "dummy cpf"
index_error = IndexError()


@pytest.mark.asyncio
@patch.object(Gladsheim, "error")
@patch.object(AutoConfig, "__call__", return_value=dummy_env)
async def test_find_client_unique_id_raising_error_in_get_collection(
        mocked_env, mocked_logger, monkeypatch
):
    monkeypatch.setattr(UserRepository, "infra", fake_infra)
    fake_infra.get_client.return_value[dummy_env].__getitem__.side_effect = index_error
    with pytest.raises(index_error.__class__):
        await UserRepository.find_client_unique_id(dummy_cpf)
    mocked_logger.assert_called_once_with(
        error=index_error,
        message=(
                    f"UserRepository::__get_collection::Error when trying to get collection"
                ),
        database=dummy_env,
        collection=dummy_env,
    )
    mocked_env.assert_called()


dummy_user_filter = {"identifier_document.cpf": dummy_cpf}
dummy_fiscal_tax_residence = "fiscal_tax_residence"
stub_fiscal_tax_residence = {"fiscal_tax_residence": dummy_fiscal_tax_residence, "_id": None}


@pytest.mark.asyncio
@patch.object(Gladsheim, "error")
@patch.object(AutoConfig, "__call__", return_value=dummy_env)
async def test_find_client_unique_id_not_finding_user(
        mocked_env, mocked_logger, monkeypatch
):
    monkeypatch.setattr(UserRepository, "infra", fake_infra)
    fake_infra.get_client.return_value[dummy_env].__getitem__.side_effect = None
    fake_infra.get_client.return_value[dummy_env].__getitem__.return_value = fake_collection
    fake_collection.find_one.return_value = None
    response = await UserRepository.find_client_unique_id(dummy_cpf)
    fake_collection.find_one.assert_called_with(dummy_user_filter)
    mocked_logger.assert_not_called()
    mocked_env.assert_called()
    assert response is None


@pytest.mark.asyncio
@patch.object(Gladsheim, "error")
@patch.object(AutoConfig, "__call__", return_value=dummy_env)
async def test_find_client_unique_id(
        mocked_env, mocked_logger, monkeypatch
):
    monkeypatch.setattr(UserRepository, "infra", fake_infra)
    fake_infra.get_client.return_value[dummy_env].__getitem__.return_value = fake_collection
    fake_collection.find_one.return_value = stub_fiscal_tax_residence.copy()
    await UserRepository.find_client_unique_id(dummy_cpf)
    fake_collection.find_one.assert_called_with(dummy_user_filter)
    mocked_logger.assert_not_called()
    mocked_env.assert_called()


stub_exchange_account = MagicMock()
updated_nothing = (0, False)
updated_one = (1, True)
updated_more_than_one = (2, False)


@pytest.mark.asyncio
@pytest.mark.parametrize("matched,expected", [updated_nothing, updated_one, updated_more_than_one])
@patch.object(AutoConfig, "__call__", return_value=dummy_env)
async def test_update_exchange_account_true(
        mocked_env, monkeypatch, matched, expected
):
    monkeypatch.setattr(UserRepository, "infra", fake_infra)
    fake_infra.get_client.return_value[dummy_env].__getitem__.return_value = fake_collection
    fake_collection.update_one.return_value.matched_count = matched
    response = await UserRepository.update_exchange_account_status(stub_exchange_account)
    fake_collection.update_one.assert_called_with(
        {"identifier_document.cpf": stub_exchange_account.cpf},
        {"$set": {
            "ouro_invest.status": stub_exchange_account.status.value
        }}
    )
    mocked_env.assert_called()
    assert response is expected
