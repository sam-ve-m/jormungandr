from unittest.mock import patch
import pytest

from src.service.document_issuer_enum.service import DocumentIssuerEnumService
from src.repository.document_issuer_enum.repository import DocumentIssuerEnumRepository

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


@patch.object(DocumentIssuerEnumRepository, "get_document_issuer_enum")
def test_get_response_when_enums_are_ok(get_enums_mock):
    get_enums_mock.return_value = enum_service_get_enums_response_ok
    result = DocumentIssuerEnumService.get_response()
    assert result == enum_service_response_ok


@patch.object(DocumentIssuerEnumRepository, "get_document_issuer_enum")
def test_get_response_when_enums_are_none(get_enums_mock):
    get_enums_mock.return_value = enum_service_get_enums_response_none
    with pytest.raises(TypeError):
        result = DocumentIssuerEnumService.get_response()
