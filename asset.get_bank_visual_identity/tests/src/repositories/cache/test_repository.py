from unittest.mock import patch

import pytest
from etria_logger import Gladsheim
from mnemosine import SyncCache

from func.src.repositories.cache.repository import CacheRepository


@patch.object(SyncCache, "save")
def test_save_logo_in_cache(save_mock):
    result = CacheRepository.save_logo_in_cache("logo_link", "79")
    assert save_mock.called
    assert result is True


@patch.object(Gladsheim, "error")
@patch.object(SyncCache, "save")
def test_save_logo_in_cache_when_value_error_occurs(save_mock, etria_mock):
    save_mock.side_effect = ValueError()
    result = CacheRepository.save_logo_in_cache("logo_link", "79")
    assert save_mock.called
    assert etria_mock.called
    assert result is False


@patch.object(Gladsheim, "error")
@patch.object(SyncCache, "save")
def test_save_logo_in_cache_when_type_error_occurs(save_mock, etria_mock):
    save_mock.side_effect = TypeError()
    result = CacheRepository.save_logo_in_cache("logo_link", "79")
    assert save_mock.called
    assert etria_mock.called
    assert result is False


@patch.object(Gladsheim, "error")
@patch.object(SyncCache, "save")
def test_save_logo_in_cache_when_exception_occurs(save_mock, etria_mock):
    save_mock.side_effect = Exception()
    result = CacheRepository.save_logo_in_cache("logo_link", "79")
    assert save_mock.called
    assert etria_mock.called
    assert result is False


@patch.object(SyncCache, "get")
def test_get_cached_logo(get_mock):
    get_return_value = "https://www.image_link_here.com"
    get_mock.return_value = get_return_value
    result = CacheRepository.get_cached_logo("79")
    assert result == get_return_value


@patch.object(Gladsheim, "error")
@patch.object(SyncCache, "get")
def test_get_cached_logo_exception(get_mock, etria_mock):
    get_return_value = "https://www.image_link_here.com"
    get_mock.side_effect = Exception()
    result = CacheRepository.get_cached_logo("79")
    assert etria_mock.called
    assert result is None
