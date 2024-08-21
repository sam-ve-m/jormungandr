from unittest.mock import patch

import pytest
from iara_client import Iara, IaraTopics

from func.src.domain.exceptions.exceptions import ErrorSendingToIaraDatailCpfValidation
from func.src.transport.iara.transport import BureauApiTransport

dummy_value = "dummy value"

success_none = None, True
content_none = True, None


@pytest.mark.asyncio
@patch.object(Iara, "send_to_iara")
async def test_detail_transaction_raising_error(mocked_transport):
    mocked_transport.return_value = None, dummy_value
    with pytest.raises(ErrorSendingToIaraDatailCpfValidation) as error:
        await BureauApiTransport.detail_transaction(dummy_value)
        assert str(error) == dummy_value
    mocked_transport.assert_called_once_with(
        topic=IaraTopics.CAF_CPF_VALIDATION_DETAILS,
        message={"cpf": dummy_value},
    )


@pytest.mark.asyncio
@patch.object(Iara, "send_to_iara")
async def test_detail_transaction(mocked_transport):
    expected_response, dummy_content = "response", "dummy_content"
    mocked_transport.return_value = True, dummy_content
    response = await BureauApiTransport.detail_transaction(dummy_value)
    mocked_transport.assert_called_once_with(
        topic=IaraTopics.CAF_CPF_VALIDATION_DETAILS,
        message={"cpf": dummy_value},
    )
    assert response is True
