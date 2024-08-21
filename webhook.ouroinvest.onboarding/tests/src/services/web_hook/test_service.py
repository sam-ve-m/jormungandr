# PROJECT IMPORTS
from unittest.mock import patch, MagicMock

import pytest

from src.domain.enums.ouroinvest_status.enum import OuroInvestStatus
from src.domain.exceptions.exceptions import UserWasNotFound, UserWasNotUpdated
from src.repositories.user.repository import UserRepository
from src.services.web_hook.service import ExchangeAccountService
from src.transport.persephone.transport import SendToPersephone
from src.transport.iara.transport import IaraTransport


dummy_webhook_message = MagicMock()


@pytest.mark.asyncio
@patch.object(UserRepository, "find_client_unique_id", return_value=None)
@patch.object(IaraTransport, "save_account_exchange")
@patch.object(SendToPersephone, "register_user_exchange_member_log")
@patch.object(UserRepository, "update_exchange_account_status")
async def test_save_exchange_account_without_finding_id(
        mocked_update, mocked_persephone,
        mocked_transport, mocked_repository
):
    with pytest.raises(UserWasNotFound):
        await ExchangeAccountService.save_exchange_account(dummy_webhook_message)
    mocked_repository.assert_called_once_with(dummy_webhook_message.cpf)
    mocked_persephone.assert_not_called()
    mocked_transport.assert_not_called()
    mocked_update.assert_not_called()


@pytest.mark.asyncio
@patch.object(UserRepository, "find_client_unique_id")
@patch.object(IaraTransport, "save_account_exchange")
@patch.object(SendToPersephone, "register_user_exchange_member_log")
@patch.object(UserRepository, "update_exchange_account_status", return_value=False)
async def test_save_exchange_account_without_exchange_account(
        mocked_update, mocked_persephone,
        mocked_transport, mocked_repository
):
    with pytest.raises(UserWasNotUpdated):
        await ExchangeAccountService.save_exchange_account(dummy_webhook_message)
    mocked_repository.assert_called_once_with(dummy_webhook_message.cpf)
    mocked_persephone.assert_called_once_with(
        webhook_message=dummy_webhook_message,
        unique_id=mocked_repository.return_value
    )
    mocked_transport.assert_not_called()
    mocked_update.assert_called_once_with(dummy_webhook_message)


@pytest.mark.asyncio
@patch.object(UserRepository, "find_client_unique_id")
@patch.object(IaraTransport, "save_account_exchange")
@patch.object(SendToPersephone, "register_user_exchange_member_log")
@patch.object(UserRepository, "update_exchange_account_status")
async def test_save_exchange_account_not_ok_status(
        mocked_update, mocked_persephone,
        mocked_transport, mocked_repository
):
    response = await ExchangeAccountService.save_exchange_account(dummy_webhook_message)
    mocked_repository.assert_called_once_with(dummy_webhook_message.cpf)
    mocked_persephone.assert_called_once_with(
        webhook_message=dummy_webhook_message,
        unique_id=mocked_repository.return_value
    )
    mocked_update.assert_called_once_with(dummy_webhook_message)
    mocked_transport.assert_not_called()
    assert response == mocked_update.return_value


@pytest.mark.asyncio
@patch.object(UserRepository, "find_client_unique_id")
@patch.object(IaraTransport, "save_account_exchange")
@patch.object(SendToPersephone, "register_user_exchange_member_log")
@patch.object(UserRepository, "update_exchange_account_status")
async def test_save_exchange_account_ok_status(
        mocked_update, mocked_persephone,
        mocked_transport, mocked_repository
):
    dummy_webhook_message.status = OuroInvestStatus.CONCLUIDO
    response = await ExchangeAccountService.save_exchange_account(dummy_webhook_message)
    mocked_repository.assert_called_once_with(dummy_webhook_message.cpf)
    mocked_persephone.assert_called_once_with(
        webhook_message=dummy_webhook_message,
        unique_id=mocked_repository.return_value
    )
    mocked_update.assert_called_once_with(dummy_webhook_message)
    mocked_transport.assert_called_once_with(mocked_repository.return_value)
    assert response == mocked_update.return_value

