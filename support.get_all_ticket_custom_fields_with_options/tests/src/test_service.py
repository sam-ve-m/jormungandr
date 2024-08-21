# Jormungandr
from func.src.service import __request_zendesk_custom_fields, __treatment_ticket_custom_fields, get_all_custom_fields
from func.src.exceptions import InvalidEndpointZendeskApi, ErrorToRequestZendeskApi
from .stubs import StubRequestObj, ticket_custom_fields, treatment_ticket_custom_fields

# Standards
from unittest.mock import patch

# Third party
from decouple import config
import pytest


@patch('func.src.service.requests.get', return_value=StubRequestObj(status_code=200))
def test_when_valid_api_url_then_return_ticket_custom_fields(mock_requests_get):
    response = __request_zendesk_custom_fields()
    assert isinstance(response, dict)
    assert 'ticket_fields' in response


@patch('func.src.service.requests.get', return_value=StubRequestObj(status_code=200))
def test_when_valid_api_url_then_mock_requests_has_called(mock_requests_get):
    __request_zendesk_custom_fields()

    mock_requests_get.assert_called_once_with(config('ZENDESK_TICKET_CUSTOM_FIELDS_API_URL'),
                                              auth=(config('ZENDESK_LOGIN'), config('ZENDESK_PASSWORD')))


@patch('func.src.service.requests.get', return_value=StubRequestObj(status_code=404))
def test_when_api_url_missing_letters_then_raises(mock_requests_get):
    with pytest.raises(InvalidEndpointZendeskApi):
        __request_zendesk_custom_fields()


@patch('func.src.service.requests.get', return_value=Exception)
def test_when_api_zendesk_unavailable_then_raises(mock_requests_get):
    with pytest.raises(ErrorToRequestZendeskApi):
        __request_zendesk_custom_fields()


def test_when_valid_dict_then_return_treatment_custom_fields():
    treatment_custom_fields = __treatment_ticket_custom_fields(ticket_custom_fields)
    assert isinstance(treatment_custom_fields, dict)
    assert 'custom_fields' in treatment_custom_fields


@patch('func.src.service.RedisRepository.get', return_value=str(treatment_ticket_custom_fields).encode())
def test_when_data_on_redis_then_return_ticket_custom_fields(mock_redis_get):
    response = get_all_custom_fields()
    assert isinstance(response, dict)
    assert 'custom_fields' in response


@patch('func.src.service.RedisRepository.get', return_value=str(treatment_ticket_custom_fields).encode())
def test_when_data_on_redis_then_mock_redis_has_called(mock_redis_get):
    get_all_custom_fields()
    mock_redis_get.assert_called_once_with()


@patch('func.src.service.RedisRepository.set')
@patch('func.src.service.__request_zendesk_custom_fields', return_value=ticket_custom_fields)
@patch('func.src.service.RedisRepository.get', return_value=None)
def teste_when_there_is_no_data_in_redis_then_request_and_treatment_custom_fields(mock_redis_get, mock__request_zendesk, mock_redis_set):
    response = get_all_custom_fields()
    assert isinstance(response, dict)
    assert 'custom_fields' in response


@patch('func.src.service.RedisRepository.set')
@patch('func.src.service.__request_zendesk_custom_fields', return_value=ticket_custom_fields)
@patch('func.src.service.RedisRepository.get', return_value=None)
def teste_when_there_is_no_data_in_redis_then_mock_redis_set_has_called(mock_redis_get, mock__request_zendesk, mock_redis_set):
    get_all_custom_fields()
    mock_redis_set.assert_called_once_with(treatment_ticket_custom_fields)
