from unittest.mock import patch
import pytest

from func.src.service.document_type_enum.service import DocumentTypeEnumService
from func.src.repository.document_type_enum.repository import DocumentTypeEnumRepository

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


@patch.object(DocumentTypeEnumRepository, "get_document_type_enum")
def test_get_response_when_enums_are_ok(get_enums_mock):
    get_enums_mock.return_value = enum_service_get_enums_response_ok
    result = DocumentTypeEnumService.get_response()
    assert result == enum_service_response_ok


@patch.object(DocumentTypeEnumRepository, "get_document_type_enum")
def test_get_response_when_enums_are_none(get_enums_mock):
    get_enums_mock.return_value = enum_service_get_enums_response_none
    with pytest.raises(TypeError):
        result = DocumentTypeEnumService.get_response()
