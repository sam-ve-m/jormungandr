# term
from func.src.domain.exceptions.transports.exception import SignTermStatusCodeNotOk
from func.src.transports.term.transport import TermTransport
from tests.src.transports.term.stubs import RequestStub

# Standards
from unittest.mock import patch

# Third party
import pytest


@pytest.mark.asyncio
@patch("func.src.transports.term.transport.config")
@patch("func.src.transports.term.transport.AsyncClient.put", return_value=RequestStub(status_code=200))
async def test_when_term_sign_with_successfully_then_return_true(mock_put,  mock_config):
    result = await TermTransport.sign_term(jwt="123", body={"teste": "teste"})

    assert result is True


@pytest.mark.asyncio
@patch("func.src.transports.term.transport.config")
@patch("func.src.transports.term.transport.AsyncClient.put", return_value=RequestStub(status_code=500))
async def test_when_failed_to_sign_term_then_raises(mock_put, mock_config):
    with pytest.raises(SignTermStatusCodeNotOk):
        await TermTransport.sign_term(jwt="123", body={"teste": "teste"})
