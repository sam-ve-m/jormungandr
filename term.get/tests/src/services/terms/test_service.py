from unittest.mock import patch

from pytest import mark

from src.domain.models.request.model import TermModel
from src.repositories.cache.repository import CacheRepository
from src.repositories.terms.repository import (
    TermRepository,
)
from src.services.terms.service import TermService

term_model_dummy = TermModel(file_type="term_refusal")


@mark.asyncio
@patch.object(
    TermRepository,
    "get_term_link",
    return_value="https://www.term_link_here.com",
)
@patch.object(CacheRepository, "save_term_in_cache", return_value=True)
@patch.object(
    CacheRepository, "get_cached_term", return_value="https://www.term_link_here.com"
)
async def test_get_term_url_when_there_is_cache(
    get_in_cache_mock, save_in_cache_mock, generate_url_mock
):
    result = await TermService.get_term_url(term_model_dummy)
    assert type(result) == str
    assert get_in_cache_mock.called
    assert not generate_url_mock.called


@mark.asyncio
@patch.object(
    TermRepository,
    "get_term_link",
    return_value="https://www.term_link_here.com",
)
@patch.object(CacheRepository, "save_term_in_cache", return_value=True)
@patch.object(CacheRepository, "get_cached_term", return_value=None)
async def test_get_term_url_when_there_is_no_cache(
    get_in_cache_mock, save_in_cache_mock, generate_url_mock
):
    result = await TermService.get_term_url(term_model_dummy)
    assert type(result) == str
    assert get_in_cache_mock.called
    assert save_in_cache_mock.called
    assert generate_url_mock.called
