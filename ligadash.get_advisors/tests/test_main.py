from unittest.mock import patch
import pytest
from func.main import get_enums
from func.src.repository.advisor_enum.repository import AdvisorEnumRepository
from func.src.service.advisor_enum.service import AdvisorEnumService
from tests.test_doubles.doubles import (
    main_service_response_dummy,
    main_response_dummy,
    enum_service_get_enums_response_none,
    enum_service_response_none,
    enum_service_response_invalid,
)

service_response_dummy = main_service_response_dummy


@pytest.mark.asyncio
@patch.object(AdvisorEnumService, "get_response")
async def test_response_when_is_all_ok(get_response_mock):
    get_response_mock.return_value = service_response_dummy
    response = await get_enums()
    expected_response = main_response_dummy
    assert response.data == expected_response


@pytest.mark.asyncio
@patch.object(AdvisorEnumRepository, "get_advisor_enum")
async def test_get_response_when_enums_are_none(get_enums_mock):
    get_enums_mock.return_value = enum_service_get_enums_response_none
    result = await get_enums()
    assert result.data == enum_service_response_none.encode()


@pytest.mark.asyncio
@patch.object(AdvisorEnumRepository, "get_advisor_enum")
async def test_get_response_when_enums_are_invalid(get_enums_mock):
    get_enums_mock.side_effect = Exception("Erroooooou!")
    result = await get_enums()
    assert result.data == enum_service_response_invalid.encode()
