from unittest.mock import patch

from func.src.repository.base_repository.oracle.repository import OracleBaseRepository
from func.src.repository.enum_state_cache.repository import EnumStateCacheRepository
from func.src.repository.state_enum.repository import StateEnumRepository
from tests.test_doubles.doubles import (
    enum_repository_get_cached_enum_dummy,
    enum_repository_get_from_cache_dummy_none,
    enum_repository_get_from_cache_dummy_list,
    enum_repository_query_dummy,
    enum_repository_save_in_cache_dummy,
)


@patch.object(StateEnumRepository, "_get_state_cached_enum")
def test_get_enums(_get_cached_enum_mock):
    _get_cached_enum_mock.return_value = enum_repository_get_cached_enum_dummy
    result = StateEnumRepository.get_state_enum(country="BRA")
    assert type(result) == list
    for item in result:
        assert type(item) == tuple


@patch.object(OracleBaseRepository, "query")
@patch.object(EnumStateCacheRepository, "save_enum_state")
@patch.object(EnumStateCacheRepository, "get_enum_state")
def test_get_cached_enums_when_there_is_cache(
    get_from_cache_mock, save_in_cache_mock, query_mock
):
    get_from_cache_mock.return_value = enum_repository_get_from_cache_dummy_list
    save_in_cache_mock.return_value = enum_repository_query_dummy
    query_mock.return_value = enum_repository_save_in_cache_dummy
    result = StateEnumRepository._get_state_cached_enum(query="", country="BRA")
    assert result == EnumStateCacheRepository.get_enum_state(country="BRA")


@patch.object(OracleBaseRepository, "query")
@patch.object(EnumStateCacheRepository, "save_enum_state")
@patch.object(EnumStateCacheRepository, "get_enum_state")
def test_get_cached_enums_when_there_is_no_cache(
    get_from_cache_mock, save_in_cache_mock, query_mock
):
    get_from_cache_mock.return_value = enum_repository_get_from_cache_dummy_none
    save_in_cache_mock.return_value = enum_repository_query_dummy
    query_mock.return_value = enum_repository_save_in_cache_dummy
    result = StateEnumRepository._get_state_cached_enum(query="", country="BRA")
    assert query_mock.called
    assert result == OracleBaseRepository.query("")
    assert save_in_cache_mock.called
    assert EnumStateCacheRepository.save_enum_state(enum_state=[], country="BRA")
