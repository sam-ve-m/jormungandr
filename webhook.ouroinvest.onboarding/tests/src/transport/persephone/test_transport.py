# THIRD PARTY IMPORTS
from unittest.mock import patch, MagicMock

import pytest
from decouple import Config
from etria_logger import Gladsheim
from persephone_client import Persephone

# PROJECT IMPORTS
from src.domain.exceptions.exceptions import NotSentToPersephone
from src.transport.persephone.transport import SendToPersephone

dummy_env = 0
dummy_unique_id = "unique id"
stub_exchange_account = MagicMock()


@pytest.mark.asyncio
@patch.object(Gladsheim, "error")
@patch.object(Config, "__call__", return_value=dummy_env)
@patch.object(Persephone, "send_to_persephone", return_value=(True, True))
async def test_register_user_exchange_member_log(
        mocked_persephone, mocked_env, mocked_log
):
    await SendToPersephone.register_user_exchange_member_log(dummy_unique_id, stub_exchange_account)
    stub_exchange_account.log_schema.assert_called_once_with(dummy_unique_id)
    mocked_persephone.assert_called_once_with(
        topic=dummy_env,
        partition=dummy_env,
        message=stub_exchange_account.log_schema.return_value,
        schema_name=dummy_env,
    )
    mocked_log.assert_not_called()
    mocked_env.assert_called()


@pytest.mark.asyncio
@patch.object(Gladsheim, "error")
@patch.object(Config, "__call__", return_value=dummy_env)
@patch.object(Persephone, "send_to_persephone", return_value=(False, False))
async def test_register_user_exchange_member_log_raising(
        mocked_persephone, mocked_env, mocked_log
):
    with pytest.raises(NotSentToPersephone):
        await SendToPersephone.register_user_exchange_member_log(dummy_unique_id, stub_exchange_account)
    stub_exchange_account.log_schema.assert_called_with(dummy_unique_id)
    mocked_persephone.assert_called_once_with(
        topic=dummy_env,
        partition=dummy_env,
        message=stub_exchange_account.log_schema.return_value,
        schema_name=dummy_env,
    )
    mocked_log.assert_called_once_with(
        message="SendToPersephone::register_user_exchange_member_log::Error on trying to register log",
        status=False,
    )
    mocked_env.assert_called()
