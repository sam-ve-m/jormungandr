from unittest.mock import patch
import pytest

from func.src.service.experience_time_enum.service import ExperienceTimeEnumService
from func.src.repository.experience_time_enum.repository import ExperienceTimeEnumRepository

from tests.test_doubles.doubles import (
    enum_service_get_enums_response_ok,
    enum_service_get_enums_response_invalid,
    enum_service_get_enums_response_none,
)
from tests.test_doubles.doubles import (
    enum_service_response_ok,
    enum_service_response_invalid,
    enum_service_response_none,
)


@patch.object(ExperienceTimeEnumRepository, "get_experience_time_enum")
def test_get_response_when_enums_are_ok(get_enums_mock):
    get_enums_mock.return_value = enum_service_get_enums_response_ok
    result = ExperienceTimeEnumService.get_response()
    assert result == enum_service_response_ok


@patch.object(ExperienceTimeEnumRepository, "get_experience_time_enum")
def test_get_response_when_enums_are_none(get_enums_mock):
    get_enums_mock.return_value = enum_service_get_enums_response_none
    with pytest.raises(TypeError):
        result = ExperienceTimeEnumService.get_response()
