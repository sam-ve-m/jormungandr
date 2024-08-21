# PROJECT IMPORTS
from unittest.mock import patch, MagicMock

import pytest

from func.src.repositories.bureau_transactions.repository import BureauTransactionRepository
from func.src.repositories.user.repository import UserRepository
from func.src.services.web_hook.service import BureauValidationService
from func.src.transport.persephone.transport import SendToPersephone
from func.src.transport.iara.transport import BureauApiTransport


dummy_webhook_message = MagicMock()
dummy_success = True


@pytest.mark.asyncio
@patch.object(UserRepository, "update_bureau_validation", return_value=dummy_success)
@patch.object(BureauApiTransport, "detail_transaction", return_value=dummy_webhook_message)
@patch.object(SendToPersephone, "register_user_cpf_validation_log", return_value=dummy_webhook_message)
@patch.object(BureauTransactionRepository, "update_bureau_transaction", return_value=dummy_webhook_message)
@patch.object(BureauTransactionRepository, "get_user_cpf_of_transaction", return_value=dummy_webhook_message)
async def test_save_exchange_account_without_updating(
        mocked_get_id, mocked_repository, mocked_persephone,
        mocked_transport, mocked_update
):
    result = await BureauValidationService.save_bureau_validation(dummy_webhook_message)
    mocked_get_id.assert_called_once_with(dummy_webhook_message)
    mocked_repository.assert_called_once_with(
        dummy_webhook_message
    )
    mocked_persephone.assert_called_once_with(
        mocked_get_id.return_value,
        dummy_webhook_message
    )
    mocked_transport.assert_called_once_with(
        mocked_get_id.return_value,
    )
    mocked_update.assert_called_once_with(
        mocked_get_id.return_value,
        dummy_webhook_message
    )
    assert result == dummy_success
