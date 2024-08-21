from unittest.mock import patch
import pytest
from func.main import get_enums
from func.src.repository.marital_status_enum.repository import MaritalStatusEnumRepository
from func.src.service.marital_status_enum.service import MaritalStatusEnumService
from tests.test_doubles.doubles import (
    main_service_response_dummy,
    main_response_dummy,
    enum_service_get_enums_response_none,
    enum_service_response_none,
    enum_service_response_invalid,
)

service_response_dummy = main_service_response_dummy


@pytest.mark.asyncio
@patch.object(MaritalStatusEnumService, "get_response")
async def test_response_when_is_all_ok(get_response_mock):
    get_response_mock.return_value = service_response_dummy
    response = await get_enums()
    expected_response = main_response_dummy
    assert response.data == expected_response


@pytest.mark.asyncio
@patch.object(MaritalStatusEnumRepository, "get_marital_status_enum")
async def test_get_response_when_enums_are_none(get_enums_mock):
    get_enums_mock.return_value = enum_service_get_enums_response_none
    result = await get_enums()
    assert result.data == enum_service_response_none.encode()


@pytest.mark.asyncio
@patch.object(MaritalStatusEnumRepository, "get_marital_status_enum")
async def test_get_response_when_enums_are_invalid(get_enums_mock):
    get_enums_mock.side_effect = Exception("Erroooooou!")
    result = await get_enums()
    assert result.data == enum_service_response_invalid.encode()
