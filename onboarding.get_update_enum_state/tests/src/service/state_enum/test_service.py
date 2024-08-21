from unittest.mock import patch

import pytest

from func.src.domain.validators.state.validator import StateParams
from func.src.repository.state_enum.repository import StateEnumRepository
from func.src.service.state_enum.service import StateEnumService
from tests.test_doubles.doubles import (
    enum_service_get_enums_response_ok,
    enum_service_get_enums_response_none,
)
from tests.test_doubles.doubles import (
    enum_service_response_ok,
)


@patch.object(StateEnumRepository, "get_state_enum")
def test_get_response_when_enums_are_ok(get_enums_mock):
    get_enums_mock.return_value = enum_service_get_enums_response_ok
    result = StateEnumService.get_response(StateParams(country="BRA"))
    assert result == enum_service_response_ok


@patch.object(StateEnumRepository, "get_state_enum")
def test_get_response_when_enums_are_none(get_enums_mock):
    get_enums_mock.return_value = enum_service_get_enums_response_none
    with pytest.raises(TypeError):
        result = StateEnumService.get_response(StateParams(country="BRA"))
