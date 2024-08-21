from src.repository.document_issuer_enum.repository import DocumentIssuerEnumRepository
from src.repository.enum_document_issuer_cache.repository import (
    EnumDocumentIssuerCacheRepository,
)
from src.repository.base_repository.oracle.repository import OracleBaseRepository
from tests.test_doubles.doubles import (
    enum_repository_get_cached_enum_dummy,
    enum_repository_get_from_cache_dummy_none,
    enum_repository_get_from_cache_dummy_list,
    enum_repository_query_dummy,
    enum_repository_save_in_cache_dummy,
)
from unittest.mock import patch


@patch.object(DocumentIssuerEnumRepository, "_get_document_issuer_cached_enum")
def test_get_enums(_get_cached_enum_mock):
    _get_cached_enum_mock.return_value = enum_repository_get_cached_enum_dummy
    result = DocumentIssuerEnumRepository.get_document_issuer_enum()
    assert type(result) == list
    for item in result:
        assert type(item) == tuple


@patch.object(OracleBaseRepository, "query")
@patch.object(EnumDocumentIssuerCacheRepository, "save_enum_document_issuer")
@patch.object(EnumDocumentIssuerCacheRepository, "get_enum_document_issuer")
def test_get_cached_enums_when_there_is_cache(
    get_from_cache_mock, save_in_cache_mock, query_mock
):
    get_from_cache_mock.return_value = enum_repository_get_from_cache_dummy_list
    save_in_cache_mock.return_value = enum_repository_query_dummy
    query_mock.return_value = enum_repository_save_in_cache_dummy
    result = DocumentIssuerEnumRepository._get_document_issuer_cached_enum("")
    assert result == EnumDocumentIssuerCacheRepository.get_enum_document_issuer()


@patch.object(OracleBaseRepository, "query")
@patch.object(EnumDocumentIssuerCacheRepository, "save_enum_document_issuer")
@patch.object(EnumDocumentIssuerCacheRepository, "get_enum_document_issuer")
def test_get_cached_enums_when_there_is_no_cache(
    get_from_cache_mock, save_in_cache_mock, query_mock
):
    get_from_cache_mock.return_value = enum_repository_get_from_cache_dummy_none
    save_in_cache_mock.return_value = enum_repository_query_dummy
    query_mock.return_value = enum_repository_save_in_cache_dummy
    result = DocumentIssuerEnumRepository._get_document_issuer_cached_enum("")
    assert query_mock.called
    assert result == OracleBaseRepository.query("")
    assert save_in_cache_mock.called
    assert EnumDocumentIssuerCacheRepository.save_enum_document_issuer([])
