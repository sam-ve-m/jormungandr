from func.src.infrastructure.http.infrastructure import HttpInfrastructure
from unittest.mock import patch
import aiohttp


@patch.object(aiohttp, "ClientSession")
def test_get_session(mocked_client):
    assert HttpInfrastructure.session is None
    client = HttpInfrastructure.get_session()
    mocked_client.assert_called_once_with()
    assert HttpInfrastructure.session == client == mocked_client.return_value
    new_client = HttpInfrastructure.get_session()
    mocked_client.assert_called_once_with()
    assert HttpInfrastructure.session == client == mocked_client.return_value == new_client
    HttpInfrastructure.session = None
