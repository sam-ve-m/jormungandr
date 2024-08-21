from unittest.mock import patch, MagicMock

import pytest
from decouple import Config
from iara_client import Iara, IaraTopics

from src.domain.exceptions.exceptions import NotSentToIara
from src.transport.iara.transport import IaraTransport

dummy_cpf = "dummy cpf"
dummy_status = "dummy status"
stub_message = MagicMock(cpf=dummy_cpf, status=dummy_status)


@pytest.mark.asyncio
@patch.object(Iara, "send_to_iara")
async def test_save_account_exchange_raising_error(mocked_transport):
    dummy_content = "content"
    mocked_transport.return_value = False, dummy_content
    with pytest.raises(NotSentToIara) as error:
        await IaraTransport.save_account_exchange(stub_message)
        assert str(error) == dummy_content
    mocked_transport.assert_called_once_with(
        topic=IaraTopics.OURO_INVESTE_BASIC_REGISTRATION_DETAILS,
        message={"unique_id": stub_message},
    )


@pytest.mark.asyncio
@patch.object(Iara, "send_to_iara")
async def test_save_account_exchange(mocked_transport):
    dummy_content = "dummy_content"
    mocked_transport.return_value = True, dummy_content
    response = await IaraTransport.save_account_exchange(stub_message)
    mocked_transport.assert_called_once_with(
        topic=IaraTopics.OURO_INVESTE_BASIC_REGISTRATION_DETAILS,
        message={"unique_id": stub_message},
    )
    assert response is None
